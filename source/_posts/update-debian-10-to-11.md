---
title: 记录：Debian 10 升级到 11 的全过程
date: 2021-09-20 23:32:00
categories: 操作系统
tags:
    - 操作系统
    - Linux
index_img: /img/debian.webp
---

## 前言

Debian 11 （代号：Bullseye）已于前段时间正式发布，但目前众多云服务商仍未提供 Debian 11 镜像，需要用户先安装 Debian 10 （代号：Buster）后再手动更新至 Debian 11。

本文为作者基于腾讯云/阿里云全新安装的 Debian 10 升级到 Debian 11 的记录。

声明：本文中的操作对于已使用一段时间的系统不可完全照搬，若按照本文所述操作导致系统损坏，本人不负任何责任。

> 以下步骤均默认使用 **root** 用户在命令行界面完成操作

## 更新 Debian 10 至最新

先安装 `aptitude`，他对依赖冲突解决的比较好，然后通过他更新系统

> 使用 `full-upgrade` 升级所有软件包至最新

```bash
apt update
apt install -y aptitude apt-transport-https ca-certificates
aptitude update
aptitude full-upgrade -y
```

## 临时将当前的命令行提示语言设置为中文

```bash
aptitude install locales
dpkg-reconfigure locales
```

新弹出的界面中，使用方向键移动光标，空格键选择，Tab 切换不同区域的选项  
在新弹出的界面的列表中只选中 `en_US.UTF-8 UTF-8` 与 `zh_CN.UTF-8 UTF-8`  
然后将光标移动到 `OK` 回车进入到下一个页面  
该页面的意思为：系统环境默认语言（Default locale for the system environment）  
请保持选中 `C.UTF-8` 或 `POSIX` 并后将光标移动到 `OK` 回车退出

> 由于一些兼容性问题，请不要更改系统环境默认语言

临时切换语言为中文（重启失效，仅为了方便看懂提示，若看得懂可以不切换）：

```bash
export LANG=zh_CN.UTF-8
export LANGUAGE=zh_CN.utf8
export LC_ALL=zh_CN.UTF-8
```

查看切换语言是否成功：

```bash
apt
```

若输出的命令提示为中文即切换成功

## 将 apt 软件源更换至 Debian 11 的版本

打开 apt 软件源配置文件

```bash
aptitude install -y vim nano  # 安装常见编辑器，Debian 10 应该自带 nano，但以防万一，可以装一下
mv /etc/apt/sources.list /etc/apt/sources.list.old  # 将现有的软件源配置文件重命名并备份，mv 即 move
nano /etc/apt/sources.list  # 创建新的配置文件并用 nano 编辑器打开
```

请按不同的云服务器服务商添入不同的内容

- 腾讯云镜像源（内网，速度快且不消耗流量）

```properties
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.tencentyun.com/debian/ bullseye main contrib non-free
deb http://mirrors.tencentyun.com/debian/ bullseye-updates main contrib non-free
deb http://mirrors.tencentyun.com/debian/ bullseye-proposed-updates main non-free contrib
deb http://mirrors.tencentyun.com/debian/ bullseye-backports main non-free contrib
deb http://mirrors.tencentyun.com/debian-security/ bullseye-security main contrib non-free
# deb-src http://mirrors.tencentyun.com/debian/ bullseye-updates main contrib non-free
# deb-src http://mirrors.tencentyun.com/debian/ bullseye main contrib non-free
# deb-src http://mirrors.tencentyun.com/debian/ bullseye-proposed-updates main contrib non-free
# deb-src http://mirrors.tencentyun.com/debian/ bullseye-backports main contrib non-free
# deb-src http://mirrors.tencentyun.com/debian-security/ bullseye-security main contrib non-free
```

- 腾讯云镜像源（外网访问）

```properties
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.tencent.com/debian/ bullseye main contrib non-free
deb http://mirrors.tencent.com/debian/ bullseye-updates main contrib non-free
deb http://mirrors.tencent.com/debian/ bullseye-proposed-updates main non-free contrib
deb http://mirrors.tencent.com/debian/ bullseye-backports main non-free contrib
deb http://mirrors.tencent.com/debian-security/ bullseye-security main contrib non-free
# deb-src http://mirrors.tencent.com/debian/ bullseye-updates main contrib non-free
# deb-src http://mirrors.tencent.com/debian/ bullseye main contrib non-free
# deb-src http://mirrors.tencent.com/debian/ bullseye-proposed-updates main contrib non-free
# deb-src http://mirrors.tencent.com/debian/ bullseye-backports main contrib non-free
# deb-src http://mirrors.tencent.com/debian-security/ bullseye-security main contrib non-free
```

- 阿里云镜像源（内网，速度快且不消耗流量）

```properties
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.cloud.aliyuncs.com/debian/ bullseye main contrib non-free
deb http://mirrors.cloud.aliyuncs.com/debian/ bullseye-updates main contrib non-free
deb http://mirrors.cloud.aliyuncs.com/debian/ bullseye-proposed-updates main non-free contrib
deb http://mirrors.cloud.aliyuncs.com/debian/ bullseye-backports main non-free contrib
deb http://mirrors.cloud.aliyuncs.com/debian-security/ bullseye-security main contrib non-free
# deb-src http://mirrors.cloud.aliyuncs.com/debian/ bullseye-updates main contrib non-free
# deb-src http://mirrors.cloud.aliyuncs.com/debian/ bullseye main contrib non-free
# deb-src http://mirrors.cloud.aliyuncs.com/debian/ bullseye-proposed-updates main contrib non-free
# deb-src http://mirrors.cloud.aliyuncs.com/debian/ bullseye-backports main contrib non-free
# deb-src http://mirrors.cloud.aliyuncs.com/debian-security/ bullseye-security main contrib non-free
```

