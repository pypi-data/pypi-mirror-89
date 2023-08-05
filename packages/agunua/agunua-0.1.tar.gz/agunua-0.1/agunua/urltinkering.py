#!/usr/bin/python3

import urllib.parse

def delete_first_segment(path):
    first_slash = path.find("/")
    if first_slash == -1:
        return (path, "")
    elif first_slash == 0:
        (first, rest) = delete_first_segment(path[1:])
    else:
        first = path[0:first_slash]
        rest = path[first_slash:]
    if not first.startswith("/"):
        first = "/" + first
    return (first, rest)
    
def delete_last_segment(path):
    last_slash = path.rfind("/")
    return path[0:last_slash]

def urlmerge(base, path):
    path_components = urllib.parse.urlparse(path)
    if path_components.scheme != "":
        raise Exception("Not a relative link \"%s\"" % path)
    components = urllib.parse.urlparse(base)
    if components.scheme == "":
        raise Exception("Base is not an absolute URI \"%s\"" % base)
    base_path = components.path
    if base_path == "":
        base_path += "/"
    elif not base_path.endswith("/"):
        last_slash = base_path.rfind("/")
        base_path = base_path[0:last_slash+1] # RFC 3986, section 5.2.3.
    base_query = components.query # We ignore fragments, since they are never sent to the server
    base = "%s://%s" % (components.scheme, components.netloc)
    if not path_components.path.startswith("/"): # If relative path
        path = base_path + path
    # Now, let's follow RFC 3986, section 5.2.4.
    result = ""
    while path != "":
        if path.startswith("./"):
            path = path[2:]
        if path.startswith("../"):
            path = path[3:]
        if path.startswith("/./"):
            path = path[2:]
        if path.startswith("/.") and (len(path) == 2 or path[2] == "/"):
            path = "/" + path[2:]
        if path.startswith("/../"):
            path = path[3:]
            result = delete_last_segment(result)
        if path.startswith("/..") and (len(path) == 3 or path[3] == "/"):
            path = "/" + path[3:]
            result = delete_last_segment(result)
        if path == "." or path == "..":
            path = ""
        (first, path) = delete_first_segment(path)
        result += first
    return "%s%s%s" % (base, result, base_query)

