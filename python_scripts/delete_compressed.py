# -*- coding: utf-8 -*-

import os


def listdir(dirpath):
    for _ in os.listdir(dirpath):
        origin_path = os.path.join(dirpath, _)
        if os.path.isdir(origin_path):
            listdir(origin_path)
        elif _.split('.')[-1] in ('br', 'gz'):
            os.remove(origin_path)
            print(f'deleted {origin_path}')


if __name__ == '__main__':
    if os.path.exists(os.path.join('public')):
        listdir(os.path.join('public'))
    else:
        print('Error: 找不到 public 文件夹')
