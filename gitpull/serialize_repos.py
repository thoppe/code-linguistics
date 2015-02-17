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
extension_lookup = {}
for lang in extensions:
    for ex in extensions[lang]:
        extension_lookup[ex] = lang

code_cleaners = collections.defaultdict(list, mini.code_cleaners)

def open_code_file(f_code):
    #print "Starting code file ", f_code

    # Assume utf-8 code encoding, not perfect but better than ASCII
    try:
        with codecs.open(f_code, "r", "utf-8") as FIN: 
            raw = FIN.read().encode('utf-8')
    except:
        raw = ""

    f_ext = '.{}'.format(f_code.split('.')[-1])

    data = {
        "language" : extension_lookup[f_ext],
        "f_code"   : f_code,
        "code"     : raw,
        "md5"      : hashlib.md5(raw).hexdigest()
    }

    return data


def iter_repo(folder=None):
    if folder is None:
        folder = os.getcwd()

    all_files = glob2.glob("{}/**/*".format(folder))
    all_file_data = {}

    # Read in all the raw data first
    for f_code in all_files:
        f_ext = '.{}'.format(f_code.split('.')[-1])
        if f_ext in extension_lookup:
            all_file_data[f_code] = open_code_file(f_code)

    # Check for any previous md5 matches
    for data in all_file_data.values():
        if code_db.is_new_code(data["md5"]):
            yield data

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

def serialize(data):
    data["is_cleaned"] = False
    linguist_data = determine_language(data["f_code"])  

    # if a language is determined use it instead of the one from the extension
    if linguist_data["language"]:
        data["language"] = linguist_data["language"]

    # Use the source lines of code from linguist
    data["source_lines_of_code"] = linguist_data["source_lines_of_code"]

    # Try to clean the code and mark if successful
    raw = data["code"]
    for func in code_cleaners[data["language"]]:
        try:
            raw = func(raw)
            data["is_cleaned"] = True
        except Exception as ex:
            msg = "Function {} failed for {}, skipping"
            vals = func,f_code
            logging.warning(msg.format(*vals))
            raw = ""
    data["code"] = raw

    return data 

if use_multicore:    
    import multiprocessing
    P = multiprocessing.Pool()

def serialize_repo(f_repo):

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

    # don't add a code that already matches the db
    if code_db.is_new_code(data["md5"]):

        project_dir = data["f_code"].split('/')[3]
        owner = project_dir.split('-')[0]
        name = '-'.join(project_dir.split('-')[1:-1])
        project_id = code_db.get_project_id(owner,name)

        # Convert code to binary object
        bin_code = sqlite3.Binary(data["code"])

        # LOC is lines of code
        LOC = data["source_lines_of_code"]

        vals = (data["md5"], lang_id, project_id, bin_code, 
                time, LOC, data["is_cleaned"])

        code_db.add_code_item(vals)



for f_repo in F_REPO[:50]:

    _,owner,name = f_repo.split('/')
    name = name.replace('.tar.gz','')

    if code_db.is_new_project(owner,name):
        for items in serialize_repo(f_repo):
            insert_into_database(items)

        code_db.commit()


