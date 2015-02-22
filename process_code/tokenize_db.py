import sqlite3, os, subprocess, string, collections
import json, itertools
import src.code_db as code_db
from src.clean import code_cleaners
from src.helpers import temp_working_space, sqlite_chunked_itr
#import multiprocessing as mp

#f_code = "../gitpull/db/code.db"
#f_code = 'db/code.db'
f_code = 'code.db'
conn = sqlite3.connect(f_code, check_same_thread=False)
chunk_size = 30

def get_tokenize_left(language=None):

    if language is None:
        cmd = "SELECT COUNT(*) FROM code WHERE is_tokenized=0"
    else:
        lang_id = code_db.get_language_id(language)
        cmd = ("SELECT COUNT(*) FROM code WHERE is_tokenized=0 "
               "AND language_id={idx}").format(idx=lang_id)

    ID_LEFT = conn.execute(cmd)

    return ID_LEFT.next()[0]


def tokenize(code):
    word_tokens = string.letters + string.digits + ' _\n'
    filtered = ''.join([x if x in word_tokens 
                        else ' ' for x in code])
    filtered = [x.lower() for x in filtered.split() if len(x)<15]
    return filtered

#######################################################################

def read_buffer(language, chunk_size=100):
    lang_id = code_db.get_language_id(language)

    cmd = '''SELECT md5, text FROM code WHERE 
             is_tokenized=0 AND language_id={}'''.format(lang_id)
    QUERY = sqlite_chunked_itr(conn, cmd, chunk_size)

    for chunk in QUERY:
        decoded_chunk = []
        for md5,code_buffer in chunk:
            code = code_buffer[:].decode('utf-8')
            decoded_chunk.append([md5, code])
        yield decoded_chunk

#######################################################################

class language_chunk_tokenizer(object):
    def __init__(self,language):
        self.language = language
        self.lang_id  = code_db.get_language_id(language)
    def __call__(self, chunk):
        C = collections.Counter()
        MD5 = []
        for md5, code in chunk:
            tokens = tokenize(code_cleaners[language](code))
            C.update(tokens)
            MD5.append((md5,))
        return MD5, C

print "Remaining files to tokenize: ", get_tokenize_left()

cmd_template = '''
CREATE TABLE IF NOT EXISTS tokens (
    name STRING PRIMARY KEY,
    count INTEGER DEFAULT 0
);
'''

for language in code_cleaners:
    print " + remaining", language, get_tokenize_left(language)


import multiprocessing as mp
P = mp.Pool()

for language in code_cleaners:
    f_tokens = "db_tokens/{}.db".format(language)
    token_conn = sqlite3.connect(f_tokens)
    token_conn.executescript(cmd_template)

    L_func = language_chunk_tokenizer(language)
    ITEMS  = read_buffer(language, chunk_size=47)
    ITR = P.imap(L_func, ITEMS)
    cmd_mark = 'UPDATE code SET is_tokenized=1 WHERE md5=?'

    for MD5, tokens in ITR:

        conn.executemany(cmd_mark, MD5)
        code_db.add_tokens(token_conn, tokens)

        print " + remaining", language, get_tokenize_left(language)

        conn.commit()
        token_conn.commit()
