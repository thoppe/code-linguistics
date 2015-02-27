import sqlite3, os, json, collections

os.system("mkdir -p stats")

f_code = 'db/code.db'
conn = sqlite3.connect(f_code)

cmd_count = '''
SELECT languages.name, COUNT(*) FROM code
INNER JOIN languages ON languages.language_id = code.language_id
GROUP BY code.language_id
ORDER BY COUNT(*) DESC
'''

f_stats = "stats/language_counts.json"

data = collections.OrderedDict()
for language,count in conn.execute(cmd_count):
    data[language] = count
    sx = "{:20s} {}"
    print sx.format(language, count)

with open(f_stats,'w') as FOUT:
    json.dump(data, FOUT, indent=2)


