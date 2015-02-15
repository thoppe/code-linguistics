import tokenize, io
import pyminifier.minification, pyminifier.token_utils

def listified_tokenizer(source):
    """Tokenizes *source* and returns the tokens as a list of lists."""
    io_obj = io.StringIO(source)
    return [list(a) for a in tokenize.generate_tokens(io_obj.readline)]

# Dummy options to allow a call to pyminifier.minification.minify
class __placeholder: pass
__mini_options = __placeholder()
__mini_options.tabs = False

def clean_pycode(raw):
    tokens = pyminifier.token_utils.listified_tokenizer(raw)
    return pyminifier.minification.minify(tokens,__mini_options)

with open("tumult.py") as FIN:
    raw = unicode(FIN.read())
    small = clean_pycode(raw)
    print len(raw), len(small)



