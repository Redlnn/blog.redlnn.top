# -*- coding: utf-8 -*-

import os
import gzip

compress_filetype = ['css', 'js', 'html', 'xml', 'txt', 'md', 'json', 'ttf', 'otf', 'woff', 'woff2', 'ico', 'tiff', 'svg', 'bmp']


def compress(origin_filepath, filename):
    with open(origin_filepath, 'rb') as f:
        with gzip.GzipFile(filename, 'wb', 9, open(f'{origin_filepath}.gz', 'wb')) as output:
            output.write(f.read())
            print(f'{origin_filepath}.gz')


def listdir(dirpath):
    for _ in os.listdir(dirpath):
        origin_path = os.path.join(dirpath, _)
        if os.path.isdir(origin_path):
            listdir(origin_path)
        else:
            if _.split('.')[-1] not in compress_filetype:
                continue
            if os.path.exists(f'{origin_path}.gz'):
                print(f'{origin_path}.gz 已存在，跳过压缩')
                continue
            compress(origin_path, _)


if __name__ == '__main__':
    if not os.path.exists(os.path.join('public')):
        print('Error: 找不到 public 文件夹')
    else:
        listdir(os.path.join('public'))
