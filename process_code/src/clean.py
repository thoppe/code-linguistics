import src.minify_code as mini

code_cleaners = collections.defaultdict(list, mini.code_cleaners)
data["is_cleaned"] = False

    # Try to clean the code and mark if successful
    raw = data["code"]
    for func in code_cleaners[data["language"]]:
        try:
            raw = func(raw)
            data["is_cleaned"] = True
        except Exception as ex:
            msg = "Function {} failed for {}, skipping"
            vals = func,f_code
            logging.warning(msg.format(*vals))
            raw = ""
    data["code"] = raw
