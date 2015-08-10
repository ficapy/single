#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Ficapy
# Create: '15/8/10'

# 压缩所有图片至jpg格式,且限制大小,调用convert(imagemagick)


from shutil import copyfile
import os
from subprocess import call
from os.path import join, dirname, getsize, split, splitext


def back_up():
    for root, _, files in os.walk(dirname(__file__)):
        for file in files:
            if join(root, file) != __file__:
                target_dir = join(join(root.replace(dirname(__file__), join(dirname(__file__), 'result'))))
                os.makedirs(target_dir, exist_ok=True)
                copyfile(join(root, file), join(target_dir, file))


def resize(file, limit=300):
    # 不缩放,修改质量大小以K为单位
    file_dir, name = split(file)
    _, file_format = splitext(file)
    file_name, _ = splitext(name)
    convert_file = join(file_dir, 'tmp' + file_name + '.jpg')

    if 'jpg' not in file_format:
        os.rename(file, join(file_dir, file_name + '.jpg'))
        file = join(file_dir, file_name + '.jpg')
        call(['convert', file, file])

    if getsize(file) / 1024 < limit:
        return

    copyfile(file, convert_file)

    left, right = 0, 100

    while True:
        if 0 < limit - (getsize(convert_file) / 1024) < 50:
            break

        middle = (left + right) / 2
        if middle < 1:
            print('{} 压缩失败'.format(file))
            break
        # JPEG即使使用100%压缩大小也会变化
        if middle > 95:
            break
        call(['convert', '-quality', '{}%'.format(middle), file, convert_file])

        if getsize(convert_file) / 1024 > limit:
            right = middle
        else:
            left = middle

    os.remove(file)
    os.rename(convert_file, join(file_dir, file_name + '.jpg'))


def main():
    back_up()
    for root, _, files in os.walk(join(dirname(__file__), 'result')):
        for file in files:
            if splitext(file)[1] in ['.jpg', '.jpeg', '.png']:
                resize(join(root, file))


if __name__ == '__main__':
    main()