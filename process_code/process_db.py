import sqlite3, os, contextlib, tempfile

use_multicore = False

f_code = "db/code.db"
conn = sqlite3.connect(f_code,check_same_thread=False)

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

with temp_working_space() as tmp_dir:
    for items in TODO_ITR("md5, text", "identified",3):

        os.chdir(tmp_dir)

        for md5, fbuff in items:
            print md5
            with open(md5,'w') as FOUT:
                FOUT.write(fbuff)

        os.system('bash')
        exit()
        print items
