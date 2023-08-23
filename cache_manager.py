def get_cache():
    g = globals()
    if "_keyword_search" not in g:
        g["_keyword_search"] = {}

    return g["_keyword_search"]
