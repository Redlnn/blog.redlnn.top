---
title: 不重新编译 Nginx 的情况下启用 Brotli 压缩算法
date: 2021-10-03 2:34:00
categories:
    - Nginx
tags:
    - Nginx
    - Brotli
index_img: /img/nginx.webp
---

## 前言

本文假设系统环境为 Debian 11，且系统目前已安装 Nginx 官方源的 1.21.4 版本的 Nginx。

前提：

- 官方版本的 Nginx 默认不支持 Brotli 压缩算法；
- 我们又想要保留包管理器安装的官方版本的 Nginx（方便日后检查更新或使用其他依赖 Nginx 的包，如 `python3-certbot-nginx` 等）。

目前可以搜到的大部分为 Nginx 启用 Brotli 的方法均要求我们卸载包管理器安装的 Nginx，而我们其实可以自己手动编译一份适用于我们当前所用的 Nginx 版本的 Brotli 模块并动态加载。

## 关于 Brotli

### ngx_brotli

其实 Nginx 上要使用 Brotli 要加载一个名叫 `ngx_brotli` 的模块而不是 Brotli 本身。该模块也由 Google 开发并开源在 [GitHub 仓库](https://github.com/google/ngx_brotli)中。

### Brotli

以下内容摘自 [Wikipedia](https://en.m.wikipedia.org/wiki/Brotli)

> Brotli is a data format specification for data streams compressed with a specific combination of the general-purpose LZ77 lossless compression algorithm, Huffman coding and 2nd order context modelling. Brotli is a compression algorithm developed by Google and works best for text compression. Brotli is primarily used by web servers and content delivery networks to compress HTTP content, making internet websites load faster. A successor to gzip, it is supported by all major web browsers and is becoming increasingly popular, as it provides better compression than gzip.

以下内容由 [DeepL翻译](https://www.deepl.com/translator) 基于上述英文文本加以人工修改而成

> Brotli 是一种数据格式规范，其是基于通用的LZ77无损压缩算法、Huffman编码和二阶上下文建模的特定组合压缩的数据流。Brotli 是谷歌开发的一种压缩算法，对文本压缩效果最好。Brotli 主要被网络服务器和内容交付网络用来压缩HTTP内容，使互联网网站加载速度更快。作为 gzip 的继承者，它被所有主要的网络浏览器所支持，并且越来越受欢迎，因为它提供了比gzip更好的压缩效果。

## 前期准备

安装编译 `ngx_brotli` 模块必要的库（此处使用 `aptitude` 包管理器，与 `apt` 用法相似）。

```bash
sudo aptitude install build-essential libperl-dev libpcre++-dev libpcre2-dev openssl libssl1.1 libssl-dev
```

## 下载源码

首页查询系统中已安装的 Nginx 版本

```bash
sudo nginx -V
```

我这里为 `1.21.4`，然后从 Nginx 官方服务器上下载对应版本的源码并解压

```bash
wget http://nginx.org/download/nginx-1.21.4.tar.gz
tar -xvf nginx-1.21.4.tar.gz
```

下载 `ngx_brotli` 源码并初始化 Git 子模块

```bash
cd nginx-1.21.4
git clone https://github.com/google/ngx_brotli.git --depth=1
cd ngx_brotli
git submodule update --init
cd ../
```

若 Git clone 或初始化子模块较慢，可重试几次或在个人电脑上 clone 并初始化子模块后再上传到服务器中。

### 为 Nginx 编译 ngx_brotli 模块

首先获取当前系统中已安装的 Nginx 的编译参数

```bash
sudo nginx -V
```

得到如下内容

```
nginx version: nginx/1.20.2
built by gcc 10.2.1 20210110 (Debian 10.2.1-6)
built with OpenSSL 1.1.1k  25 Mar 2021
TLS SNI support enabled
configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-g -O2 -ffile-prefix-map=/data/builder/debuild/nginx-1.20.2/debian/debuild-base/nginx-1.20.2=. -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie'
```

`configure arguments` 后的内容即是我们需要的编译参数

然后先构建出编译 `ngx_brotli` 模块的参数 `./configure {上面得到的编译参数} --add-dynamic-module=./ngx_brotli` 并执行，即

```bash
./configure --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-compat --with-file-aio --with-threads --with-http_addition_module --with-http_auth_request_module --with-http_dav_module --with-http_flv_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_mp4_module --with-http_random_index_module --with-http_realip_module --with-http_secure_link_module --with-http_slice_module --with-http_ssl_module --with-http_stub_status_module --with-http_sub_module --with-http_v2_module --with-mail --with-mail_ssl_module --with-stream --with-stream_realip_module --with-stream_ssl_module --with-stream_ssl_preread_module --with-cc-opt='-g -O2 -ffile-prefix-map=/data/builder/debuild/nginx-1.20.2/debian/debuild-base/nginx-1.20.2=. -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -Wl,--as-needed -pie' --add-dynamic-module=/path/to/ngx_brotli
```

然后执行如下命令开始编译模块

```bash
make modules
```

编译完成后将编译出来的模块复制到 Nginx 的模块目录并更改所有者和权限

```bash
sudo cp ./objs/ngx_http_brotli_static_module.so /usr/lib/nginx/modules/
sudo cp ./objs/ngx_http_brotli_filter_module.so /usr/lib/nginx/modules/
sudo chown root:root /usr/lib/nginx/modules/ngx_http_brotli_static_module.so
sudo chown root:root /usr/lib/nginx/modules/ngx_http_brotli_filter_module.so
sudo chmod 644 /usr/lib/nginx/modules/ngx_http_brotli_static_module.so /usr/lib/nginx/modules/ngx_http_brotli_filter_module.so
```

### 在配置文件中引入模块并启用 Brotli 压缩算法

打开 Nginx 的配置文件（`/etc/nginx/nginx.conf`）

添加如下内容

```nginx
load_module modules/ngx_http_brotli_filter_module.so;
load_module modules/ngx_http_brotli_static_module.so;

brotli on;
brotli_comp_level 6;
brotli_static on;
brotli_buffers 16 8k;
brotli_min_length 20
brotli_types text/plain text/css application/x-pointplus
             text/javascript application/javascript application/x-javascript
             text/xml application/xml application/xaml+xml application/atom+xml application/rss+xml application/xhtml+xml application/json
             application/vnd.ms-fontobject application/x-font-opentype application/x-font-truetype application/x-font-otf application/x-font-ttf font/eot font/opentype font/truetype font/otf font/ttf font/sfnt font/woff font/woff2
             image/vnd.microsoft.icon image/vnd.microsoft.ico image/x-icon image/tiff image/svg+xml image/x-win-bitmap image/bmp image/png image/jpeg;
```

最后保存并退出，然后重启 Nginx 即可

```bash
sudo nginx -t
sudo systemctl restart nginx
sudo nginx -s reload
```

## 后记

之后如果 Nginx 被包管理器更新版本之后无法启动并提示 `module is not binary compatible` 错误，说明 `ngx_brotli` 模块与 Nginx 版本不兼容，需要使用 相同版本的 Nginx 的源代码重新编译新的模块。
