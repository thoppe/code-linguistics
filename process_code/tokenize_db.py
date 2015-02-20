import sqlite3, os, subprocess, string, collections
import json, itertools
import src.code_db as code_db
from src.clean import code_cleaners
from src.helpers import temp_working_space, sqlite_chunked_itr
#import multiprocessing as mp

#f_code = "../gitpull/db/code.db"
#f_code = 'db/code.db'
f_code = 'code.db'
conn = sqlite3.connect(f_code)
chunk_size = 30

def get_tokenize_left(lang_id=None):
    if lang_id is None:
        cmd = "SELECT COUNT(*) FROM code WHERE is_tokenized=0"
    else:
        cmd = ("SELECT COUNT(*) FROM code WHERE is_tokenized=0 "
               "AND language_id={idx}")

    cmd = cmd.format(idx=lang_id)
    ID_LEFT = conn.execute(cmd)

    return ID_LEFT.next()[0]


def tokenize(code):
    word_tokens = string.letters + string.digits + ' _\n'
    filtered = ''.join([x if x in word_tokens 
                        else ' ' for x in code])
    filtered = [x.lower() for x in filtered.split() if len(x)<15]
    return filtered

#import multiprocessing as mp
#P = mp.Pool()

#######################################################################

print "Remaining files to tokenize: ", get_tokenize_left()

cmd_template = '''
CREATE TABLE IF NOT EXISTS tokens (
    name STRING PRIMARY KEY,
    count INTEGER DEFAULT 0
);
'''

for language in code_cleaners:
    lang_id = code_db.get_language_id(language)
    print " + remaining", language, get_tokenize_left(lang_id)

for language in code_cleaners:
    f_tokens = "db_tokens/{}.db".format(language)
    token_conn = sqlite3.connect(f_tokens)
    token_conn.executescript(cmd_template)

    lang_id = code_db.get_language_id(language)
    cmd_grab = '''SELECT md5, text FROM code WHERE 
                  is_tokenized=0 AND language_id={}'''
    cmd_mark = 'UPDATE code SET is_tokenized=1 WHERE md5=?'

    for items in sqlite_chunked_itr(conn, cmd_grab.format(lang_id), 
                                    chunk_size):

        for (md5,code,) in items:
            tokens = tokenize(code_cleaners[language](code))
            code_db.add_tokens(token_conn, tokens)
            conn.execute(cmd_mark, (md5,))

        conn.commit()
        code_db.commit()

        print " + remaining", language, get_tokenize_left(lang_id)
