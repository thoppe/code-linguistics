### Documenting power law fits

#### Parameter estimation, `fit.py`

There a couple of interesting points to note when fitting the data.

+ First, we have to correct for any spurious regularity between the frequency and the rank of each word. To do this we split our tokens randomly between a "frequency" and a "rank" data set by drawing from a binomial distribution.
+ We remove any words that now have a zero frequency.
+ We fit the parameters to the distribution by maximizing the likelihood function, specifically we minimize the -log of this.
+ We then compute the [KS](http://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test) test and [R^2](http://en.wikipedia.org/wiki/Coefficient_of_determination) test against the fit and record the results (to do).

#### Types of fit functions

+ [Power law (Zipfs)](http://en.wikipedia.org/wiki/Zipf%27s_law)
+ [Shifted power law (Zipf–Mandelbrot)](http://en.wikipedia.org/wiki/Zipf%E2%80%93Mandelbrot_law)
+ [Discrete exponential](http://en.wikipedia.org/wiki/Exponential_distribution)
+ [Poisson](http://en.wikipedia.org/wiki/Poisson_distribution)
+ [Yule-Simon](http://en.wikipedia.org/wiki/Yule%E2%80%93Simon_distribution) (not working)