import glob, json, sqlite3, os, json, string, hashlib, time
from API_github import *
import tempfile, collections

# Storage for repos
os.system("mkdir -p repos")

cmd_grab = "curl -L https://api.github.com/repos/{full_name}/tarball?access_token={oauth_token} > repos/{full_name}.tar.gz"

# Connect to the DB that has been through parse_public.py
f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

# Get the column names
cursor = conn.execute('SELECT * FROM repo_info LIMIT 1')
cols = list(map(lambda x: x[0], cursor.description))

cmd_select = '''
SELECT full_name FROM repo_info
WHERE created_at IS NOT NULL AND size>0'''

#git_url = "git://github.com/{}.git"
#cmd_git = "git clone {url} --branch {branch} --single-branch {folder}"

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)

def download_repo_tar(full_name):

    user_dir = full_name.split('/')[0]
    os.system("mkdir -p repos/{}".format(user_dir))

    f_out = "repos/{}.tar.gz".format(full_name)

    if not os.path.exists(f_out):
        check_limits()
        print "DOWNLOADING: ", f_out
        cmd = cmd_grab.format(full_name=full_name,
                              oauth_token=oauth_token)
        os.system(cmd)

        # Be nice
        time.sleep(1.0) 


for (full_name,) in conn.execute(cmd_select):
    download_repo_tar(full_name)




