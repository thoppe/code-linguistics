import sqlite3, os, collections

os.system("mkdir -p db")
os.system("mkdir -p db_tokens")

f_code = "db/code.db"
conn = sqlite3.connect(f_code,check_same_thread=False)

cmd_template = '''
CREATE TABLE IF NOT EXISTS languages (
    language_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner STRING,
    name STRING
);

CREATE TABLE IF NOT EXISTS code (
    md5 STRING PRIMARY KEY,
    extension STRING,
    language_id INT NOT NULL,
    project_id INT,
    text BLOB,
    LOC  INT,
    local_inserted_at TIMESTAMP,
    is_identified BOOL DEFAULT 0,
    is_cleaned    BOOL DEFAULT 0,
    is_tokenized  BOOL DEFAULT 0
);

--CREATE TABLE IF NOT EXISTS tokens (
--    name STRING PRIMARY KEY,
--    count INTEGER DEFAULT 0
--);

'''

conn.executescript(cmd_template)
conn.commit()


def is_new_code(*vals):
    cmd_md5_query = '''SELECT * FROM code WHERE md5=?'''
    try:
        conn.execute(cmd_md5_query, vals).next()
        return False
    except:
        return True

def get_language_id(language):
    # Gets the language_id, if a new language adds it to db
    cmd_code_query = '''SELECT language_id FROM 
    languages WHERE name=?'''

    cmd_new   = '''INSERT INTO languages (name) VALUES (?)'''
    cursor = conn.execute(cmd_code_query, (language,))

    try:
        idx = cursor.next()[0]
    except:
        conn.execute(cmd_new, (language,))
        idx = get_language_id(language)
        print "New language found: ", language

    return idx


cmd_project_query = '''SELECT * FROM projects 
                       WHERE owner=? AND name=?'''
def is_new_project(*vals):
    try:
        conn.execute(cmd_project_query, vals).next()
        return False
    except:
        return True

def get_project_id(owner,name):

    # Gets the project_id, if a new adds it to db
    cmd_new   = '''INSERT INTO projects (owner,name) VALUES (?,?)'''
    vals = (owner,name)
    cursor = conn.execute(cmd_project_query, vals)

    try:
        idx = cursor.next()[0]
    except:
        conn.execute(cmd_new, vals)
        idx = get_project_id(*vals)

    return idx

def add_code_item(items):
    # items = (md5, language_id, project_id, code, time, extension)
    md5 = items[0]

    cmd_add = '''
    INSERT INTO code (md5, language_id, project_id, 
    text, local_inserted_at, extension) VALUES (?,?,?,?,?,?)'''
    
    if is_new_code(md5):
        conn.execute(cmd_add, items)

def add_tokens(conn, tokens):
    cmd_add = '''UPDATE tokens SET count = count + ? WHERE name = ?'''
    cmd_new = '''INSERT OR IGNORE INTO tokens (name) VALUES (?)'''

    col = collections.Counter(tokens)

    def ITR():
        for name in col.keys():
            yield (name,)

    conn.executemany(cmd_new, ITR())

    def ITR():
        for name,count in col.iteritems():
            yield count,name
    conn.executemany(cmd_add, ITR())


def commit():
    conn.commit()


