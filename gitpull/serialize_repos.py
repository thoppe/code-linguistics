import glob, json, sqlite3, os, json, string, hashlib, datetime, codecs
import tempfile, collections, contextlib, itertools
import src.code_db as code_db
import logging
import glob2 # Recursive globber
import multiprocessing

use_multicore = True

# Load the extensions
with open("filetypes/extensions.json") as FIN:
    extensions = json.load(FIN)
extension_lookup = {}
for lang in extensions:
    for ex in extensions[lang]:
        extension_lookup[ex] = lang

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
        "extension": f_ext,
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

        vals = (data["md5"], lang_id, project_id, 
                bin_code, time, data["extension"])

        code_db.add_code_item(vals)

def serialize(data):
    # This used to do more, now it simply passes through
    return data 

def serialize_repo(f_repo):
    data = []

    with process_repo(f_repo) as tmp_dir:
        for f_code in iter_repo(tmp_dir):
            item = serialize(f_code)
            data.append(item)

    return data

def unserialized_ITR():
    F_REPO = glob2.glob("repos/**/*.gz")
    NEW_REPO = []
    for f_repo in F_REPO:
        _,owner,name = f_repo.split('/')
        name = name.replace('.tar.gz','')
        if code_db.is_new_project(owner,name):
            NEW_REPO.append(f_repo)
    for f_repo in NEW_REPO:
        print "Starting repo", f_repo
        yield f_repo

if use_multicore:
    P = multiprocessing.Pool()
    ITR = P.imap(serialize_repo, unserialized_ITR(),chunksize=20)
else:
    ITR = itertools.imap(serialize_repo, unserialized_ITR())

for counter, result in enumerate(ITR):
    #print "Saving {} items".format(len(result))
    for item in result:
        insert_into_database(item)

    if counter%500 == 0:
        code_db.commit()
code_db.commit()
    