- 阿里云镜像源（外网访问）

```properties
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free
deb http://mirrors.aliyun.com/debian/ bullseye-updates main contrib non-free
deb http://mirrors.aliyun.com/debian/ bullseye-proposed-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ bullseye-backports main non-free contrib
deb http://mirrors.aliyun.com/debian-security/ bullseye-security main contrib non-free
# deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main contrib non-free
# deb-src http://mirrors.aliyun.com/debian/ bullseye main contrib non-free
# deb-src http://mirrors.aliyun.com/debian/ bullseye-proposed-updates main contrib non-free
# deb-src http://mirrors.aliyun.com/debian/ bullseye-backports main contrib non-free
# deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main contrib non-free
```

- 清华大学开源软件镜像站

```properties
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-proposed-updates main non-free contrib
deb http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main non-free contrib
deb http://mirrors.tuna.tsinghua.edu.cn/debian-security/ bullseye-security main contrib non-free
# deb-src http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-updates main contrib non-free
# deb-src http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye main contrib non-free
# deb-src http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-proposed-updates main contrib non-free
# deb-src http://mirrors.tuna.tsinghua.edu.cn/debian/ bullseye-backports main contrib non-free
# deb-src http://mirrors.tuna.tsinghua.edu.cn/debian-security/ bullseye-security main contrib non-free
```

- Debian 官方（默认，自动选择镜像，但不一定快）

```properties
deb http://deb.debian.org/debian/ bullseye main contrib
deb http://deb.debian.org/debian/ bullseye-updates main contrib
deb http://deb.debian.org/debian/ bullseye-proposed-updates main contrib
deb http://deb.debian.org/debian/ bullseye-backports main contrib
deb http://deb.debian.org/debian-security/ bullseye-security main contrib
deb-src http://deb.debian.org/debian/ bullseye-updates main contrib
deb-src http://deb.debian.org/debian/ bullseye main contrib
deb-src http://deb.debian.org/debian/ bullseye-proposed-updates main contrib
deb-src http://deb.debian.org/debian/ bullseye-backports main contrib
deb-src http://deb.debian.org/debian-security/ bullseye-security main contrib
```

## 开始升级 Debian 11

> 若更新途中提示将会自动重启服务，请使用 `y` 同意

```bash
aptitude update
aptitude upgrade  # 第一次更新，如果中间有提示文件冲突就不要盲目替换，建议查看文件的 diff 再确认要不要替换或手动解决冲突
aptitude upgrade  # 第二次更新，更新上一次可能会遗漏或冲突导致未更新的软件包
aptitude full-upgrade  # 更新系统软件包，如果中间有提示文件冲突就不要盲目替换，建议查看文件的 diff 再确认要不要替换或手动解决冲突
aptitude full-upgrade  # 再更新系统软件包
```

到这里，理论上应该已经更新完成，如果使用 ssh 登录，此时请保持当前 ssh 登录然后新开一个 ssh 窗口测试是否可以连上，若可以连上则关闭新开的 ssh 窗口，使用之前的 ssh 窗口继续下面的操作

## 清除已过期且未使用的软件包（及系统内核）

```bash
aptitude purge "~o"  # 中途可能会提示系统内核将被删除，确认即可（之前的更新理论上已安装新版本的系统内核）
```

### [可选] 安装一些必备的软件包和库

> 第一行超长，请完整复制

```bash
aptitude install curl wget binutils bzip2 gzip bzr busybox dnsutils gnupg gnupg2 gnutls-dev gpgv2 net-tools debtags ca-certificates apt-transport-https debian-keyring build-essential cpp c-compiler make cmake g++ gcc gccgo gobjc++-10 gobjc-10 python3-gccjit patch git gdbm-l10n xapian-tools checkinstall libc++1 libc++1-11 libc++-11-dev libcwidget-dev libcurl4-openssl-dev libcurl4-nss-dev libcurl4-gnutls-dev libterm-readline-gnu-perl libterm-readline-perl-perl libtap-harness-archive-perl libreadline-dev libcurl3-gnutls-dev libcurl4-gnutls-dev libtool-bin libffi-dev libssl-dev libtemplate-perl libssl1.1 libxml2-dev debian-faq-zh-cn debian-reference-zh-cn manpages-zh-cn python3 python3-apt python3-pycurl python3-wheel python3-pip
aptitude install maven openjdk-17-jdk golang
aptitude install python-six pyflakes3 python3-aiohttp python3-pyflakes python3-flake8 python3-gnupg python3-numpy python3-pep8 python3-regex python3-yaml
aptitude install tree htop vim p7zip-full p7zip-rar p7zip zip unzip neofetch ffmpeg zsh axel mariadb-client mariadb-server
aptitude install xfonts-intl-chinese xfonts-intl-chinese-big  # 中文字体，不用 GUI 界面不用装
```

### [可选] 创建新用户并调整 ssh 服务端设置

由于 `root` 用户具有系统最高权限，因此建议创建新的普通用户为日常登录 ssh 所用，该用户可使用 sudo 使用 root 权限执行命令

同时，应调整 `sshd_config`，禁止通过 `root` 用户连接 ssh

为了提高 ssh 的安全性，还可以禁用密码登录，只使用密钥登录（需要本地生成密钥并上传至远程机器）
