# -*- coding: utf-8 -*-

import os


def listdir(dirpath):
    for _ in os.listdir(dirpath):
        origin_path = os.path.join(dirpath, _)
        if os.path.isdir(origin_path):
            listdir(origin_path)
        else:
            if _.split('.')[-1] in ('br', 'gz'):
                os.remove(origin_path)
                print(f'deleted {origin_path}')


if __name__ == '__main__':
    if not os.path.exists(os.path.join('public')):
        print('Error: 找不到 public 文件夹')
    else:
        listdir(os.path.join('public'))
