import sqlite3, os, json, collections

os.system("mkdir -p stats")

f_code = 'db/repo_info.db'
conn = sqlite3.connect(f_code)

cmd_count = '''
SELECT language, COUNT(*) FROM repo_info
GROUP BY language
ORDER BY COUNT(*) DESC
'''

data = collections.OrderedDict()
for language,count in conn.execute(cmd_count):
    data[language] = count
    sx = "{:25s} {}"
    print sx.format(str(language), count)

f_stats = "stats/repo_language_counts.json"

with open(f_stats,'w') as FOUT:
    json.dump(data, FOUT, indent=2)


##########################################################

f_code = 'db/code.db'
conn = sqlite3.connect(f_code)

cmd_count = '''
SELECT languages.name, COUNT(*) FROM code
INNER JOIN languages ON languages.language_id = code.language_id
GROUP BY code.language_id
ORDER BY COUNT(*) DESC
'''


data = collections.OrderedDict()
for language,count in conn.execute(cmd_count):
    data[language] = count
    sx = "{:25s} {}"
    print sx.format(language, count)

f_stats = "stats/downloaded_language_counts.json"

with open(f_stats,'w') as FOUT:
    json.dump(data, FOUT, indent=2)


