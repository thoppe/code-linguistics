import sqlite3, os, tempfile, subprocess
import json, itertools
import src.code_db as code_db
from src.helpers import temp_working_space, sqlite_chunked_itr

#use_multicore = False
#use_multicore = True

#f_code = "../gitpull/db/code.db"
#f_code = 'db/code.db'
f_code = 'code.db'
conn = sqlite3.connect(f_code)

chunk_size = 1000
src_dir = os.getcwd()

# Create indices for work to be done
cmd_index = '''
CREATE INDEX IF NOT EXISTS idx_cleaned ON code (is_cleaned);
CREATE INDEX IF NOT EXISTS idx_identified ON code (is_identified);
CREATE INDEX IF NOT EXISTS idx_tokenized ON code (is_tokenized);
CREATE INDEX IF NOT EXISTS idx_lang_id ON code (language_id);
'''
conn.executescript(cmd_index)


def get_language_from_linguist(target_dir='.', src_dir=""):
    d = os.path.join(src_dir, "src/linguist_helper.rb")
    proc = subprocess.Popen(["ruby",d,target_dir],stdout=subprocess.PIPE)
    ITEMS = []

    for line in iter(proc.stdout.readline, ''):
        js = json.loads(line)
        md5 = os.path.basename(js["name"]).split('.')[0]
        ITEMS.append([js["sloc"], js["language"],md5])

    return ITEMS


def identify_chunk(items):

    with temp_working_space() as tmp_dir:
    
        for md5, ex, fbuff in items:
            f = os.path.join(tmp_dir, md5+ex)

            with open(f,'w') as FOUT:
                
                FOUT.write(fbuff)

        data = get_language_from_linguist(tmp_dir, src_dir)
        final_data = []
        
        for sloc, lang, md5 in data:
            lang_id = code_db.get_language_id(lang)
            vals = (sloc,lang_id,md5)
            final_data.append(vals)

    return final_data
    
def get_ID_left():
    cmd = "SELECT COUNT(*) FROM code WHERE is_identified=0"
    ID_LEFT = conn.execute(cmd)
    return ID_LEFT.next()[0]

def get_tokenize_left(lang_id=None):
    if lang_id is None:
        cmd = "SELECT COUNT(*) FROM code WHERE is_tokenized=0"
    else:
        cmd = ("SELECT COUNT(*) FROM code WHERE is_tokenized=0 "
               "AND language_id={idx}")

    cmd = cmd.format(idx=lang_id)
    ID_LEFT = conn.execute(cmd)

    return ID_LEFT.next()[0]


#######################################################################


cmd = 'SELECT md5, extension, text FROM code WHERE is_identified==0'
for items in sqlite_chunked_itr(conn, cmd, 1000):

    print "Remaining files to ID", get_ID_left()

    data = identify_chunk(items)

    cmd_update = '''UPDATE code SET LOC=?, language_id=?, 
                    is_identified=1 WHERE md5=?'''

    conn.executemany(cmd_update, data)
    conn.commit()

