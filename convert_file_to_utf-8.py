#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/7/16'

# FUCK YOU GB2312

import codecs
import os
import shutil
from chardet.universaldetector import UniversalDetector
from os import path

dir = path.dirname(path.abspath(__file__))
detector = UniversalDetector()

for root, dirnames, files in os.walk(dir):
    for file in files:
        detector.reset()
        filepath = path.join(root, file)
        for line in open(filepath, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        encode = detector.result.get('encoding')

        utf8path = path.dirname(filepath.replace(dir, path.join(dir, 'utf-8')))
        # 适用于py3,懒得兼容2了
        os.makedirs(utf8path, exist_ok=True)
        dst = path.join(utf8path, file)

        # http://stackoverflow.com/questions/191359/how-to-convert-a-file-to-utf-8-in-python
        BLOCKSIZE = 1048576  # or some other, desired size in bytes
        if encode:
            with codecs.open(filepath, "r", encode) as sourceFile:
                with codecs.open(dst, "w", "utf-8") as targetFile:
                    while True:
                        contents = sourceFile.read(BLOCKSIZE)
                        if not contents:
                            break
                        targetFile.write(contents)
                        # 日了狗了🐶，osx上自带iconv不支持-o参数
                        # subprocess.call(['iconv', '-f', encode, '-t', 'UTF-8', filepath, '-o', dst],stdout=subprocess.DEVNULL)
        else:
            shutil.copyfile(filepath, dst)