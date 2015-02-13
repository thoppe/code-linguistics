import glob, json, sqlite3, os, json, string, hashlib
from API_github import *
import tempfile, collections

# Recursive globber
import glob2

f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

# Get the column names
cursor = conn.execute('SELECT * FROM repo_info LIMIT 1')
cols = list(map(lambda x: x[0], cursor.description))

cmd_select = '''
SELECT full_name, default_branch FROM repo_info
WHERE created_at IS NOT NULL AND size>0 LIMIT 1'''

git_url = "git://github.com/{}.git"
cmd_git = "git clone {url} --branch {branch} --single-branch {folder}"

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)

def clone_repo(full_name, branch,folder):

    payload = {
        "url":git_url.format(full_name),
        "branch":branch,
        "folder":folder
    }

    cmd = cmd_git.format(**payload)
    os.system(cmd)

def iter_repo(folder):
    all_files = glob2.glob("{}/**/*".format(folder))
    all_files_ext = ['.'+f.split('.')[-1][:10] for f in all_files]

    for language in extensions:
        for ext in extensions[language]:
            for f,f_ext in zip(all_files,all_files_ext):
                if f_ext == ext:
                    yield (language, f)


token_words = set(string.letters + string.digits + '_ \n')
MAX_TOKEN_SIZE = 20

def tokenize(f_code):

    with open(f_code) as FIN: 
        raw = FIN.read()

    md5 = hashlib.md5(raw).hexdigest()

    filtered = ''.join([x if x in token_words 
                        else ' ' for x in raw]).split()
    adjusted = [x.lower() for x in filtered if len(x)<20]
    tokens = collections.Counter(adjusted) 

    return md5,tokens
  

    

for [full_name,branch] in conn.execute(cmd_select):

    folder = "tmp_git"
    #clone_repo(full_name, branch,folder)

    for language, f_code in iter_repo(folder):
        md5, tokens = tokenize(f_code)
        print md5, tokens


        





