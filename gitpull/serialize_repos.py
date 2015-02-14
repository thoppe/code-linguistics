import glob, json, sqlite3, os, json, string, hashlib, time
import tempfile, collections
import glob2 # Recursive globber

F_REPO = glob2.glob("repos/**/*.gz")

def process_repo(f_repo):
    org_d = os.getcwd()
    f_full_repo = os.path.abspath(f_repo)

    d = tempfile.mkdtemp()
    os.chdir(d)

    cmd_tar = "tar -xvf {}".format(f_full_repo, d)
    print cmd_tar
    os.system(cmd_tar)
   
    #os.system("bash")
    os.chdir(org_d)
    os.system("rm -rf {}".format(d))


f = F_REPO[200]
for f in F_REPO:
    print f
    process_repo(f)

#for language, f_code in iter_repo(folder):
#    md5, tokens = tokenize(f_code)
#    print md5, tokens

'''
def iter_repo(folder):
    all_files = glob2.glob("{}/**/*".format(folder))
    all_files_ext = ['.'+f.split('.')[-1][:10] for f in all_files]

    for language in extensions:
        for ext in extensions[language]:
            for f,f_ext in zip(all_files,all_files_ext):
                if f_ext == ext:
                    yield (language, f)


token_words = set(string.letters + string.digits + '_ \n')
MAX_TOKEN_SIZE = 20

def tokenize(f_code):

    with open(f_code) as FIN: 
        raw = FIN.read()

    md5 = hashlib.md5(raw).hexdigest()

    filtered = ''.join([x if x in token_words 
                        else ' ' for x in raw]).split()
    adjusted = [x.lower() for x in filtered if len(x)<20]
    tokens = collections.Counter(adjusted) 

    return md5,tokens
'''     

