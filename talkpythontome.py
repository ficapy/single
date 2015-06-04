#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/6/3'

import logging
import codecs
import os
import re
import urllib
import time
import requests
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed
from multiprocessing import Process
from pyquery import PyQuery as pq

# download_url = 'http://www.talkpythontome.com/episodes/download/9/docker-for-the-python-developer.mp3'
# subtitle_url = 'http://www.talkpythontome.com/episodes/transcript/9/docker-for-the-python-developer'

baseurl = 'http://www.talkpythontome.com/episodes/'
url = 'http://www.talkpythontome.com/episodes/all'
html = requests.get(url).text
d = pq(html)
# 使用以下解析中文字符会有bug
# print d('table a').map(lambda i, e: pq(e).text())
# 将所有非字母使用单个-代替，末尾省略
title_list = [re.sub('[^A-Z^a-z]', '-', pq(i).text().lower().strip()) for i in d('table a')][::-1]
title_list = [re.sub('-{2,}', '-', a) for a in title_list]
title_list = [re.sub('-{1,}$', '', a) for a in title_list]


def generate_lrc(url, filename=''):
    filename = filename if filename else url.split('/')[-1]
    for i in range(1, 4):
        html = requests.get(url).text
        if html:
            break
        if i == 3:
            logging.CRITICAL('%s读取失败' % i)
        time.sleep(pow(3, i))
    d = pq(html)
    original = d('.large-content-text p')
    original = [pq(i).text() for i in original if pq(i).text().strip()]
    if not original:
        logging.exception(url)
        return False
    original[0] = u'0:00 ' + original[0]
    with codecs.open(filename + '.lrc', 'wb', 'utf-8') as f:
        f.write('[ti:{}]'.format(filename) + os.linesep)
        flag = -1
        for i in original:
            if re.match(r'^\d{1,2}\:\d{2}', i):
                current = re.findall(r'(^\d{1,2}\:\d{2})', i)[-1].split(':')
                current = int(current[0]) * 60 + int(current[1])
                if current > flag:
                    flag = current
                    if re.match(r'^\d\:\d{2}', i):
                        f.write(re.sub(r'(^\d\:\d{2})', r'[0\1.00]', i) + os.linesep)
                        continue
                    f.write(re.sub(r'(^\d{2}\:\d{2})', r'[\1.00]', i) + os.linesep)
                else:
                    flag += 1
                    current = '{:0>2}'.format(flag / 60) + ':' + '{:0>2}'.format(flag % 60)
                    f.write(re.sub(r'(^\d{1,2}\:\d{2})', r'[%s.00]' % current, i) + os.linesep)


def download(url, filename=''):
    filename = filename if filename else url.split('/')[-1]
    # http://stackoverflow.com/questions/11143767/how-to-make-a-download-with-progress-bar-in-python
    widgets = ['%s: ' % filename, Percentage(), ' ', Bar(marker=RotatingMarker()), ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets)

    def dlprogress(count, blocksize, totalsize):
        if pbar.maxval is None:
            pbar.maxval = totalsize
            pbar.start()

        pbar.update(min(count * blocksize, totalsize))

    try:
        urllib.urlretrieve(url, filename, reporthook=dlprogress)
    except Exception as e:
        logging.exception(e)
    pbar.finish()


def task(title):
    generate_lrc(baseurl + 'transcript/' + str(title_list.index(title)) + '/%s' % title)
    download(baseurl + 'download/' + str(title_list.index(title)) + '/%s' % title + '.mp3')


process_list = []
# 从第四节才有字幕
for i in title_list[3:]:
    p = Process(target=task, args=(i,))
    p.start()
    process_list.append(p)

for i in process_list:
    i.join()
