import pyminifier.minification, pyminifier.token_utils

# Dummy options to allow a call to pyminifier.minification.minify
class __placeholder: pass
__mini_options = __placeholder()
__mini_options.tabs = False

def clean_pycode(raw):
    tokens = pyminifier.token_utils.listified_tokenizer(raw)
    return pyminifier.minification.minify(tokens,__mini_options)

