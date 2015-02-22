import sqlite3, os, tempfile, subprocess
import json, itertools, codecs
import src.code_db as code_db
from src.helpers import temp_working_space, sqlite_chunked_itr

#use_multicore = False
#use_multicore = True

#f_code = "../gitpull/db/code.db"
#f_code = 'db/code.db'
f_code = 'code.db'
conn = sqlite3.connect(f_code,check_same_thread=False)

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
    proc = subprocess.Popen(["ruby",d,target_dir],
                            stdout=subprocess.PIPE)
    ITEMS = []
    for line in iter(proc.stdout.readline, ''):
        js = json.loads(line)
        md5 = os.path.basename(js["name"]).split('.')[0]
        ITEMS.append([md5,js["sloc"], js["language"]])

    return ITEMS


def identify_chunk(items):

    with temp_working_space() as tmp_dir:
        for md5, ex, fbuff in items:
            f = os.path.join(tmp_dir, md5+ex)
            with codecs.open(f,'w','utf-8') as FOUT:              
                FOUT.write(fbuff)
        data = get_language_from_linguist(tmp_dir, src_dir)
    return data
    
def get_ID_left():
    cmd = "SELECT COUNT(*) FROM code WHERE is_identified=0 LIMIT 1"
    ID_LEFT = conn.execute(cmd)
    return ID_LEFT.fetchall()[0][0]

'''
def get_tokenize_left(lang_id=None):
    if lang_id is None:
        cmd = "SELECT COUNT(*) FROM code WHERE is_tokenized=0"
    else:
        cmd = ("SELECT COUNT(*) FROM code WHERE is_tokenized=0 "
               "AND language_id={idx}")

    cmd = cmd.format(idx=lang_id)
    ID_LEFT = conn.execute(cmd)

    return ID_LEFT.next()[0]
'''

#######################################################################

def read_buffer(chunk_size=100):
    cmd = 'SELECT md5, extension, text FROM code WHERE is_identified=0'
    QUERY = sqlite_chunked_itr(conn, cmd, chunk_size)

    for chunk in QUERY:
        decoded_chunk = []
        for x in chunk:
            code_buffer = x[2]
            code = code_buffer[:].decode('utf-8')
            decoded_chunk.append([x[0],x[1], code])
        yield decoded_chunk


def process_language_id(data):
    final_data = []
        
    for md5,sloc,lang in data:
        lang_id = code_db.get_language_id(lang)
        vals = (sloc,lang_id,md5)
        final_data.append(vals)
       
    return final_data


import multiprocessing as mp
P = mp.Pool()
ITR = P.imap(identify_chunk, read_buffer(1000))
#ITR = itertools.imap(identify_chunk, read_buffer(100))
for data in ITR:

    final_data = process_language_id(data)

    print "Remaining files to ID", get_ID_left()

    cmd_update = '''UPDATE code SET LOC=?, language_id=?, 
                    is_identified=1 WHERE md5=?'''

    conn.executemany(cmd_update, final_data)
    conn.commit()


