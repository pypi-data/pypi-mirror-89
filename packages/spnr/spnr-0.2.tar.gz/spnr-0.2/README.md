# Spanner

[![PyPI](https://img.shields.io/pypi/v/spnr.svg)](https://pypi.org/project/spnr)

A command line toolset.

## qr

### generate

```
usage: spnr qr generate [-h] [-s STRING | -f [FILE]] [-S | -o [OUTPUT_FILE]]

optional arguments:
  -h, --help            show this help message and exit
  -s STRING, --string STRING
                        content
  -f [FILE], --file [FILE]
                        read content from the file, default stdin
  -S, --screen          show the qrcode on the screen
  -o [OUTPUT_FILE], --output-file [OUTPUT_FILE]
                        output qrcode to a file, default stdout
```

### scan

```
usage: spnr qr scan [-h] [-c | -s | -f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --camera          scan a qrcode from the camera
  -s, --screen          scan a qrcode from the screen
  -f FILE, --file FILE  scan a qrcode from the picture file
```

## table

```
usage: spnr table [-h] [-m MATRIX | -f [FILE]] [--row-span {head,none,all}]

optional arguments:
  -h, --help            show this help message and exit
  -m MATRIX, --matrix MATRIX
                        a matrix literal
  -f [FILE], --file [FILE]
                        read a matrix literal or csv from the file, default stdin
  --row-span {head,none,all}
                        row span mode
```

## json

```
usage: spnr json [-h] [-s STRING | -f [FILE]] [-i INDENT]

optional arguments:
  -h, --help            show this help message and exit
  -s STRING, --string STRING
                        a json string
  -f [FILE], --file [FILE]
                        read the json from a file, default stdin
  -i INDENT, --indent INDENT
                        indent
```

## hash

```
usage: spnr hash [-h] [-s STRING | -f [FILE]] -a ALG

optional arguments:
  -h, --help            show this help message and exit
  -s STRING, --string STRING
                        hash a string
  -f [FILE], --file [FILE]
                        hash a file, default stdin
  -a ALG, --alg ALG     hash algorithm
```

## code

```
usage: spnr code [-h] (-e ENCODE | -d DECODE) -m {base64,url}

optional arguments:
  -h, --help            show this help message and exit
  -e ENCODE, --encode ENCODE
                        encode a string
  -d DECODE, --decode DECODE
                        decode a string
  -m {base64,url}, --mode {base64,url}
                        code mode
```

## time

```
usage: spnr time [-h] [-t TIMESTAMP | -T TIME] [-f FORMAT] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -t TIMESTAMP, --timestamp TIMESTAMP
                        timestamp
  -T TIME, --time TIME  time in string
  -f FORMAT, --format FORMAT
                        time format
  -u, --utc             use utc time
```
