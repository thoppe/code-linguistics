import tokenize, io
import pyminifier.minification as mini


def listified_tokenizer(source):
    """Tokenizes *source* and returns the tokens as a list of lists."""
    io_obj = io.StringIO(source)
    return [list(a) for a in tokenize.generate_tokens(io_obj.readline)]

class placeholder:
    pass

options = placeholder()
options.tabs = False

with open("tumult.py") as FIN:
    raw = unicode(FIN.read())

tokens = listified_tokenizer(raw)
print len(raw)
small = mini.minify(tokens,options)
print len(small)

