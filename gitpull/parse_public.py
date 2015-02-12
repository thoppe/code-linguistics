import glob, json, codecs, sqlite3, os

os.system("mkdir -p db")

f_repo_names = "db/repo_names.db"
conn = sqlite3.connect(f_repo_names)

cmd_template = '''
CREATE TABLE IF NOT EXISTS repo_names (
    id INT PRIMARY KEY,
    full_name STRING,
    description STRING,
    fork BOOL
); '''
conn.executescript(cmd_template)
conn.commit()


add_keys = ["id", "full_name", "description", "fork"]
cmd_add = '''
INSERT OR IGNORE INTO repo_names 
({}) VALUES (?,?,?,?)
'''.format(','.join(add_keys))

F_CONTENT = sorted(glob.glob("content/*"))

'''
API URL is stored as:
https://api.github.com/repos/mojombo/grit
'''

def extract_info(repo):
    ''' Keeps a subset of information of the github dump '''
    return [repo[key] for key in add_keys]

def content_iter():
    for f in F_CONTENT:
        print "Reading file", f
        with codecs.open(f, 'r', 'utf-8') as FIN:
            js = json.load(FIN)
            for repo in js:
                yield extract_info(repo)



#for content in content_iter():
#    print content

conn.executemany(cmd_add, content_iter())
conn.commit()
print "Complete"
