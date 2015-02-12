## Example code, not working yet.
import requests, json, codecs, ast, glob, os, time

# https://api.github.com/repositories?since=364
url = "https://api.github.com/repositories"
rate_limit_api = "https://api.github.com/rate_limit"

# Set a BASH environment variable for github access
# https://help.github.com/articles/creating-an-access-token-for-command-line-use/
oauth_token = os.environ["GITHUB_TOKEN"]

os.system("mkdir -p headers")
os.system("mkdir -p content")

def check_limits():
    
    payload = {"access_token":oauth_token,}
    R = requests.get(rate_limit_api,params=payload)
    limit_js = ast.literal_eval(R.text)
    remaining = limit_js["rate"]["remaining"]
    print "Requests remaing", remaining

    if not remaining:
        print "Overload requests, exiting"
        exit()

def parse_header_info(header):
    ''' example input from link to parse
    <https://api.github.com/repositories?since=365>; rel="next", 
    <https://api.github.com/repositories{?since}>; rel="first"
    '''
    link = header["link"]
    next_link = [x for x in link.split(', ') if '"next"' in x][0]
    since  = next_link.split("since=")[1].split('>')[0]

    return int(since)

def find_next_pagination():
    F_HEADERS = sorted(glob.glob("headers/*"))
    if not F_HEADERS:
        return 1

    f_header = F_HEADERS[-1]

    with codecs.open(f_header, 'r', 'utf-8') as FIN:
        js = json.load(FIN)
    page = parse_header_info(js)

    f_num = int(os.path.basename(f_header))
    if page < f_num:
        print "Strange pagenumber reported", f_num, page
        exit()
        page = f_num + 30

    return page

'''
def find_next_pagination():
    # Pagination lies when it gets too large
    F_CONTENT = sorted(glob.glob("content/*"))
    if not F_CONTENT:
        return 1

    f = F_CONTENT[-1]

    with codecs.open(f, 'r', 'utf-8') as FIN:
        js = json.load(FIN)
        ID = [repo["id"] for repo in js]
    
    page = max(ID)+1
    print "PAGE", page, f
    return page
'''

def grab_next_page():
    page = find_next_pagination()
    payload = {
        "since":page,
        "access_token":oauth_token,
    }

    print "Starting ", page
    check_limits()

    # Be nice
    time.sleep(4.0)

    R = requests.get(url,params=payload)
    h = dict(R.headers)

    f_header = "headers/{:010d}".format(page)
    with codecs.open(f_header, 'w', 'utf-8') as FOUT:
        json.dump(h, FOUT)

    f_content = "content/{:010d}".format(page)
    with codecs.open(f_content, 'w', 'utf-8') as FOUT:
        FOUT.write(R.text)

    print "Completed ", page

#for n in xrange(2):
while True:
    grab_next_page()
