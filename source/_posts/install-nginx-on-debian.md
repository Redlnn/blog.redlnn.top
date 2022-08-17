---
title: 在 Linux 上安装 Nginx 并启用 HTTPS
date: 2021-12-19 21:11:00
categories:
    - Nginx
tags:
    - Nginx
    - Linux
index_img: /img/nginx.webp
---

## 前提

本文假设你使用的是 `Debian 11` 系统，且具有一定的 `Linux` 基础

## 安装 Nginx

由于 Debian 自带的 apt 源里的 Nginx 版本较旧，因此我们使用首先 Nginx 官方源安装 Nginx。

按照 [Nginx 官方文档](http://nginx.org/en/linux_packages.html#Debian)添加 Nginx 官方源。

1. 安装基础工具

   ```bash
   sudo apt install curl gnupg2 ca-certificates lsb-release debian-archive-keyring
   ```

2. 导入 Nginx 官方的签名密钥，以便 apt 可以验证软件包的真实性

   ```bash
   curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
       | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
   ```

3. 验证导入的签名密钥

   ```bash
   gpg --dry-run --quiet --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg
   ```

   > 请检查输出值是否等于以下内容

   ```gpg
   pub   rsa2048 2011-08-19 [SC] [expires: 2024-06-14]
         573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62
   uid                      nginx signing key <signing-key@nginx.com>
   ```

4. 此处使用`mainline`通道的 Nginx （即最新版，稳定版请参阅文档使用`Stable`通道，这个通道的概念与`Windows`的更新通道类似）

   ```bash
   echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
   http://nginx.org/packages/mainline/debian `lsb_release -cs` nginx" \
       | sudo tee /etc/apt/sources.list.d/nginx.list
   ```

5. 优先使用 Nginx 官方源而不是`Debian`默认源的 Nginx

   ```bash
    echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" \
       | sudo tee /etc/apt/preferences.d/99nginx
   ```

6. 安装 Nginx

   ```bash
   sudo apt update
   sudo apt install nginx nginx-module-geoip nginx-module-image-filter nginx-module-njs nginx-module-perl nginx-module-xslt
   ```

7. 启用 Brotil 压缩算法

   > 请参考我的[这篇文章](/2021/10/03/enable-brotli-support-without-recompiling-nginx/)

8. 启动 Nginx 并设置为开机启动

   ```bash
   sudo systemctl start nginx
   sudo systemctl enable nginx
   ```

   此时你就可以通过你服务器的 IP 或指向该 IP 的域名访问服务器，若没有问题，你将会看到 Nginx 的示例页面

9. 一些常用的 Nginx 命令

   ```bash
   sudo nginx -V # 查看 Nginx 版本与编译信息
   sudo nginx -t # 校验配置文件是否正确
   sudo nginx -s reload # 重载配置文件
   ```

## 配置 Nginx

Nginx 本体的配置位于`/etc/nginx/nginx.conf`，推荐不同的网站分开存放在不同的文件中，因此新建一个文件夹专门用于放置不同的网站的配置文件。

```bash
sudo mkdir /etc/nginx/sites-available/
sudo mkdir /etc/nginx/sites-enabled/
```

其中`sites-available`用于放置可用的网站的配置文件（正如其名，可用但不启用，即不会被 Nginx 加载），而`sites-enabled`用于放置启用的（会被 Nginx 加载的）配置文件。

### 修改 Nginx 配置文件

部分参考[这篇文章](https://imququ.com/post/my-nginx-conf-for-wpo.html)

用文本编辑器打开配置文件，此处使用`vim`，有关`vim`的使用方法请自行搜索

```bash
sudo vim /etc/nginx/nginx.conf
```

配置文件内容参考如下部分

```nginx
user  nginx;
worker_processes  auto; # 指定Nginx要开启的进程数，默认auto

load_module modules/ngx_http_brotli_filter_module.so; # 开启 Brotli 算法
load_module modules/ngx_http_brotli_static_module.so;

# 日志输出级别有debug、info、notice、warn、error、crit可供选择
error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;

events {
    use  epoll; # 事件模型
    worker_connections  1024; # 每个进程的最大连接数
    multi_accept  on;
}

http {
    include          /etc/nginx/mime.types; # 文件扩展名与文件类型映射表
    default_type  application/octet-stream; # 默认文件类型

    # 日志格式
    log_format  main  '[$time_iso8601] $remote_user@$remote_addr "$request" '
                      'status:$status bytes_sent:$body_bytes_sent referer:"$http_referer" '
                      'ua:"$http_user_agent" from:"$http_x_forwarded_for" '
                      'clientRealIp:"$clientRealIp"';

    access_log  /var/log/nginx/access.log  main; # 日志位置

    charset  utf-8; # 默认编码

    server_names_hash_bucket_size   64; # 服务器名字的hash表大小
    client_header_buffer_size       4k; # 客户端请求头部的缓冲区大小
    large_client_header_buffers  4 64k; # 设定请求缓存大小
    client_max_body_size            8m; # 设定请求缓存大小
    client_header_timeout           15; # 请求头的超时时间
    client_body_timeout             15; # 请求体的超时时间
    send_timeout                    15; # 响应客户端超时时间
    keepalive_timeout               65; # 连接超时时间，默认为75s，可以放在http，server，location块
    server_tokens                  off; # 不向浏览器发送 Nginx 版本，包括错误页面与相应请求

    autoindex  off; # 关闭目录列表访问（即可列出文件夹的文件目录）
    autoindex_exact_size off; # 显示出文件的确切大小，单位是bytes，改为off后，显示出文件的大概大小，单位是KB或者MB或者GB
    autoindex_localtime on; # 显示的文件时间，off为GMT时间，on为服务器时间

    sendfile     on; # 开启高效文件传输模式,sendfile指令指定nginx是否调用sendfile函数来输出文件,对于普通应用设为 on,如果用来进行下载等应用磁盘IO重负载应用,可设置为off,以平衡磁盘与网络I/O处理速度,降低系统的负载.注意：如果图片显示不正常把这个改成off.
    tcp_nopush   on; # 防止网络阻塞
    tcp_nodelay  on; # 防止网络阻塞

    # FastCGI相关参数是为了改善网站的性能：减少资源占用,提高访问速度.下面参数看字面意思都能理解.
    fastcgi_connect_timeout        300; # 连接到后端FastCGI的超时时间
    fastcgi_send_timeout           300; # 读取 是指nginx进程向fastcgi进程发送request的整个过程的超时时间
    fastcgi_read_timeout           300; # 发请求 是指fastcgi进程向nginx进程发送response的整个过程的超时时间
    fastcgi_buffer_size            64k;
    fastcgi_buffers              4 64k;
    fastcgi_busy_buffers_size     128k;
    fastcgi_temp_file_write_size  128k;
    fastcgi_intercept_errors        on;

    gzip on;
    gzip_min_length     1k; # 允许压缩的页面的最小字节数,页面字节数从header偷得content-length中获取.默认是0,不管页面多大都进行压缩.建议设置成大于1k的字节数,小于1k可能会越压越大
    gzip_buffers     4 32k; # 表示申请4个单位为32k的内存作为压缩结果流缓存,默认值是申请与原始数据大小相同的内存空间来存 储gzip压缩结果
    gzip_http_version  1.1; # 压缩版本（默认1.1,目前大部分浏览器已经支持gzip解压.前端如果是squid2.5请使用1.0）
    gzip_comp_level      5; # 压缩等级.1压缩比最小,处理速度快.9压缩比最大,比较消耗cpu资源,处理速度最慢,但是因为压缩比最 大,所以包最小,传输速度快
    # 压缩类型,默认就已经包含text/html,所以下面就不用再写了,写上去也不会有问题,但是会有一个warn.
    gzip_types text/plain text/css application/x-pointplus text/javascript application/javascript application/x-javascript text/xml application/xml application/xaml+xml application/atom+xml application/rss+xml application/xhtml+xml application/json image/vnd.microsoft.icon image/vnd.microsoft.ico image/x-icon image/svg+xml image/x-win-bitmap image/bmp;
    gzip_vary           on; # 选项可以让前端的缓存服务器缓存经过gzip压缩的页面.例如:用squid缓存经过nginx压缩的数据

    brotli on;
    brotli_static on;
    brotli_comp_level 6;
    brotli_buffers 16 8k;
    brotli_min_length 20;
    brotli_types text/plain text/css application/x-pointplus text/javascript application/javascript application/x-javascript text/xml application/xml application/xaml+xml application/atom+xml application/rss+xml application/xhtml+xml application/json image/vnd.microsoft.icon image/vnd.microsoft.ico image/x-icon image/svg+xml image/x-win-bitmap image/bmp;

    # 取得原始用户的IP地址，From: https://blog.csdn.net/u011078940/article/details/51426288
    # 通过 map 指令，为 nginx 创建了一个变量 $clientRealIp ，这个就是原始用户的真实 IP 地址，
    # 不论用户是直接访问，还是通过一串 CDN 之后的访问，我们都能取得正确的原始IP地址
    map $http_x_forwarded_for $clientRealIp {
        ~^(?P<firstAddr>[0-9\.]+),?.*$  $firstAddr;
        ""  $remote_addr; # 没有通过代理，直接用 remote_addr
        # 用正则匹配，从 x_forwarded_for 中取得用户的原始IP
        # 例如 X-Forwarded-For: 202.123.123.11, 208.22.22.234, 192.168.2.100,...
        # 这里第一个 202.123.123.11 是用户的真实 IP，后面其它都是经过的 CDN 服务器
    }

    # 用户的 IP 地址作为 Key，每个 IP 地址最多有 250 个并发连接
    # 超过 250 个连接，就返回 503 错误
    #limit_conn_zone $binary_remote_addr zone=TotalConnLimitZone:10m ;
    limit_conn_zone $clientRealIp zone=TotalConnLimitZone:20m;
    limit_conn TotalConnLimitZone 250;
    limit_conn_log_level notice;

    # 用户的 IP 地址作为 Key，每个 IP 地址每秒处理 200 个请求
    # 若每秒几百次的刷，就返回 503 错误
    #limit_req_zone $binary_remote_addr zone=ConnLimitZone:10m  rate=200r/s;
    limit_req_zone $clientRealIp zone=ConnLimitZone:10m rate=200r/s;
    limit_req_log_level notice;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*; # 引入已启用的网站配置文件

    # 通过除了 已启用的网站配置文件 中指定的域名外访问服务器的逻辑（缺省网站配置）
    server {
        # 监听 80 端口，开启 spdy、tcp_fastopen 与 tcp_reuseport
        listen 80 default default_server spdy fastopen=3 reuseport;
        server_name _;

        access_log /var/log/nginx/access_ip.log main; # 自定义该配置的日志文件存放位置

        # 每秒处理 200 个请求 + 30 个排队
        limit_req zone=ConnLimitZone burst=30 nodelay;

        return 301 https://www.example.com$request_uri; # 301跳转到指定网站
    }

    server {
        # 监听 443 端口，即 https
        listen 443 ssl default_server spdy fastopen=3 reuseport;
        server_name _;

        access_log /var/log/nginx/access_ip.log main;

        # 每秒处理 200 个请求 + 30 个排队
        limit_req zone=ConnLimitZone burst=30 nodelay;

        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem; # 引入 SSL 证书
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf; # 引入 SSL 设置
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        return 301 https://www.example.com$request_uri;
    }
}
```

### 创建网站配置文件

此处假设你的用户名为 user 且具有使用`sudo`命令的权限  
以及你的网站目录位于`/home/user/website`，主页位于`/home/user/website/index.html`

先用文本编辑器创建并打开一个网站配置文件

```bash
sudo vim /etc/nginx/sites-available/website.conf
```

文件内容可参考如下部分

```nginx
server {
    listen 443 ssl http2 spdy fastopen=3 reuseport; # 开启 http2
    server_name www.example.com;

    access_log /var/log/nginx/access_www.example.com.log main;

    root /home/user/website;

    index index.html;

    # 对于不同的文件分别设置
    location ~* \.(jpg|jpeg|png|svg|webp|gif|css|js|ico|woff|woff2|scss) {
        try_files $uri =404;
        expires 1d; # 客户端缓存时间
        access_log off; # 关闭日志记录
        log_not_found off; # 关闭找不到日志时报错
    }

    location = /robots.txt {
        try_files $uri =404;
        expires 30d; # 客户端缓存时间
        log_not_found off;
        access_log off;
    }

    location / {
        # 每秒处理 200 个请求 + 30 个排队
        limit_req zone=ConnLimitZone burst=30 nodelay;

        try_files $uri $uri/ =404;
        try_files $uri $uri/ /index.html$query_string =404;
    }
}

# http 访问跳转 https
server {
    listen 80;
    server_name www.example.com;

    return 301 https://$host$request_uri;
}
```

### 申请 Let's Encrypt 的免费 SSL 证书

- 安装申请工具

  ```bash
  # 此处必须使用 sudo 以 root 用户安装，否则后续会报错
  # 平时使用 pip 一般情况下请不要添加 sudo
  sudo python3 -m pip install certbot certbot-nginx
  ```

- 申请 Let's Encrypt 证书需要注意以下几点：

  1. 为了方便使用，我们将会申请同时可用于根域名（`example.com`）与泛域名（`*.example.com`）。因此在申请过程中为了验证域名的所有权，将会要求你在域名的 DNS 记录上添加一个**临时**的`TXT`记录，请自己参阅`certbot`的提示操作
  2. Let's Encrypt 的免费证书只有**3个月**有效期，因此需要每2个月续期一次
  3. 由于使用了`certbot-nginx`插件，`certbot`会在申请域名时自动更改你的 Nginx 的主配置文件并创建一个新的网站（`server`块），因为我们在上文中已配置好了 SSL 相关信息，因此需要在`/etc/nginx/nginx.conf`中删除`certbot`新添加的`server`块（对比一下就会知道他加了什么了）

- 使用`certbot`为你的域名申请一个证书

  > 此处命令中的邮箱是你的个人邮箱，用于接收 Let's Encrypt 的提醒邮件（无广告，不泄露）
  > 如果你的 DNS 使用的是 CloudFlare 的服务，你可以考虑使用 certbot-cloudflare 插件自动化申请

  ```bash
  sudo certbot -d "*.example.com" -d "example.com" --agree-tos --email user@example.com --nginx
  ```

- 证书到期时使用`certbot`续期

  ```bash
  sudo certbot renew
  ```

## 后续

完成以上步骤后，你就可以尝试重载 Nginx 的配置文件，若没有报错即可使用你设置的域名访问服务器了（记得添加在你域名的 DNS 中添加指向该服务器 IP 地址的 A 记录噢）
