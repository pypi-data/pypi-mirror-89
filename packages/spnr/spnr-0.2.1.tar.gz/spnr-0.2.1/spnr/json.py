# coding=utf-8

import json


def handle(args):
    if args.string is not None:
        j = args.string
    else:
        j = args.file.read()
    j = json.loads(j)
    print(json.dumps(j, indent=args.indent, ensure_ascii=False))
