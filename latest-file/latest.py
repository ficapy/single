#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '16/4/24'

import os
import sys
import time
from subprocess import Popen, PIPE
from os import stat, path
from workflow import Workflow


class F(object):
    def __init__(self, path):
        self.path = path

    @property
    def size(self):
        return stat(self.path).st_size

    @property
    def time(self):
        return time.time() - stat(self.path).st_ctime

    @property
    def name(self):
        return path.basename(self.path)


def _filter(file_path):
    # 过滤掉 /Applications和$HOME/Applications和$HOME/Library
    if not path.exists(file_path):
        return True
    home = os.environ['HOME']
    exclude = ['/Applications', path.join(home, 'Applications'), path.join(home, 'Library')]
    for i in exclude:
        if file_path.startswith(i):
            return True
    return False


def _sort(file_queue):
    # 根据文件大小和文件创建日期进行排序
    size = sorted(file_queue, key=lambda x: x.size, reverse=True)
    time = sorted(file_queue, key=lambda x: x.time)
    return sorted(file_queue, key=lambda x: size.index(x) + time.index(x))


def main(wf):
    args = wf.args[0] if wf.args else u''
    query = Popen(
        ['/usr/bin/mdfind', u'kMDItemFSName=*{}*&&kMDItemFSContentChangeDate>$time.now(-{})'.format(args, 1800)],
        stdout=PIPE)
    query = query.stdout.read().decode('utf-8').split(u'\n')
    ret = []
    for i in query:
        if _filter(i):
            continue
        ret.append(F(i))
    for i in _sort(ret):
        wf.add_item(i.name, i.path, type='file', copytext=i.path, arg=i.path, valid=True)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))