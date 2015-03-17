# code-linguistics
_(five minute hack-and-tell version)_

*[Travis Hoppe](http://thoppe.github.io/)*
----------
[https://github.com/thoppe/code-linguistics](https://github.com/thoppe/code-linguistics)

====

# Zipf's Law
!(images/Wikipedia-n-zipf.png)<<height:600px>> remember when I downloaded [wikipedia](https://github.com/thoppe/Colorless-Green-Ideas)?

====
## so i tried to download github...

====+
+ API rate-limit of 5000 requests/hr with OAuth
+ Paginated to find ALL public repos _(stopping naturally at this one)_
+ ID counter was sequential, 18 million ID's
+ About 12 million public non-forked repos...
+ Requires an API hit to get info on each one...
====+
+ Created a (small) army of AWS clones to hit it up
+ Stopped when the project cost > 3 lattes (2.5mil)
+ github is big and people are amazing...
====+
+ Downloaded top 1000 repos
+ for C++, Python, Javascript
====*
## POWER LAWS EVERYWHERE!
!(images/plot_forks_count.png) <<height:300px>> forks
!(images/plot_stargazers_count.png) <<height:300px>> stars
!(images/plot_subscribers_count.png) <<height:300px>> subscribers
!(images/plot_size.png) <<height:300px>> size
====
## does code follow a power law?
no _comments_, no _strings_...

only *keywords*, *literals*, *variables* and *constants*.

#$(r+\beta)^{-\alpha}$
====*
Yes it does!
!(images/python.png)<<height:250px>> python
!(images/javascript.png)<<height:250px>> javascript
!(images/c++.png)<<height:250px>> c++


    1726926, u'self'
    647161, 0
    543759, u'def'
    501404, 1
    474704, u'if'
    359567, u'return'
    318063, u'the'
    287194, u'import'
    283680, u'in'
    282158, u'none'
    225461, u'for'
    197735, u'a'
    197623, u'u'
    194436, 2
    190769, u'from'
    161552, u'is'
    155933, u'not'
    140324, u'name'
    138828, u'and'
    136889, u'x'

