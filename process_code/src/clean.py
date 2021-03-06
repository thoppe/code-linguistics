import pyparsing as pyp

class generic_code_cleaner(object):
    def __call__(self, raw):
        cleaned = self.grammar.transformString(raw)
        # Remove blank lines
        return '\n'.join([x for x in cleaned.split('\n') if x.strip()])
    
class grammar_python_clean(generic_code_cleaner):
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

class grammar_c_clean(generic_code_cleaner):
    def __init__(self):
        # Replaces all string (docstrings and quoted strings) with ''

        block_quote = pyp.QuotedString("/*", endQuoteChar="*/", 
                                       multiline=True)
        block_quote.setParseAction(lambda:"")

        # C-files can have quotes that span multilines
        short_single_quote = pyp.QuotedString("'",multiline=True)
        short_double_quote = pyp.QuotedString('"',multiline=True)
        short_quote = short_single_quote | short_double_quote

        quote = block_quote | short_quote
        short_quote.setParseAction(lambda : r'""')      

        # Removes all # comments, leaves only the marker,
        # handles shebang properly
        double_slash   = pyp.Literal("//")         
        EOL_comment = (double_slash + pyp.SkipTo(pyp.LineEnd()))
        EOL_comment.setParseAction(lambda tokens:"")
        self.grammar = quote | EOL_comment


test_py = """
from time import localtime

''' long multiline 
comment '''

activities = {8: 'Sleeping',
              9: 'Commuting',
              17: 'Working',
              18: 'Commuting',
              20: 'Eating',
              22: 'Resting' }

time_now = localtime()
hour = time_now.tm_hour

for activity_time in sorted(activities.keys()):
    if hour < activity_time:
        print activities[activity_time]
        break
else:
    print 'Unknown, AFK or sleeping!'
"""

test_cpp = '''
// Sample program
/* long 
multiline
comment */

#include <iostream.h>

void main()
{
  int length, width;
  int perimeter, area;              // declarations
  cout <<  "Length = ";             // prompt user
  cin >> length;                    // enter length
  cout << "Width = ";               // prompt user
  cin >> width;                     // input width
  perimeter = 2*(length+width);     // compute perimeter
  area = length*width;              // compute area
  cout << endl
       << "Perimeter is " << perimeter;
  cout << endl
       << "Area is " << area
       << endl;                    // output results
} // end of main program
'''

python_like_clean = grammar_python_clean()
c_like_clean      = grammar_c_clean()

# Java/Javascript uses /*...*/ and // ... for comments, we can reuse C-code

code_cleaners = {
    "python"       : python_like_clean,
    "c"            : c_like_clean,
    "c++"          : c_like_clean,
    "java"         : c_like_clean,
    "javascript"   : c_like_clean,
}

if __name__ == "__main__":
    print code_cleaners["python"](test_py)
    print code_cleaners["c++"](test_cpp)


'''
code_cleaners = collections.defaultdict(list, mini.code_cleaners)
data["is_cleaned"] = False

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
'''
