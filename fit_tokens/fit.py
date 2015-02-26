import numpy as np
import sqlite3
from scipy.optimize import fmin, minimize
import scipy.special
import scipy.stats
import mpmath
mpmath.dps = 15

#language = "javascript"
language = "python"
f_conn = "db_tokens/{}.db".format(language)
conn = sqlite3.connect(f_conn)

cmd_grab = '''SELECT count FROM tokens'''
COUNTS = np.array([x for (x,) in conn.execute(cmd_grab)],dtype=float)
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

#idx = np.argsort(FREQ)[::-1]
#FREQ = FREQ[idx].astype(np.float64)

RANK = np.arange(1, len(FREQ)+1)

# Normalize
total_FREQ = FREQ.sum()
FREQ /= total_FREQ

class rank_fit_function(object):

    def __init__(self,FREQ,RANK):
        self.FREQ = FREQ.astype(np.float64)
        self.RANK = RANK.astype(np.float64)
        self.px = None

    def F(self):  print "PASS"
    def ln_F(self):  print "PASS"

    def normalization_constant(self,params):
        f = lambda r:self.F(r,params)
        return 1.0/mpmath.sumem(f, [1, mpmath.inf])

    def err_func(self,p):
        C    = self.normalization_constant(p)

        #val = np.log(C)
        #print "NORM constant",C

        val  = (self.FREQ*self.ln_F(self.RANK,p)).sum()
        val += mpmath.log(C)
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
        
class power_law(rank_fit_function):
    def __init__(self,*args):
        super(power_law, self).__init__(*args)
        self.p0 = (1.5,)
    def F(self,r,(alpha,)):
        return r**(-alpha)
    def ln_F(self,r,(alpha,)):
        return -alpha*np.log(r)

class shifted_power_law(rank_fit_function):
    def __init__(self,*args):
        super(shifted_power_law, self).__init__(*args)
        self.p0 = (1.5,2.0)
    def F(self,r,(alpha,beta)):
        return (r+beta)**(-alpha)
    def ln_F(self,r,(alpha,beta)):
        return -alpha*np.log(r+beta)

class exponential_law(rank_fit_function):
    def __init__(self,*args):
        super(exponential_law, self).__init__(*args)

    def optimize(self):
        mu = (RANK*FREQ).sum()/FREQ.sum()
        self.px = [1/mu,]

    def F(self,r,(alpha,)):
        return np.exp(-alpha*r)

class poisson_law(rank_fit_function):
    def __init__(self,*args):
        super(poisson_law, self).__init__(*args)

    def optimize(self):
        mu = (RANK*FREQ).sum()/FREQ.sum()
        self.px = [mu,]

    def F(self,r,(alpha,)):
        return alpha**x/scipy.special.factorial(r)

class yule_simon(rank_fit_function):
    # Does not work for now (why? is norm off?)
    def __init__(self,*args):
        super(yule_simon, self).__init__(*args)
        self.p0 = (1.5,)

    def F(self,r,(alpha,)):
        g = np.frompyfunc(mpmath.gamma, 1, 1)
        return g(r)/g(r+alpha)

    def ln_F(self,r,(alpha,)):
        dg  = np.frompyfunc(mpmath.digamma, 1, 1)
        val = self.F(r,(alpha,))
        return val*(dg(r)-dg(r+alpha))
        #return val*(psi(0,r)-psi(0,r+alpha))

def kolmogorov_smirnov_test(X,Y):
    return np.abs(X-Y).max()

def r_squared(Y,Y2):
    SS_tot = (Y-Y.mean())**2
    SS_res = (Y-Y2)**2
    return 1 - SS_res.sum()/SS_tot.sum()

fit = shifted_power_law(FREQ,RANK)
#fit = power_law(FREQ,RANK)
#fit = yule_simon_law(FREQ,RANK)
#fit = exponential_law(FREQ,RANK)
#fit = poisson_law(FREQ,RANK)

fit.optimize()
Y_FIT = fit.fitted_ranked()
print "Kolmogorov smirnov: ", scipy.stats.ks_2samp(FREQ,Y_FIT)
print "R^2 value: ", r_squared(FREQ,Y_FIT)

import pylab as plt

plt.loglog(RANK,FREQ,'ro',mew=0,alpha=.50)
plt.loglog(RANK,Y_FIT,lw=3,alpha=.50)
plt.ylim(FREQ.min(),0.5)

#fig = plt.figure()
#plt.loglog(RANK,(FREQ-Y_FIT)**2, 'ro')

plt.show()
