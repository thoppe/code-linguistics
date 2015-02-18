# TOKENIZE will go into it's own script eventually, pulling it out
# of serialize ...
#import src.code_db as code_db

def tokenize((language, f_code)):
    
    word_tokens = string.letters + string.digits + ' _\n'

    code = open_code_file(language, f_code)
    md5 = hashlib.md5(code).hexdigest()

    filtered = ''.join([x if x in word_tokens 
                        else ' ' for x in code]).split()

    #keep_words = set(keywords[language]["keywords"] +
    #                 keywords[language]["builtins"])
    #keep_words = set(keywords[language]["keywords"])               
    #tokens = [x for x in filtered if x in keep_words]
    tokens = filtered
    counted_tokens = collections.Counter(tokens) 

    return (language, f_code, md5, code, tokens)


#code_db.add_tokens(tokens)

exit()

# Load the keywords
with open("filetypes/keywords.json") as FIN:
    keywords = json.load(FIN)

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
