## Example code, not working yet.

import requests, json, codecs, ast

# https://api.github.com/repositories?since=364
url = "https://api.github.com/repositories"
payload = {'since': 1}

with codecs.open("headers.json",'r','utf-8') as FIN:
    js = ast.literal_eval(FIN.read())
    #js = json.load(FIN)

for x in js:
    print x
print js["link"]

'''
R = requests.get(url,params=payload)
print R.headers
exit()

with open("tmp.json") as FIN:
    js = json.load(FIN)

for x in js:
    print (x)

print js[0]
'''
