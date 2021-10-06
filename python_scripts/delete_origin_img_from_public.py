# -*- coding: utf-8 -*-

import os

if os.path.exists(os.path.join('public')):
    for _ in os.listdir(os.path.join('public', 'img')):
        if _.endswith('.jpg') or _.endswith('.png'):
            f_path = os.path.join('source', 'img', _)
            if _.endswith('.jpg'):
                convert_path = os.path.join(
                    'source', 'img', _.replace('jpg', 'webp'))
            else:
                convert_path = os.path.join(
                    'source', 'img', _.replace('png', 'webp'))

            if os.path.exists(convert_path) and os.path.exists(f_path):
                os.remove(f_path)
                print(f'deleted {f_path}')
else:
    print('Error: 找不到 public 文件夹')
