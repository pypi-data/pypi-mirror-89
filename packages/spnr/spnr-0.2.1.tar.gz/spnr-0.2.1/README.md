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

#### Examples

Generate a qrcode with the specific string to the stdout:

`$ spnr qr gen -s https://pypi.org/project/spnr` 

to the screen:

`$ spnr qr gen -s https://pypi.org/project/spnr -S` 

to a picture file:

`$ spnr qr gen -s https://pypi.org/project/spnr -o qr.png` 

### scan

```
usage: spnr qr scan [-h] [-c | -s | -f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --camera          scan a qrcode from the camera
  -s, --screen          scan a qrcode from the screen
  -f FILE, --file FILE  scan a qrcode from the picture file
```

#### Examples

Recognize qrcodes from the screen:

`$ spnr qr scan -s` 

from the camera:

`$ spnr qr scan -c`

from a picture file:

`$ spnr qr scan -f path/to/qr.png`

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

### Examples

Print a table from a matrix literal:

`$ spnr table -m "[['Name', 'Age'], ['Alice', 15], ['Bob', 12]]"`

from a csv file:

`$ spnr table -f some.csv`

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

### Examples

Format a json string to indent 4 space:

`$ spnr json -s '{"name": "Alice", "age": 15}' -i 4`

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

### Examples

Hash a string:

`$ spnr hash -s 'Hello World' -a sha256`

Hash a file:

`$ spnr hash -f path/to/somefile -a md5`

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

### Examples

Decode a url:

`$ spnr code -d https%3A//pypi.org/project/spnr -m url`

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

### Examples

Print current time and timestamp:

`$ spnr time`

timestamp to time string:

`$ spnr time -t 3376656000`

time string to timestamp:

`$ spnr time -T '2077-1-1 00:00:00' -f '%Y-%m-%d %H:%M:%S'`
