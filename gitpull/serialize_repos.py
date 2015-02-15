import glob, json, sqlite3, os, json, string, hashlib, datetime
import tempfile, collections, contextlib, itertools
import glob2 # Recursive globber
import src.minify_code, src.code_db as code_db
import logging


F_REPO = glob2.glob("repos/**/*.gz")

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)

# Load the keywords
with open("filetypes/keywords.json") as FIN:
    keywords = json.load(FIN)

# DEBUG: only use python here
extensions = {"python":[".py"]}

# Clean functions
code_cleaners = {
    "python" : [src.minify_code.clean_pycode] 
}
code_cleaners = collections.defaultdict(list, code_cleaners)

def open_code_file(language, f_code):
    try:
        with open(f_code) as FIN: 
            raw = FIN.read()
    except:
        raw = ""


    for func in code_cleaners[language]:
        func(raw)
        try:
            raw = func(raw)
        except Exception as ex:
            msg = "Function {} failed for {}, skipping"
            vals = func,f_code
            logging.warning(msg.format(*vals))
            raw = ""

    return raw



def tokenize((language, f_code)):
    
    word_tokens = string.letters + string.digits + ' _\n'

    raw = open_code_file(language, f_code)

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
    # Untar the repo in a tmp directory and cleanup when finished
    # when used a context manager, yields the tmp_directory

    f_full_repo = os.path.abspath(f_repo)
    tmp_dir = tempfile.mkdtemp()

    cmd_tar = "tar -xf {} -C {}".format(f_full_repo, tmp_dir)
    cmd_clean = "rm -rf {}".format(tmp_dir)

    os.system(cmd_tar)

    try:
        yield tmp_dir
    finally:       
        os.system(cmd_clean)


import multiprocessing
P = multiprocessing.Pool()

def serialize(f_repo):

    print "Starting", f_repo

    with process_repo(f_repo) as tmp_dir:

        #ITR = itertools.imap(tokenize, iter_repo(tmp_dir))
        ITR = P.imap(tokenize, iter_repo(tmp_dir))

        for result in ITR:
            yield result

def prep_serialize_for_insert(items):
    (language, f_code, md5, tokens) = items
    time = datetime.datetime.now()
    code_db.get_language_id(language)
    print f_code, language, time


all_tokens = collections.Counter()
ITR = itertools.imap(serialize, F_REPO)

for f_repo in F_REPO[:5]:
    for items in serialize(f_repo):
        prep_serialize_for_insert(items)
        #all_tokens.update(tokens)

exit()

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

