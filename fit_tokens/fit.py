import numpy as np
import sqlite3
from scipy.optimize import fmin, minimize
import mpmath
mpmath.dps = 15

language = "java"
#language = "python"
f_conn = "db_tokens/{}.db".format(language)
conn = sqlite3.connect(f_conn)

cmd_grab = '''SELECT count FROM tokens'''
COUNTS = np.array([x for (x,) in conn.execute(cmd_grab)],dtype=float)
FREQ = COUNTS
FREQ = np.sort(FREQ)[::-1]
RANK = np.arange(1, len(FREQ)+1)

total_FREQ = FREQ.sum()
FREQ /= total_FREQ

class rank_fit_function(object):

    def __init__(self,FREQ,RANK):
        self.FREQ = FREQ
        self.RANK = RANK
        self.px = None

    def normalization_constant(self,params):
        f = lambda r:self.F(r,params)
        return 1.0/mpmath.sumem(f, [1, mpmath.inf])

    def err_func(self,p):
        C = self.normalization_constant(p)
        val  = mpmath.log(C)
        val += (self.FREQ*self.ln_F(self.RANK,p)).sum()
        val *= -1
        print p, val
        return val

    def optimize(self):

        self.result = minimize(self.err_func, 
                               self.p0,
                               method="Nelder-Mead")
        self.px = self.result.x
        return self.px

    def fitted_ranked(self):
        assert(self.px is not None)

        Y_FIT = self.F(self.RANK, self.px)
        Y_FIT /= Y_FIT.sum()
        return Y_FIT
        

def fit_factory(FREQ, RANK, F=None, ln_F=None, p0=None):
    fit = rank_fit_function(FREQ,RANK)
    fit.F = F
    fit.ln_F = ln_F
    fit.p0 = p0
    return fit


power_law = {"F"   : lambda r,p:r**(-p[0]),
             "ln_F": lambda r,p:-p[0]*np.log(r),
             "p0"  : (1.5,)}

shifted_power_law = {"F"   : lambda r,p:(r+p[1])**(-p[0]),
                     "ln_F": lambda r,p:-p[0]*np.log(r+p[1]),
                     "p0"  : (1.5,2.0)}

#fit = fit_factory(FREQ,RANK,**power_law)
fit = fit_factory(FREQ,RANK,**shifted_power_law)
fit.optimize()

import pylab as plt

Y_FIT = fit.fitted_ranked()
plt.loglog(RANK,Y_FIT,lw=3,alpha=.50)
plt.loglog(RANK,FREQ,'ro',mew=0,alpha=.50)
plt.show()
