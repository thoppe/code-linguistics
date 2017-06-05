# Code Linguistics

The statistical frequency of words in a natural language follows a power-law distribution, known as [Zipfs Law](http://en.wikipedia.org/wiki/Zipf%27s_law#Related_laws).
More specifically, there are three distinct regimes that fit well to power-laws with exponents of `0.5, 1.0, 2.0`.

The goal of this project is to determine if the following observations holds for code.
The dataset will be a large sampling of code hosted on github.
The hypothesis is that the keywords (when restricted to a single language) will give an exponent of 0.5, variables will fit to 1.0 exponent and the comments and everything else will fit to a greater exponent (possibly not 2.0).

#### Author: [Travis Hoppe](http://thoppe.github.io/)

## Roadmap:

+ Download a large sampling of code from github. [Completed](gitpull/).
+ Process, filter and tokenize the dataset. [Completed](process_code/).
+ Fit the proper power laws values to the data. [In-progress](fit_tokens/)
+ Determine a list of keywords for all languages we are interested in.
+ Plot results and interpret.
+ Draft submission for arXiv.

## Presentations

+ [DC Hack and Tell Round 18: Ternary Bits](http://www.meetup.com/DC-Hack-and-Tell/events/220231708/), March 17, 2015, [presentation link](http://thoppe.github.io/code-linguistics/HnC_presentation.html).

## References
  
+  Power-law distributions in empirical data, [arXiv:0706.1062](https://arxiv.org/abs/0706.1062)
+  Similarity of symbol frequency distributions with heavy tails, [arXiv:1510.00277](http://arxiv.org/abs/1510.00277)
+  Power laws in software, [ACM Trans. on Software Engineering and Methodology, Vol 18:1, Sept 2008](http://dl.acm.org/citation.cfm?id=1391986)
