import glob, json, codecs, sqlite3, os, time, json, datetime
from src.API_github import *

# Awesome date library
import timestring

f_repo_info = "db/repo_info.db"
conn = sqlite3.connect(f_repo_info)

# Get the column names
cursor = conn.execute('SELECT * FROM repo_info LIMIT 1')
cols = list(map(lambda x: x[0], cursor.description))
# Remove ID from cols, we don't want to change it
cols.remove("id")

cols_dates = [1 if "_at" in name else 0 for name in cols]
print cols_dates
exit()
cmd_select = '''
SELECT id,full_name FROM repo_info
WHERE created_at IS NULL AND fork=0
LIMIT {}
'''

cmd_count_left = '''
SELECT COUNT(*) FROM repo_info
WHERE created_at IS NULL AND fork=0
'''

cmd_count_completed = '''
SELECT COUNT(*) FROM repo_info
WHERE created_at IS NOT NULL AND fork=0
'''

cmd_insert = '''
UPDATE repo_info 
SET {}=?
WHERE id=?
'''.format('=?,'.join(cols))

def proper_date(date_string):
    d = timestring.Date(date_string)
    return datetime.datetime(d.year, d.month, 
                             d.day, d.hour, d.minute, 
                             d.second)

full_repo_info_url = "https://api.github.com/repos/{}"

def info_grab_iter(limit=10):

    for (idx,full_name) in conn.execute(cmd_select.format(limit)):

        payload = {"access_token":oauth_token,}

        check_limits()
        print "Downloading info for", full_name

        url = full_repo_info_url.format(full_name)

        R = requests.get(url,params=payload)
        h = dict(R.headers)
        js = json.loads(R.text)

        js["local_has_downloaded"] = 1

        try:
            vals = [js[key] for key in cols]

            vals = [proper_date(x) if is_date else x 
                    for x,is_date in zip(vals, cols_dates)]

            # For the WHERE clause
            vals += [idx,]
            yield vals

        except Exception as Ex:

            # For errors, use dummy info
            print json.dumps(js)
            null_date = datetime.datetime(2000,1,1)
            print null_date
            vals = [null_date if is_date else 0
                    for x,is_date in zip(cols, cols_dates)]
            vals[0] = idx
            vals[1] = full_name
            vals += [idx,]
            yield vals

        # Be nice
        time.sleep(0.25)

def get_items_left():
    return conn.execute(cmd_count_left).next()[0]

def get_items_completed():
    return conn.execute(cmd_count_completed).next()[0]

while True:  

    vals = (get_items_completed(), get_items_left())
    print "Item completed/remaining {}/{}".format(*vals)
    if not vals[1]: break

    for info in info_grab_iter(limit=20):
         conn.execute(cmd_insert, info)
    conn.commit()


