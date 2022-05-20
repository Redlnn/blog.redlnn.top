# -*- coding: utf-8 -*-

import os
import brotli

compress_filetype = ['css', 'js', 'html', 'xml', 'txt', 'md', 'json', 'ttf', 'otf', 'woff', 'woff2', 'ico', 'tiff', 'svg', 'bmp']


def compress(origin_filepath, filetype):
    with open(origin_filepath, 'rb') as f:
        if filetype in ['css', 'js', 'html', 'xml', 'txt', 'md', 'json', 'svg']:
            data = brotli.compress(f.read(), mode=brotli.MODE_TEXT)
        elif filetype in ['woff', 'woff2']:
            data = brotli.compress(f.read(), mode=brotli.MODE_FONT)
        else:
            data = brotli.compress(f.read())

        with open(f'{origin_filepath}.br', 'wb') as f_target:
            f_target.write(data)
            print(f'{origin_filepath}.br')


def listdir(dirpath):
    for _ in os.listdir(dirpath):
        origin_path = os.path.join(dirpath, _)
        if os.path.isdir(origin_path):
            listdir(origin_path)
        else:
            filetype = _.split('.')[-1]
            if filetype not in compress_filetype:
                continue
            if os.path.exists(f'{origin_path}.br'):
                print(f'{origin_path}.br 已存在，跳过压缩')
                continue
            compress(origin_path, filetype)


if __name__ == '__main__':
    if os.path.exists(os.path.join('public')):
        listdir(os.path.join('public'))
    else:
        print('Error: 找不到 public 文件夹')
