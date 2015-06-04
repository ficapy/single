#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/6/3'
import logging
import codecs
import os

from pyquery import PyQuery as pq
import re
import requests
import urllib
import time

# url = 'http://www.talkpythontome.com/episodes/all'
# html = requests.get(url).text
# d = pq(html)
# #使用以下解析中文字符会有bug
# # print d('table a').map(lambda i, e: pq(e).text())
# title_list =  [pq(i).text() for i in d('table a')]

crawl_list = 'http://www.talkpythontome.com/episodes/transcript/9/docker-for-the-python-developer'

def generate_lrc(url,filename):
    assert isinstance(filename,str)
    filename = filename.replace(' ','_').replace('-','_')
    for i in range(1,4):
        html = requests.get(url).text
        if html:
            break
        if i ==3:
            logging.CRITICAL('%s读取失败'%i)
        time.sleep(pow(3,i))
    d = pq(u'0:00 '+ html) #因为原文没有加0
    original =  d('.large-content-text p')
    original = [pq(i).text() for i in original if pq(i).text().strip()]
    original[0] = u'0:00 ' + original[0]
    with codecs.open(filename+'.lrc','wb','utf-8') as f:
        f.write('[ti:{}]'.format(filename) + os.linesep)
        for i in original:
            f.write(re.sub(r'(\d{1,2}\:\d{2})',r'[\1]',i) + os.linesep)

generate_lrc(crawl_list,'docker-for-the-python-developer')

requests.get(crawl_list,)
