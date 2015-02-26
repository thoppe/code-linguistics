import numpy as np
import sqlite3
from scipy.optimize import fmin, minimize
import scipy.special
import mpmath
mpmath.dps = 15

language = "javascript"
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


fit = shifted_power_law(FREQ,RANK)
#fit = power_law(FREQ,RANK)
#fit = yule_simon_law(FREQ,RANK)
#fit = exponential_law(FREQ,RANK)
#fit = poisson_law(FREQ,RANK)

fit.optimize()

import pylab as plt

Y_FIT = fit.fitted_ranked()
print Y_FIT
plt.loglog(RANK,Y_FIT,lw=3,alpha=.50)
plt.loglog(RANK,FREQ,'ro',mew=0,alpha=.50)

plt.ylim(FREQ.min(),1)
plt.show()
