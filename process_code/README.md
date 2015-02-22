### Documenting the code processing

#### Determine the correct language `identify_db.py`

Once the code files have been properly [downloaded and serialized](../gitpull/), each code needs to be correctly tagged with the programming language. For this we use the ruby-gem [linguist](https://github.com/github/linguist), the same one that github uses internally. We pull code files in chunks and apply linguist code detection which also identifies the lines of code. We mark `is_identified` once this has been done.
