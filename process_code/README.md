### Documenting code processing

#### Determine the correct language, `identify_db.py`

Once the code files have been properly [downloaded and serialized](../gitpull/), each code needs to be correctly tagged with the programming language. For this we use the ruby-gem [linguist](https://github.com/github/linguist), the same one that github uses internally. We pull code files in chunks and apply linguist code detection which also identifies the lines of code. We mark `is_identified` once this has been done.

A report listing the number repos that match a given language:

+ [Info statistics](stats/repo_language_counts.json).
+ [Download statistics](stats/downloaded_language_counts.json).

Plots showing various statistics:
+ [Stargazers](stats/plot_stargazers_count.png).
+ [Subscribers](stats/plot_subscribers_count.png).
+ [Forks](stats/plot_forks_count.png).
+ [Size](stats/plot_size.png).

#### Build the token database, `tokenize_db.py`

For each code file, we [tokenize](http://en.wikipedia.org/wiki/Lexical_analysis#Token) it. To do so, we strip out all comments and strings inside the code. This is a language specific task, and is handled with the code [`src/clean.py`](src/clean.py). Currently we can handle the following languages:

```python
code_cleaners = {
    "python"       : python_like_clean,
    "c"            : c_like_clean,
    "c++"          : c_like_clean,
    "java"         : c_like_clean,
    "javascript"   : c_like_clean,
}
```

As an example, tokenizing the following python line:

```python
a.value = math.pow(my_number, b.value)
```

would result in:

```python
{"a":1, "b":1, "math":1, "value":2, "pow":1, "my_value":1}
```
