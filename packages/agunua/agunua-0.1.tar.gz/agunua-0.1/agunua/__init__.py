#!/usr/bin/env python3

import urllib.parse
import socket
import re
import sys
import codecs
import cgi
import datetime

# https://www.pyopenssl.org/ Python standard library has the "ssl"
# module but PyOpenSSL offers more features.
import OpenSSL

from agunua.urltinkering import urlmerge

# Things you shouldn't touch
VERSION = "0.1"
GEMINI_PORT = 1965
BUFSIZE = 4096

# In uppercase, the defaults. Most can be changed when calling the constructor.
INSECURE = False
MAXSIZE = 2**20
MAXLINES = 1000
MAXDEPTH = 4 # Max redirections
FOLLOW_REDIRECT = False
DEBUG = False
IDN = True

def readline(s):
    """ Returns a triple (line_read, rest_of_the_data, eof) """
    nextline = 0
    for char in s:
        nextline += 1
        if char == "\r" and s[nextline] == "\n":
            l = s[0:nextline-1]
            return (l, s[nextline+1:], False)
        if char == "\n":
            l = s[0:nextline-1]
            return (l, s[nextline:], False)            
    return (s, None, True)

def parse(content, url=None):
    """Parse a gemtext (Gemini usual format) content and returns an array
of the links it contains. If url is None, we dont' handle relative
links, and ignore them. """
    linenum = 0
    rest = content
    result = []
    components = urllib.parse.urlparse(url)
    while linenum < MAXLINES:
        (l, rest, eof) = readline(rest)
        linenum += 1
        if eof:
            break
        if l[0:2] == "=>":
            l = re.sub("^\s*", "", l[2:]) # Strip leading spaces. Note
                                          # the standard says there is
                                          # at least one space ("any
                                          # non-zero number of
                                          # consecutive spaces or
                                          # tabs") but this is not
                                          # what we see in the wild.
            s = re.split("[ \t]+", l, maxsplit=1)
            if len(s) == 2:
                (link, text) = s
            else:
                link = s[0] # Link without a text
            components_link = urllib.parse.urlparse(link)
            if components_link.scheme == "": # Relative link
                if url is not None:
                    # Unfortunately, Python's standard library's
                    # urllib.parse.urljoin does not work with non-HTTP
                    # URIs :-( So we have to do that ourselves. There
                    # is an interesting trick in
                    # <https://tildegit.org/solderpunk/gemini-demo-1>
                    # (replace gemini with http, join and replace
                    # back) but we preferred to reimplement.
                    result.append(urlmerge(url, link))
            elif components_link.scheme == "gemini": 
                result.append(link)
            # Else ignore
    return result

