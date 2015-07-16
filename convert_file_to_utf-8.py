#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/7/16'

# FUCK YOU GB2312

import os
import shutil
from chardet.universaldetector import UniversalDetector
from subprocess import Popen
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
        os.makedirs(utf8path, exist_ok=True)
        dst = path.join(utf8path, file)

        shutil.copyfile(filepath, dst)
        if encode:
            Popen(['iconv','-f',encode,'-t','UTF-8',filepath,'-o',dst],shell=True)



