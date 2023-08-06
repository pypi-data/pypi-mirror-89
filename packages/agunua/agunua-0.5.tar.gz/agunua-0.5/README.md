# Agunua

Agunua is a Python library for the development of Gemini clients.

## Installation

You need Python 3 and [PyOpenSSL](https://www.pyopenssl.org/).  You
can install the dependencies with pip `pip3 install agunua`. 

## Usage

```
import Agunua
...
u = Agunua.GeminiUri(url)
print(u)
```

Main attributes of `GeminiUri` objects:
* `network_success`: was retrieved successfully
* `status_code`: if retrieved successfully, the Gemini two-digit
  status code

See `sample-client.py`.

### Command-line client

`agunua` is a simple Gemini command-line client, a bit like
curl. You can just call:

```
agunua YOUR-URL
```

And you will get its content. Interesting options:

* `--insecure`: do not check the certificate
* `--verbose`: more talkative

## Name

Agunua is a melanesian serpent god. Caduceus would have been better
for a Python + Gemini project since there are two snakes on a caduceus
but it was already used.

## License

GPL. See LICENSE.

## Authors

Stéphane Bortzmeyer <stephane+framagit@bortzmeyer.org>.

## Reference site

https://framagit.org/bortzmeyer/agunua/ Use the Gitlab issue tracker to
report bugs or wishes. But you can of course also access it with
gemini at gemini://gemini.bortzmeyer.org/software/agunua/

## Other Gemini clients in Python 

* https://tildegit.org/solderpunk/gemini-demo-1 Very simple but working client
* https://git.carcosa.net/jmcbray/gusmobile/ Good code
* https://git.sr.ht/~fkfd/picross 
* https://github.com/apellis/pygemini No longer maintained


