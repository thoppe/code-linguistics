# INPROGRESS

import numpy as np
import sqlite3
from scipy.optimize import fmin
import mpmath
mpmath.dps = 15

language = "javascript"
f_conn = "db_tokens/{}.db".format(language)
conn = sqlite3.connect(f_conn)

cmd_grab = '''SELECT count FROM tokens'''
COUNTS = np.array([x for (x,) in conn.execute(cmd_grab)])
FREQ = COUNTS
FREQ = np.sort(FREQ)[::-1]
RANK = np.arange(1, len(FREQ)+1)

def F(r, params):
    alpha,beta = params
    return (r+beta)**(-alpha)


def normalization_constant(F, params):
    f = lambda r:F(r,params)
    return 1.0/mpmath.sumem(f, [1, mpmath.inf])

def err_func(p,X):
    C = normalization_constant(F,p)
    
    print C
    print X
    exit()
    return 1.0

p0 = (alpha,beta) = 3.0,0.0
C = normalization_constant(F,p0)

fmin(err_func, p0,args=(FREQ,))
exit()

import pylab as plt
plt.loglog(X,C*F(X,p0),lw=3,alpha=.50)
plt.loglog(X,C*F(X,p0),'ro',alpha=.50)


plt.show()

print C
exit()


print fmin(min_func, (alpha,beta))
exit()


C = normalization_constant(RANK,F,(alpha,beta))
print C

FIT = F(RANK, (alpha,beta))

import pylab as plt
plt.loglog(RANK, FREQ,'o',lw=0,alpha=.75)
plt.loglog(RANK, FIT ,'r--',alpha=.75)
plt.loglog(RANK, C*FIT ,'b--',alpha=.75)
plt.loglog(RANK, FIT/C ,'g--',alpha=.75)
plt.show()

