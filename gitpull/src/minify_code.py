import pyparsing as pyp

class grammar_python_clean():
    def __init__(self):
        # Replaces all string (docstrings and quoted strings) with ''

        long_single_quote = pyp.QuotedString("'''",multiline=True)
        long_double_quote = pyp.QuotedString('"""',multiline=True)

        short_single_quote = pyp.QuotedString("'",multiline=False)
        short_double_quote = pyp.QuotedString('"',multiline=False)

        long_quote  = long_single_quote | long_double_quote
        short_quote = short_single_quote | short_double_quote

        quote = long_quote | short_quote
        quote.setParseAction(lambda : r"''")      

        # Removes all # comments, leaves only the marker,
        # handles shebang properly
        octothorpe   = pyp.Literal("#") 
        bang         = pyp.Literal("!")
        shebang      = octothorpe + bang
        EOL_comment = (~(shebang) + octothorpe + 
                        pyp.SkipTo(pyp.LineEnd()))
        EOL_comment.setParseAction(lambda tokens:"")

        self.grammar = quote | EOL_comment


    def __call__(self, raw):
        cleaned = self.grammar.transformString(raw)
        # Remove blank lines
        return '\n'.join([x for x in cleaned.split('\n') if x.strip()])


clean_pycode = grammar_python_clean()

