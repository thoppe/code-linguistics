import src.code_db as code_db
import sqlite3, os, contextlib, tempfile, subprocess, json

use_multicore = False

#f_code = "../gitpull/db/code.db"
#f_code = 'db/code.db'
f_code = 'code.db'
conn = sqlite3.connect(f_code)

# Create indices for work to be done
cmd_index = '''
CREATE INDEX IF NOT EXISTS idx_cleaned ON code (is_cleaned);
CREATE INDEX IF NOT EXISTS idx_identified ON code (is_identified);
CREATE INDEX IF NOT EXISTS idx_tokenized ON code (is_tokenized);
'''
conn.executescript(cmd_index)

@contextlib.contextmanager
def temp_working_space():
    # when used a context manager, yields the tmp_directory
    tmp_dir = tempfile.mkdtemp()
    cmd_clean = "rm -rf {}".format(tmp_dir)

    try:
        yield tmp_dir
    finally:       
        os.system(cmd_clean)


def TODO_ITR(select_targets, index_name, block_size=100):
    cmd = 'SELECT {} FROM code WHERE is_{}==0'
    cmd = cmd.format(select_targets,index_name)
    cursor = conn.execute(cmd)
    while True:
        result = cursor.fetchmany(size=block_size)
        yield result
        if not result: break


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
    

chunk_size = 1000
src_dir = os.getcwd()

def get_ID_left():
    cmd = "SELECT COUNT(*) FROM code WHERE is_identified=0"
    ID_LEFT = conn.execute(cmd)
    return ID_LEFT.next()[0]


for items in TODO_ITR("md5, extension, text", 
                      "identified", chunk_size):

    print "Remaining files to ID", get_ID_left()

    data = identify_chunk(items)

    cmd_update = '''UPDATE code SET LOC=?, language_id=?, 
                    is_identified=1 WHERE md5=?'''


    conn.executemany(cmd_update, data)
    conn.commit()
