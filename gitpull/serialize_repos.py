import glob, json, sqlite3, os, json, string, hashlib
import tempfile, collections, contextlib, itertools
import glob2 # Recursive globber

F_REPO = glob2.glob("repos/**/*.gz")

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)

# Load the keywords
with open("filetypes/keywords.json") as FIN:
    keywords = json.load(FIN)

# DEBUG: only use python here
extensions = {"python":[".py"]}

def tokenize((language, f_code)):
    
    word_tokens = string.letters + string.digits + ' _\n'

    try:
        with open(f_code) as FIN: 
            raw = FIN.read()
    except:
        raw = ""

    md5 = hashlib.md5(raw).hexdigest()

    #keep_words = set(keywords[language]["keywords"] +
    #                 keywords[language]["builtins"])

    keep_words = set(keywords[language]["keywords"])
                

    filtered = ''.join([x if x in word_tokens 
                        else ' ' for x in raw]).split()
    tokens = [x for x in filtered if x in keep_words]
    counted_tokens = collections.Counter(tokens) 

    return (language, f_code, md5, tokens)


def iter_repo(folder=None):
    if folder is None:
        folder = os.getcwd()

    all_files = glob2.glob("{}/**/*".format(folder))
    all_files_ext = ['.'+f.split('.')[-1][:10] for f in all_files]

    for language in extensions:
        for ext in extensions[language]:
            for f,f_ext in zip(all_files,all_files_ext):
                if f_ext == ext:
                    yield (language, f)

@contextlib.contextmanager
def process_repo(f_repo):
    org_d = os.getcwd()
    f_full_repo = os.path.abspath(f_repo)

    d = tempfile.mkdtemp()
    os.chdir(d)

    cmd_tar = "tar -xf {}".format(f_full_repo, d)
    os.system(cmd_tar)

    try:
        yield
    finally:
        os.chdir(org_d)
        os.system("rm -rf {}".format(d))


import multiprocessing
P = multiprocessing.Pool()

def serialize(f_repo):

    print "Starting", f_repo

    with process_repo(f_repo):

        #ITR = itertools.imap(tokenize, iter_repo())
        ITR = P.imap(tokenize, iter_repo())

        for result in ITR:
            yield result

all_tokens = collections.Counter()
ITR = itertools.imap(serialize, F_REPO)

for f_repo in F_REPO[:5000]:
    for (language, f_code, md5, tokens) in serialize(f_repo):
        all_tokens.update(tokens)

import pylab as plt
import seaborn as sns
import numpy as np
print all_tokens
Y = sorted(all_tokens.values())[::-1]
Y = np.array(Y,dtype=float)
X = np.arange(1,len(Y)+1)
plt.loglog(X,Y,'o')
plt.loglog(X,Y)

F1 = (1.0/X)*Y.max()
F2 = (1.0/X**0.5)*Y.max()
F3 = (1.0/X**2)*Y.max()
plt.plot(X,F1,ls='--',label=r"$1/X$")
plt.plot(X,F2,ls='--',label=r"$1/X^{1/2}$")
plt.plot(X,F3,ls='--',label=r"$1/X^2$")
plt.title("Python keywords")
plt.legend(loc="best")


plt.axis('tight')
plt.show()

        
        

#for language, f_code in iter_repo(folder):
#    md5, tokens = tokenize(f_code)
#    print md5, tokens



'''

token_words = set(string.letters + string.digits + '_ \n')
MAX_TOKEN_SIZE = 20


'''     

