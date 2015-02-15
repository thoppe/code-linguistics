import sqlite3, os

os.system("mkdir -p db")

f_code = "db/code.db"
conn = sqlite3.connect(f_code)

cmd_template = '''
CREATE TABLE IF NOT EXISTS languages (
    language_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name STRING
);

CREATE TABLE IF NOT EXISTS code (
    md5 STRING PRIMARY KEY,
    language_id INT NOT NULL,
    github_id INT,
    text BLOB,
    local_inserted_at TIMESTAMP
); '''

conn.executescript(cmd_template)
conn.commit()

def get_language_id(language):
    # Gets the language_id, if a new language adds it to db

    cmd_query = '''SELECT language_id FROM languages WHERE name=?'''
    cmd_new   = '''INSERT INTO languages (name) VALUES (?)'''
    cursor = conn.execute(cmd_query, (language,))

    try:
        idx = cursor.next()
    except:
        conn.execute(cmd_new, (language,))
        idx = get_language_id(language)

    return idx



add_keys = ["md5", "github_id", "text", "local_inserted_at"]
cmd_add = '''
INSERT OR IGNORE INTO repo_info 
({}) VALUES (?,?,?,?)
'''.format(','.join(add_keys))

