# -*- coding: utf-8 -*-

import os

from PIL import Image

for _ in os.listdir(os.path.join('source', 'img')):
    if _.endswith('.jpg') or _.endswith('.png'):
        f_path = os.path.join('source', 'img', _)
        if _.endswith('.jpg'):
            convert_path = os.path.join(
                'source', 'img', _.replace('jpg', 'webp'))
        else:
            convert_path = os.path.join(
                'source', 'img', _.replace('png', 'webp'))

        if os.path.exists(convert_path):
            print(f'{convert_path} 已存在，不进行转换')
        else:
            with Image.open(f_path) as f:
                longest = f.width if f.width > f.width else f.height
                flag = f.width > f.height
                if f.width > 800:
                    if f.width >= 2160:
                        if flag:
                            f = f.resize((1920, int(f.height/(f.width/1920))),
                                         resample=Image.LANCZOS, reducing_gap=True)
                        else:
                            f = f.resize((int(f.width/(f.height/1920)), 1920),
                                         resample=Image.LANCZOS, reducing_gap=True)
                    elif 1920 > f.width >= 1280:
                        f = f.resize((1280, int(f.height/(f.width/1280))),
                                     resample=Image.LANCZOS, reducing_gap=True)
                    elif 1280 > f.width >= 800:
                        f = f.resize((800, int(f.height/(f.width/800))),
                                     resample=Image.LANCZOS, reducing_gap=True)
                    f.save(convert_path, 'WebP',
                           quality=70, method=6, allow_mixed=True)
                else:
                    f.save(convert_path, 'WebP',
                           quality=80, method=6, allow_mixed=True)
            print(
                f'{_}: {round(os.path.getsize(f_path)/1024, 2)}KB -> {round(os.path.getsize(convert_path)/1024, 2)}KB')
