# coding=utf-8

import hashlib


def handle(args):
    if args.string is not None:
        data = args.string
    else:
        data = args.file.read()
    if isinstance(data, str):
        data = data.encode()
    print(hashlib.new(args.alg, data).hexdigest())
