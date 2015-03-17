import glob, json, sqlite3, os, json, string, hashlib, time
from src.API_github import *
import tempfile, collections

target_language = "JavaScript"
total_download  = 1000

# Storage for repos
os.system("mkdir -p repos")

cmd_grab = "curl -L https://api.github.com/repos/{full_name}/tarball?access_token={oauth_token} > repos/{full_name}.tar.gz"

# Connect to the DB that has been through parse_public.py
f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

# Get the column names
cursor = conn.execute('SELECT * FROM repo_info LIMIT 1')
cols = list(map(lambda x: x[0], cursor.description))

# Monkey-patch in column local_has_downloaded
cmd_new_col = '''
ALTER TABLE repo_info 
ADD COLUMN local_has_downloaded BOOL DEFAULT 0'''
if "local_has_downloaded" not in cols:
    conn.execute(cmd_new_col)

# Add some useful indices (maybe?)
cmd_index = '''
DROP INDEX IF EXISTS idx_stargazers;
DROP INDEX IF EXISTS idx_downloaded;
DROP INDEX IF EXISTS idx_downloaded_search;
'''
conn.executescript(cmd_index)

# UNMARK ALL, hard reset if wanted
#cmd_unmark_all = "UPDATE repo_info SET local_has_downloaded=0;"
#conn.execute(cmd_unmark_all)
#conn.commit()

#cmd_query_lang = '''
#SELECT language, COUNT(*) FROM repo_info GROUP BY language'''

cmd_select = '''
SELECT full_name,id,stargazers_count,size FROM repo_info
WHERE created_at IS NOT NULL 
AND size>0
AND language="{language}"
AND local_has_downloaded=0
ORDER BY stargazers_count DESC
LIMIT {total_download}
'''.format(language=target_language, total_download=total_download)

cmd_mark_downloaded = '''
UPDATE repo_info SET local_has_downloaded=1 WHERE id=?;'''

#git_url = "git://github.com/{}.git"
#cmd_git = "git clone {url} --branch {branch} --single-branch {folder}"

def download_repo_tar(items):
    full_name,idx,stargazers_count,size = items

    user_dir = full_name.split('/')[0]
    os.system("mkdir -p repos/{}".format(user_dir))

    f_out = "repos/{}.tar.gz".format(full_name)

    if not os.path.exists(f_out):
        print "Downloading", full_name, stargazers_count, size

        check_limits()
        cmd = cmd_grab.format(full_name=full_name,
                              oauth_token=oauth_token)
        os.system(cmd)
        conn.execute(cmd_mark_downloaded,(idx,))

        # Be nice
        #time.sleep(0.25)

for items in conn.execute(cmd_select):
    download_repo_tar(items)