class GeminiUri():
    
    def __init__(self, url, insecure=INSECURE, get_content=False,
                 parse_content=False, follow_redirect=FOLLOW_REDIRECT,
                 idn=IDN, redirect_depth=0, debug=DEBUG):
        """Note it does not enforce robots.txt. The caller has to do it.

        WARNING: there is no timeout, so you risk being blocked for
        ever, for instance if the server is nasty and accepts
        connections but then never writes anything. The caller has to
        handle this, using alarm signals or stuff like that. An
        example is in the command-line client,
        agunua.py. (Implementing a timeout with PyOpenSSL is *hard*,
        see <https://github.com/pyca/pyopenssl/issues/168>.)

        """
        self.url = url
        self.insecure = insecure
        self.network_success = False
        self.ip_address = None
        self.status_code = None
        self.meta = None
        self.links = None # An array. If empty, means there was no
                          # links. If None, means the file was not
                          # gemtext, or was not parsed.
        self.error = "No error"
        self.payload = None
        do_idn = False
        try:
            components = urllib.parse.urlparse(url)
        except ValueError: # Invalid URL 
            self.error = "Invalid URL"
            return   
        if components.scheme != 'gemini':
            self.error = "Ignoring non-Gemini URL"
            return 
        host = components.hostname
        if idn:
            a_host = codecs.encode(host, encoding="idna").decode()
            if a_host != host:
                do_idn = True
            else:
                a_host = host
        try:
            port = components.port
        except ValueError: # I've seen strange things.
            self.error = "Invalid port in URL"
            return 
        if port is None:
            port = GEMINI_PORT
        if port != GEMINI_PORT:
            tport = ":%s" % port
        else:
            tport = ""
        if components.query != "":
            query = "?%s" % components.query
        else:
            query = ""
        if parse_content:
            get_content = True
        try:
            addrinfo_list = socket.getaddrinfo(host, port)
        except socket.gaierror:
            self.error = "Name %s not known or invalid" % host
            return 
        addrinfo_set = { (addrinfo[4], addrinfo[0]) for addrinfo in addrinfo_list }
        data = ""
        for (addr, family) in addrinfo_set:
            sock = socket.socket(family, socket.SOCK_STREAM)
            context = OpenSSL.SSL.Context(OpenSSL.SSL.TLSv1_2_METHOD)
            if self.insecure: 
                # Many Gemini capsules have only a self-signed certificate
                context.set_verify(OpenSSL.SSL.VERIFY_NONE, lambda *x: True)
            else:
                context.set_default_verify_paths()
                context.set_verify(OpenSSL.SSL.VERIFY_PEER | OpenSSL.SSL.VERIFY_FAIL_IF_NO_PEER_CERT | \
                               OpenSSL.SSL.VERIFY_CLIENT_ONCE,
                                   lambda conn, cert, errno, depth, preverify_ok: preverify_ok)
            session = OpenSSL.SSL.Connection(context, sock)
            session.set_tlsext_host_name(a_host.encode()) # Server Name Indication (SNI)
            try:
                if debug:
                    print("DEBUG: trying to connect to %s ..." % str(addr))
                try:
                    session.connect(addr)
                except OSError as e:
                    self.error = "Cannot connect to host %s: %s" % (addr, e)
                    if debug:
                        print("DEBUG: failed: %s" % self.error)
                    continue
                try:
                    sock.setblocking(True) # Long-standing issue https://github.com/pyca/pyopenssl/issues/168
                    session.do_handshake() 
                except OpenSSL.SSL.Error as e:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    self.error = "TLS handshake error %s: problem in the certificate? \"%s\"" % (exc_type, exc_value)
                    if debug:
                        print("DEBUG: failed: %s" % self.error)
                    continue
                cert = session.get_peer_certificate()
                request = "gemini://" + a_host + tport + components.path + query + "\r\n" # We
                # do not send the fragment to the server
                session.send(request.encode())
                data = ""
                while True:
                    try:
                        response = session.recv(BUFSIZE) # Or create a
                        # file object with session.makefile("rb"), to be
                        # able to use readline()?
                        try:
                            data += response.decode()
                        except UnicodeDecodeError: # Not UTF-8. TODO
    #            We should honor the charset (parsed later) but, in the
    #            mean time, we give in.
                            break
                        if len(data) > MAXSIZE: # Protection against very huge files
                            break
                    # The Gemini protocol has no equivalent of HTTP
                    # Content-Length
                    # <https://gemini.circumlunar.space/docs/faq.html> or
                    # EPP or DNS explicit lengths. The only way to read
                    # everything is to go until EOF exception.
                    except (OpenSSL.SSL.SysCallError, OpenSSL.SSL.ZeroReturnError): # TODO check if SysCallError is really EOF
                        break
                body_start = 0
                (header, rest, eof) = readline(data)
                if eof:
                    self.error = "No header line"
                    continue
                self.status_code = header[0:2]
                self.meta = header[3:]
                if self.status_code == "20":
                    mtype, mime_opts = cgi.parse_header(self.meta)
                    self.mediatype = mtype
                    self.lang = ""
                    self.charset = ""
                    for key in mime_opts:                                                                       
                        if key == "lang":
                            self.lang = mime_opts["lang"].lower()
                        elif key == "charset":                                                                              
                            self.charset = mime_opts["charset"].lower()
                self.payload = rest
                self.network_success = True
                if self.status_code == "30" or self.status_code == "31":
                    if follow_redirect:
                        if redirect_depth <= MAXDEPTH:
                            self.__init__(self.meta,
                                          get_content=get_content,
                                          parse_content=parse_content,
                                          debug=debug,
                                          follow_redirect=follow_redirect,
                                          redirect_depth=redirect_depth+1)
                            return
                        else:
                            self.network_success = False
                            self.error = "Too many redirects"
                elif self.status_code == "20":
                    if parse_content and self.mediatype == "text/gemini":
                        self.links = parse(rest, url)
                session.shutdown()
                session.close()
                break
            except (ConnectionRefusedError, TimeoutError) as e:  # Or "isinstance(err, (TimeoutError, socket.timeout))" ?
                self.error = "%s failed because of \"%s\"" % (addr, e)
                continue # Try another address
        self.ip_address = addr[0]
        if self.network_success:
            self.issuer = str(cert.get_issuer()) # TODO not obvious, but try to find a better way to display it
            self.subject = str(cert.get_subject())
            self.cert_not_after = datetime.datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
            self.cert_not_before = datetime.datetime.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ")
            self.size = len(data)

    def __str__(self):
        if self.network_success:
            return("%s / %s OK: code %s" % (self.url, self.ip_address, self.status_code))
        else:
            return("%s FAIL: \"%s\"" % (self.url, self.error))
