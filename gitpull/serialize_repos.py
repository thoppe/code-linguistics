import glob, json, sqlite3, os, json, string, hashlib, datetime, codecs
import tempfile, collections, contextlib, itertools
import src.minify_code as mini, src.code_db as code_db
from src.code_detection import determine_language
import logging
import glob2 # Recursive globber

use_multicore = True

F_REPO = glob2.glob("repos/**/*.gz")

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)

code_cleaners = collections.defaultdict(list, mini.code_cleaners)

def open_code_file(language, f_code):

    # Assume utf-8 code encoding, not perfect but better than ASCII
    try:
        with codecs.open(f_code, "r", "utf-8") as FIN: 
            raw = FIN.read().encode('utf-8')
    except:
        raw = ""

    data = determine_language(f_code)

    # if a language is determined use that instead of the one from the extension
    if not data["language"]:
        data["language"] = language

    for func in code_cleaners[language]:
        func(raw)
        try:
            raw = func(raw)
        except Exception as ex:
            msg = "Function {} failed for {}, skipping"
            vals = func,f_code
            logging.warning(msg.format(*vals))
            raw = ""

    data["code"] = raw
    data["f_code"] = f_code
    
    return data



def iter_repo(folder=None):
    if folder is None:
        folder = os.getcwd()

    all_files = glob2.glob("{}/**/*".format(folder))
    all_files_ext = ['.'+f.split('.')[-1][:15] for f in all_files]

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

def serialize((language, f_code)):
    data = open_code_file(language, f_code)
    data["md5"] = hashlib.md5(data["code"]).hexdigest()
    return data 

if use_multicore:    
    import multiprocessing
    P = multiprocessing.Pool()

def serialize_file(f_repo):

    print "Starting", f_repo

    with process_repo(f_repo) as tmp_dir:

        if use_multicore:
            ITR = P.imap(serialize, iter_repo(tmp_dir))
        else:
            ITR = itertools.imap(serialize, iter_repo(tmp_dir))

        for result in ITR:
            yield result

def insert_into_database(data):

    time = datetime.datetime.now()
    lang_id = code_db.get_language_id(data["language"])
    md5 = data["md5"]

    # don't add a code that already matches the db
    if code_db.is_new_code(md5):

        project_dir = data["f_code"].split('/')[3]
        owner = project_dir.split('-')[0]
        name = '-'.join(project_dir.split('-')[1:-1])
        project_id = code_db.get_project_id(owner,name)

        # Convert code to binary object
        bin_code = sqlite3.Binary(data["code"])

        # LOC is lines of code
        LOC = data["source_lines_of_code"]

        vals = (md5, lang_id, project_id, bin_code, time, LOC)
        code_db.add_code_item(vals)



for f_repo in F_REPO[:50]:

    _,owner,name = f_repo.split('/')
    name = name.replace('.tar.gz','')

    if code_db.is_new_project(owner,name):
        for items in serialize_file(f_repo):
            insert_into_database(items)

        code_db.commit()


