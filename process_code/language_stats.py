import sqlite3, os, json, collections

os.system("mkdir -p stats")

f_code = 'db/repo_info.db'
conn = sqlite3.connect(f_code)



import pylab as plt
import seaborn as sns

def plot_stat(name):

    print "Creating index for", name

    conn.executescript('''
    CREATE INDEX IF NOT EXISTS 
    idx_{name} ON repo_info({name});
    '''.format(name=name))

    cmd_get_stat = '''
    SELECT {name},COUNT(*) FROM repo_info
    GROUP BY {name}
    ORDER BY count(*) DESC
    '''.format(name=name)

    print "Querrying information for", name

    X,Y = zip(*[(y,x) for (y,x) in 
                conn.execute(cmd_get_stat) 
                if y is not None])

    print "Plotting", name

    fig = plt.figure()
    plt.loglog(X,Y,'o',alpha=0.75)
    plt.xlabel(name)
    plt.ylabel("matching repos")
    f_png = "stats/plot_{}.png".format(name)
    plt.savefig(f_png,bbox_inches="tight")

STAT_NAMES = ["stargazers_count","subscribers_count","forks_count"]
for name in STAT_NAMES:
    plot_stat(name)

#######################################################################


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


