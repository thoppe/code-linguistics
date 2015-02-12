import requests, os, ast

'''
Helper commands for the github API
'''

# Set a BASH environment variable for github access
# https://help.github.com/articles/creating-an-access-token-for-command-line-use/
oauth_token = os.environ["GITHUB_TOKEN"]

rate_limit_url = "https://api.github.com/rate_limit"

def check_limits():
    
    payload = {"access_token":oauth_token,}
    R = requests.get(rate_limit_url,params=payload)
    limit_js = ast.literal_eval(R.text)
    remaining = limit_js["rate"]["remaining"]
    print "Requests remaing", remaining

    if not remaining:
        print "Overload requests, exiting"
        exit()

