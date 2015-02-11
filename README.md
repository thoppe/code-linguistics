# Code Linguistics

The statistical frequency of words in a natural language follows a power-law distribution, known as [Zipfs Law](http://en.wikipedia.org/wiki/Zipf%27s_law#Related_laws).
More specifically, there are three distinct regimes that fit well to power-laws with exponents of `0.5, 1.0, 2.0`.

The goal of this project is to determine if the following observations holds for code.
The dataset will be a large sampling of code hosted on github.
The hypothesis is that the keywords (when restricted to a single language) will give an exponent of 0.5, variables will fit to 1.0 exponent and the comments and everything else will fit to a greater exponent (possibly not 2.0).

#### Authors: [Travis Hoppe](http://thoppe.github.io/), Max Henderson and Derya Meral.

## Roadmap:

+ Get a large sampling of code from github (how do we systematically identify projects on github, is there a list?).
+ Download the dataset and organize into a database.
+ Determine a list of keywords for all languages we are interested in.
+ Compute the word freq for the data.
+ Plot results and interpret.
+ Draft submission for arXiv.