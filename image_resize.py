#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/8/10'

# 压缩所有图片至jpg格式,且限制大小,调用convert(imagemagick)


import sys
import os
from shutil import copyfile
from os.path import join, dirname, getsize, split, splitext, abspath


def back_up():
    for root, dirs, files in os.walk(dirname(abspath(__file__))):
        if 'result' in dirs:
            print('当前目录已经存在result文件夹，是不是已经操作过一次了?')
            sys.exit()
        for file in files:
            if join(root, file) != abspath(__file__):
                target_dir = join(
                    join(root.replace(dirname(abspath(__file__)), join(dirname(abspath(__file__)), 'result'))))
                os.makedirs(target_dir, exist_ok=True)
                copyfile(join(root, file), join(target_dir, file))


def resize(file, limit=300):
    # 不缩放大小,改变文件大小，以K为单位
    file_dir, name = split(file)
    _, file_format = splitext(file)
    file_name, _ = splitext(name)
    convert_file = join(file_dir, 'tmp' + file_name + '.jpg')

    if 'jpg' not in file_format:
        os.rename(file, join(file_dir, file_name + '.jpg'))
        file = join(file_dir, file_name + '.jpg')
        os.system(' '.join(['convert', '"{}"'.format(file), '"{}"'.format(file)]))

    if getsize(file) / 1024 < limit:
        return

    copyfile(file, convert_file)

    left, right = 0, 100
    convert_num = 0
    while True:
        if 0 < limit - (getsize(convert_file) / 1024) < 50:
            break

        middle = (left + right) / 2
        convert_num += 1
        # JPEG即使使用100%压缩大小也会变化
        if middle < 1 or middle > 98 or convert_num > 9:
            if getsize(convert_file) / 1024 > limit:
                print('{} 我去，你这是逆天大文件啊→→压缩失败'.format(file))
            break
        try:
            # 使用subprocess在win上会报错
            os.system(' '.join(['convert', '-quality', '{}%'.format(middle), '"{}"'.format(file), '"{}"'.format(convert_file)]))
        except Exception as e:
            import logging

            logging.exception('{}出错'.format(file), e)

        if getsize(convert_file) / 1024 > limit:
            right = middle
        else:
            left = middle

    os.remove(file)
    os.rename(convert_file, join(file_dir, file_name + '.jpg'))


def main(limit=300):
    back_up()
    for root, _, files in os.walk(join(dirname(abspath(__file__)), 'result')):
        for file in files:
            if splitext(file)[1].lower() in ['.jpg', '.jpeg', '.png']:
                resize(join(root, file), limit)


if __name__ == '__main__':
    try:
        main(limit=300)
    finally:
        input('按任意键回车退出...')
