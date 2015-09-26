#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/9/25'

import os
import traceback
import ast
import codecs
import subprocess
import tempfile
from contextlib import contextmanager


@contextmanager
def safe_write(filename):
    path = os.path.dirname(filename)
    fd, tmp = tempfile.mkstemp(suffix='.bak', dir=path)
    try:
        with os.fdopen(fd, 'w') as f:
            yield f
            os.rename(tmp, filename)
    finally:
        try:
            os.unlink(tmp)
        except:
            pass


def del_isolate_def(filename, root_path):
    with codecs.open(filename) as f:
        file_content = f.read()

    ret = []
    module = ast.parse(file_content)
    get_next_line = False
    for i in ast.walk(module):
        if get_next_line:
            if not hasattr(i, 'lineno') or i.lineno < ret[-1][-1]:
                # line_count = sum(1 for _ in open(filename))
                ret[-1].append(1111111111)  # 余下全部删除
                break
            ret[-1].append(i.lineno - 1)
            get_next_line = False
        if isinstance(i, (ast.FunctionDef)):
            ret.append([i.name, i.lineno])
            get_next_line = True
    wait_del_line = []
    FNULL = open(os.devnull, 'w')
    for i in ret:
        cmd = "find {} -name '*.py' -o -name '*.html' -type f | xargs grep -ris {} | wc -l".format(root_path, i[0])
        count = subprocess.Popen(cmd, stderr=FNULL, stdout=subprocess.PIPE, shell=True)
        count = count.stdout.read().strip()
        if count in map(str, range(2)):
            wait_del_line.extend(i[1:])
    return wait_del_line


def signal_file_process(filename, lines):
    if not lines:
        return
    print(filename, lines)
    with codecs.open(filename, 'r', 'utf-8') as r, safe_write(filename) as w:
        section, lines = lines[:2], lines[2:]
        for index, line in enumerate(r, 1):
            if index > section[-1] and len(lines):
                section, lines = lines[:2], lines[2:]
            if section[0] <= index <= section[1]:
                continue
            w.write(line.encode('utf-8'))


def main(rootpath):
    for root, dirs, files in os.walk(rootpath):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith('py') and path != __file__:
                try:
                    lines = del_isolate_def(path, rootpath)
                    signal_file_process(path, lines)
                except:
                    traceback.print_exc()


if __name__ == '__main__':
    main('path')
