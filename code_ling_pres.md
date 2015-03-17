# code-linguistics
_(five minute hack-and-tell version)_

*[Travis Hoppe](http://thoppe.github.io/)*
----------
[https://github.com/thoppe/code-linguistics](https://github.com/thoppe/code-linguistics)

====

# Zipf's Law
!(images/Wikipedia-n-zipf.png)<<height:600px>> remember when I downloaded [wikipedia](https://github.com/thoppe/Colorless-Green-Ideas)?

====
## so I tried to download github...

====+
+ API rate-limit of 5000 requests/hr with [OAuth](https://developer.github.com/v3/oauth/).
+ [Paginated](https://developer.github.com/guides/traversing-with-pagination/) to find ALL public repos _(stopping naturally at this one)_.
+ ID counter was sequential, 18 million ID's.
+ About 12 million public non-forked repos.
+ Requires an [API hit](https://developer.github.com/v3/repos/) to get info on each one...
====+
+ Created a (small) army of AWS clones to hit it up.
+ Stopped when the project cost > 3 lattes (2.5mil).
+ github is _big_ and people are _amazing_...
====+
+ Downloaded top 1000 repos
+ for C++, Python, Javascript
+ serialized by unique md5's
====*
## POWER LAWS EVERYWHERE!
!(images/plot_forks_count.png) <<height:300px>> forks
!(images/plot_stargazers_count.png) <<height:300px>> stars
!(images/plot_subscribers_count.png) <<height:300px>> subscribers
!(images/plot_size.png) <<height:300px>> size
====
## does code follow a power law?

#### what is code?
no _comments_, no _strings_...
only *keywords*, *literals*, *variables* and *constants*.

#### what is a power law?
#$(r+\beta)^{-\alpha}$
[maximum likelihood](http://en.wikipedia.org/wiki/Maximum_likelihood) fit to [generalized exponential](http://en.wikipedia.org/wiki/Zipf%E2%80%93Mandelbrot_law).
====*
## code follows a power law!
!(images/python.png)<<height:250px>> python
!(images/javascript.png)<<height:250px>> javascript
!(images/c++.png)<<height:250px>> c++


Top 20 "words" from Python code:
    1726926, self       647161, 0            543759, def      501404, 1
    474704, if          359567, return       318063, the      287194, import
    283680, in          282158, none         225461, for      197735, a
    197623, a           194436, 2            190769, from     161552, is
    155933, not         140324, name         138828, and      136889, x
====*
### *keywords* only? Not a power law!
!(images/all_keywords.png)<<height:500px>>

    def          543759    if           474704    return       359567    import       287194
    in           283680    for          225461    from         190769    is           161552
    not          155933    and          138828    class        135388    else         112140
    or            95160    assert        84450    print         76666    try           68039
    raise         63663    except        63357    with          50317    elif          49321
    as            45614    pass          39847    while         17380    lambda        16325
    yield         14846    continue      12991    del           12713    break         11999
    finally        6930    global         6523    exec           1881
====
# Consequences & quick thoughts

+ "computational linguistics" $\rightarrow$ "linguistics of computation"
+ Investigate bigrams, trigrams of keywords?
+ Language design, keyword choice?
+ Difference in smaller projects?
+ coder "fingerprints"?
====*

# Thanks you!

<div style="footnote">
Looking for an overpowered scientist turned analyst/developer? Let's talk!<br>*travis.hoppe @ gmail.com*
</div>


