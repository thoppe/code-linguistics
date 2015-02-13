import glob, json, codecs, sqlite3, os, itertools

os.system("mkdir -p db")

f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

cmd_template = '''
CREATE TABLE IF NOT EXISTS repo_info (
    id INT PRIMARY KEY,
    full_name STRING,
    description STRING,
    fork BOOL,
    created_at TIMESTAMP, 
    updated_at TIMESTAMP, 
    pushed_at TIMESTAMP, 
    homepage STRING, 
    size INT, 
    stargazers_count INT, 
    watchers_count INT, 
    language STRING, 
    has_issues BOOL, 
    has_downloads BOOL, 
    has_wiki BOOL, 
    has_pages BOOL, 
    forks_count INT, 
    open_issues_count INT, 
    forks INT, 
    open_issues INT, 
    watchers INT, 
    default_branch STRING, 
    network_count INT, 
    subscribers_count INT
); '''

conn.executescript(cmd_template)
conn.commit()


add_keys = ["id", "full_name", "description", "fork"]
cmd_add = '''
INSERT OR IGNORE INTO repo_info 
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

def content_file_iter(f):
    print "Reading file", f

    with codecs.open(f, 'r', 'utf-8') as FIN:
        js = json.load(FIN)
        for repo in js:
            if repo["private"]:
                print "Nothing should be private!"
            yield extract_info(repo)

def whole_content_file(f):
    return list(content_file_iter(f))

def content_iter():

    import multiprocessing
    P = multiprocessing.Pool(8)

    #ITR = itertools.imap(whole_content_file, F_CONTENT)
    ITR = P.imap(whole_content_file,F_CONTENT)

    for repo_info in ITR:
        for info in repo_info:
            yield info




#for content in content_iter():
#    print content

conn.executemany(cmd_add, content_iter())
conn.commit()
print "Complete"
