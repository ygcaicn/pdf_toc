#!/usr/bin/env python
import re
import fitz
import argparse
import logging
import sys
import io
import os


def parserToc(toc_file):
    print('parser toc file...')
    toc = []
    err = 0
    with open(toc_file, 'rt') as f:
        for t in f.readlines():
            if not t.strip():
                continue
            # \tchapter@5
            # \tchapter@-1
            re_t = re.match(r'^(\s*)([\s\S]+)@([-\d]+)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = int(re_t.group(3))
                toc.append([level, name, page])
                continue
            # \tchapter 5
            re_t = re.match(r'^(\s*)([\s\S]+?)(\d+)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = int(re_t.group(3))
                toc.append([level, name, page])
                continue
            re_t = re.match(r'^(\s*)([\s\S]+?)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = -1
                toc.append([level, name, page])
                continue
            print("parser error:{}".format(t))
            err+=1
    print('格式错误：{}'.format(err))
    return err, toc


def formatToC(tocs, file=sys.stdout):
    for i in tocs:
        level = i[0]
        name = i[1]
        page = i[2]
        print('\t' * (level - 1) + "{}@{}".format(name, page), file=file)


def check_level(tocs):
    print('check toc level...')
    err = 0
    ret_toc = []
    s = []
    for t in tocs:
        flag = 0
        if len(s) == 0:
            s.append(t[0])
        elif t[0] == s[-1]:
            ...
        elif t[0] > s[-1]:
            if t[0] - s[-1] == 1:
                s.append(t[0])
            else:
                print("check level error:{}".format(t))
                err+=1
                flag = 1
        elif t[0] < s[-1]:
            s = s[:(t[0] - s[-1])]
        if not flag:
            ret_toc.append(t)
    print('大纲级别错误：{}'.format(err))
    return err, ret_toc


def func_export(args):
    pdf_file = args.pdf_file
    output = sys.stdout
    if args.out != None:
        if args.out == '':
            args.out = pdf_file+'.txt'
            print('output toc to {}'.format(args.out))
        output = open(args.out, 'wt')
    doc = fitz.open(pdf_file)
    tocs = doc.getToC()
    for i in tocs:
        print(i)
    formatToC(tocs, file=output)
    if output != sys.stdout:
        output.close()
    return 0

def func_mount(args):
    pdf_file = args.pdf_file
    toc_file = args.toc
    offset = args.offset
    if toc_file == '':
        toc_file = pdf_file+'.txt'
    err, tocs = parserToc(toc_file)
    err, tocs = check_level(tocs)
    # print(tocs)
    _tocs = []
    for i in tocs:
        if i[2] != -1:
            i[2] += offset-1
        _tocs.append(i)

    doc = fitz.open(pdf_file)
    doc.setToC(tocs, collapse=args.collapse)
    if args.out and args.out!=pdf_file:
        return(doc.save(args.out))
    else:
        ret = doc.save(pdf_file, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        return ret

def func_test(args):
    print('test')

    print(args)

def func_clean(args):
    pdf_file = args.pdf_file
    output = args.pdf_file
    if args.out:
        output = args.out
    doc = fitz.open(pdf_file)
    doc.setToC([])
    doc.save(output, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)

def func_format(args):
    toc_file = args.toc_file
    out = io.StringIO()

    print('parser toc file...')
    err = 0
    with open(toc_file, 'rt+') as f:
        for t in f.readlines():
            if not t.strip():
                continue
            # \tchapter@5
            # \tchapter@-1
            re_t = re.match(r'^(\s*)([\s\S]+)@([-\d]+)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = int(re_t.group(3))
                print('\t' * (level - 1) + "{}@{}".format(name, page))
                print('\t' * (level - 1) + "{}@{}".format(name, page), file=out)
                continue
            # \tchapter 5
            re_t = re.match(r'^(\s*)([\s\S]+?)(\d+)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = int(re_t.group(3))
                print('\t' * (level - 1) + "{}@{}".format(name, page))
                print('\t' * (level - 1) + "{}@{}".format(name, page), file=out)
                continue
            # \tchapter
            re_t = re.match(r'^(\s*)([\s\S]+?)$', t)
            if re_t:
                level = len(re_t.group(1)) + 1
                name = re_t.group(2).strip()
                page = -1
                print('\t' * (level - 1) + "{}@{}".format(name, page))
                print('\t' * (level - 1) + "{}@{}".format(name, page), file=out)
                continue
            print("parser error:{}".format(t))
            print(t, file=out)

            err+=1
        print('格式错误：{}'.format(err))
        if not args.out:
            f.seek(0)
            f.truncate(0)
            f.write(out.getvalue())
        else:
            with open(args.out) as out_file:
                out_file.write(out.getvalue())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True,metavar='sub-command ')
    parser_export = subparsers.add_parser('export', help='export toc of pdf')
    parser_export.add_argument('-o', '--out', nargs='?', const='', help='output to file')
    parser_export.add_argument('pdf_file', help='pdf file')
    parser_export.set_defaults(func=func_export)

    parser_mount = subparsers.add_parser('mount', help='mount toc to pdf')
    parser_mount.add_argument('-o', '--out', help='output to file')
    parser_mount.add_argument('-i', '--offset', type=int, default=0, help='offset page num')
    parser_mount.add_argument('-t', '--toc', default='', help='mount the toc to pdf file')
    parser_mount.add_argument('-c', '--collapse', type=int, default=1, help='controls the hierarchy level, to completely expand specify either a large integer, 0 or None')
    parser_mount.add_argument('pdf_file', help='pdf file')
    parser_mount.set_defaults(func=func_mount)

    parser_test = subparsers.add_parser('test', help='test toc file')
    parser_test.add_argument('toc_file', help='toc file')
    parser_test.set_defaults(func=func_test)

    parser_format = subparsers.add_parser('format', help='test toc file')
    parser_format.add_argument('-o', '--out', help='output to file')

    parser_format.add_argument('toc_file', help='toc file')
    parser_format.set_defaults(func=func_format)

    parser_clear = subparsers.add_parser('clean', help='clean toc')
    parser_clear.add_argument('-o', '--out', help='output to file')
    parser_clear.add_argument('pdf_file', help='pdf file')
    parser_clear.set_defaults(func=func_clean)

    args = parser.parse_args()
    args.func(args)
