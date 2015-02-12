import glob, json, codecs

F_CONTENT = sorted(glob.glob("content/*"))

for f in F_CONTENT:
    with codecs.open(f, 'r', 'utf-8') as FIN:
        js = json.load(FIN)
        for repo in js:
            print repo["name"], repo["html_url"], repo["fork"]

