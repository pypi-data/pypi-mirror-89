#!/usr/bin/python3

import agunua
import sys

if len(sys.argv) <= 1:
    raise Exception("Usage: %s url ..." % sys.argv[0])

for url in sys.argv[1:]:
    u = agunua.GeminiUri(url, get_content=True, parse_content=True, insecure=True)
    print(u)
    if u.network_success:
        print("%i bytes" % len(u.payload))
        if u.links is not None and u.links != []:
            print("Links: %s" % u.links)
    print("")
    
