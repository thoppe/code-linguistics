import src.minify_code as mini
code_cleaners = collections.defaultdict(list, mini.code_cleaners)

linguist_data = determine_language(data["f_code"])  

# if a language is determined use it instead of the 
# one from the extension
if linguist_data["language"]:
    data["language"] = linguist_data["language"]

# Use the source lines of code from linguist
data["source_lines_of_code"] = linguist_data["source_lines_of_code"]
