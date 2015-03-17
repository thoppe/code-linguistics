import numpy as np
import sqlite3
from scipy.optimize import fmin, minimize
import scipy.special
import scipy.stats
import mpmath
mpmath.dps = 15

python_keywords = [
    'and', 'as', 'assert', 'break', 'class', 'continue', 
    'def', 'del', 'elif', 'else', 'except', 'exec', 'finally', 
    'for', 'from', 'global', 'if', 'import', 'in', 'is', 
    'lambda', 'not', 'or', 'pass', 'print', 'raise', 'return', 
    'try', 'while', 'with', 'yield']

cpp_keywords = [
    'auto','const','double','float','int','short','struct','unsigned',
    'break','continue','else','for','long','signed','switch','void',
    'case','default','enum','goto','register','sizeof','typedef','volatile',
    'char','do','extern','if','return','static','union','while',
    'asm','dynamic_cast','namespace','reinterpret_cast','try',
    'bool','explicit','new','static_cast','typeid',
    'catch','false','operator','template','typename',
    'class','friend','private','this','using',
    'const_cast','inline','public','throw','virtual',
    'delete','mutable','protected','true','wchar_t']

# ECMA 5.1
javascript_keywords = [
    'do','if','in','for','let','new','try','var','case','else','enum','eval',
    'null','this','true','void','with','break','catch','class','const','false',
    'super','throw','while','yield','delete','export','import','public',
    'return','static','switch','typeof','default','extends','finally',
    'package','private','continue','debugger','function','arguments',
    'interface','protected','implements','instanceof']

def measure_keywords(language, keywords):
    print language
    f_conn = "db_tokens/{}.db".format(language)
    conn = sqlite3.connect(f_conn)

    print "Total keywords", len(keywords)
    cmd_grab = '''SELECT count,name FROM tokens'''
    results = [(n,word) for (n,word) in conn.execute(cmd_grab) 
               if word in keywords]
    COUNTS, WORDS = map(np.array,zip(*results))

    idx = np.argsort(COUNTS)[::-1]
    COUNTS = COUNTS[idx]
    WORDS = WORDS[idx]

    for a,b in zip(WORDS,COUNTS):
        print "{:8s} {:10d}".format(a,b)

    FREQ = COUNTS

    # Account for spurious regularity, e.g. remove correlation between
    # x-y values that could happen by chance by pulling the rank and freq
    # from a binomial distribution

    F1 = np.random.binomial(FREQ.astype(np.int64), 0.5)
    F2 = FREQ-F1
    idx  = np.argsort(F2)[::-1]
    FREQ = F1[idx].astype(np.float64)

    # Remove those with no remaining frequency
    low_counts = FREQ<1
    FREQ = FREQ[~low_counts]
    RANK = np.arange(1, len(FREQ)+1)

    # Normalize
    total_FREQ = FREQ.sum()
    FREQ /= total_FREQ

    return RANK, FREQ


import pylab as plt
import seaborn as sns

L = ["c++","javascript","python"]
K = [cpp_keywords,javascript_keywords,python_keywords]

for language, keywords in zip(L,K):
    RANK,FREQ = measure_keywords(language,keywords)
    X = RANK/float(RANK.max())
    plt.loglog(X,FREQ,'o',mew=0,alpha=.80,label=language)

plt.legend(loc="best",fontsize=20)
plt.axis('tight')
plt.savefig('all_keywords.png',bbox_inches="tight")

plt.show()
