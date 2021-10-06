---
title: 记录：重装/全新安装 Windows 10 的步骤
date: 2021-09-17 20:43:00
categories: 操作系统
tags:
    - 操作系统
    - Windows
    - Windows 10
index_img: /img/windows10.webp
---

> 这篇 Blog 仅用于测试 `Hexo` / `WordPress` 是否工作正常，所以是随便写的

## 更新主板 BIOS

> BIOS 中具体哪个选项或者不会操作在什么位置可以百度

1. 准备一个大于等于 8G 的空 U 盘
2. 格式化 U 盘为 FAT32 格式
3. 去主板官网下载最新的 BIOS，解压放到 U 盘里
4. 插入 U 盘，开机进入 BIOS，更新 BIOS
5. 更新时确保不断电，更新完成后第一次开机会提示按 F1 进入 BIOS
6. 在 BIOS 中打开 XMP、快速启动、TPM、安全启动、CPU 虚拟化
7. 在 BIOS 中开启 【4G 以上解码 / 大于 4G 地址空间解码 / above 4g decoding】和【re-size BAR support (Resizable BAR)】
8. 保存 BIOS 设置并重启
    > 若重启无法进入系统，需要暂时关闭【4G 以上解码】和【re-size BAR support】

## 更新显卡 BIOS

> 若是全新安装系统，此处留待系统安装完后再进行

1. 去显卡厂商官网（不是 NVIDIA/AMD，是品牌官网）下载最新的显卡 BIOS
2. 更新显卡 BIOS 并重启

## 重装/安装系统

> 全新安装系统请从第 4 条开始，需要另外一台可以用的电脑

1. 备份所有 C 盘的重要文件到其他分区，记住 C 盘空间的总大小和剩余大小
2. 备份一些程序的设置和数据（比如摄像头设置、QQ 聊天记录之类的，设置可以用手机拍照）
    > QQ 聊天记录直接复制他的数据文件夹到其他分区即可，具体操作可以百度
3. 若有外部设备，如外置声卡和摄像头等，应提前获取好对应驱动的下载地址
4. 在[这里](https://go.microsoft.com/fwlink/?LinkId=691209)下载官方最新的系统安装盘制作工具
5. 运行该工具，制作系统安装 U 盘
6. 重启进入 BIOS，在 BIOS 中启动 U 盘中的安装程序
7. 开始安装后选择【没有激活密钥】，安装方式为【自定义】，安装位置选择与 C 盘空间总大小和剩余大小一致的分区后开始安装
8. 安装完并设置好进入系统
9. 安装必备的运行库（不要改安装位置，一直下一步就行）
    > 下面的几个 .Net 框架的下载链接不一定是最新的，详细可以去 [.Net 官网](https://dotnet.microsoft.com/)查看
      [微软常用运行库合集（Visual C++系列）](https://www.ghxi.com/yxkhj.html)  
      [.NET Desktop Runtime 5.0.10 64 位](https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-desktop-5.0.10-windows-x64-installer)  
      [.NET Desktop Runtime 5.0.10 32 位](https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-desktop-5.0.10-windows-x86-installer)  
      [.NET Desktop Runtime 3.1.19 64 位](https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-desktop-3.1.19-windows-x64-installer)  
      [.NET Desktop Runtime 3.1.19 32 位](https://dotnet.microsoft.com/download/dotnet/thank-you/runtime-desktop-3.1.19-windows-x86-installer)
10. 任务栏搜索框中搜索【启用或关闭 Windows 功能】并打开，勾选【.Net Framework 3.5 (包含 .NET 2.0 和 3.0)】并确定
11. 激活系统（激活方法问我）
12. 打开【Microsoft Store】（系统应用商店），获取所有程序的更新
13. 打开主板官网，下载芯片组驱动、网卡驱动、内置声卡驱动（有外部声卡也要下）
    > 具体要下载和安装哪些可以百度  
    > 下载和安装驱动前建议先从下面的推荐软件列表下载安装解压缩软件
14. 去 NVIDIA/AMD 官网下载显卡驱动并安装
    > 不知道网址可以百度
15. 安装外置声卡和摄像头驱动（若有）、LGHUB 等外部设备的驱动和配套软件
16. 安装必备的软件

## 一些需要更改的系统配置

- 虚拟内存
    1. 任务栏搜索【高级系统设置】并打开
    2. 在弹出的【系统属性】窗口中的【高级】选项卡的【性能】部分点【设置】，在弹出的【性能选项】中选择【高级】选项卡，点击【更改】
    3. 在弹出的【虚拟内存】窗口中，取消勾选【自动管理所有驱动器的分页文件大小】，选中 C 盘，再选中下方的【自定义大小】，填入 800-1024，再点击【设置】按钮；类似的，选中其他盘，设置为【系统管理的大小】，最后一路点击【确定】退出【系统属性】窗口

## 推荐软件列表及下载地址

### 黑名单

- 2345 全系列

### 解压缩软件

- [360 压缩](https://yasuo.360.cn/)
- [7-zip](https://www.7-zip.org/download.html) - 请从【Download 7-Zip 21.03 beta (2021-07-20)】分栏中下载【64-bit Windows x64】

### 安全软件

- [火绒](https://www.huorong.cn/) （已包含垃圾清理和弹窗拦截等功能，但需要手动开启）
- 系统自带的，其他如 360 安全卫士、腾讯电脑管家、金山电脑管家等强烈建议不要装

### 看图软件

- 系统自带
- [HoneyView](https://cn.bandisoft.com/honeyview/) （官网打开较慢）

### 视频软件

- [PotPlayer](https://potplayer.daum.net/?lang=zh_CN) （国内可能打不开官网，请选择【64bit Download】）
- [QQ 影音](https://player.qq.com/)
- 系统自带

### 浏览器

- 强烈推荐系统自带的
- [Google Chrome](http://www.google.cn/chrome/browser/desktop/index.html?standalone=1&platform=win64)

### 聊天软件

- [QQ](https://im.qq.com/pcqq/)
- [微信](https://pc.weixin.qq.com/)

### 直播软件

- [OBS Studio](https://obsproject.com/)
- 哔哩哔哩直播姬，下载在 B 站直播页面右上角的【我要开播】里

### 输入法

- 只推荐系统自带

### 文档编辑

- [Microsoft 365 (原 Office 365)](https://office.com/)
- [WPS Office](https://platform.wps.cn/)

### 其他

- 搜索整台电脑的所有文件 - [Everything](https://www.voidtools.com/zh-cn/downloads/)
- 截图软件（可以用 QQ 自带的，也可以用这个，但是需要自己研究设置） - Snipaste - 在系统自带商店搜索下载
- [B 站弹幕姬（非官方）](https://www.danmuji.org/) - [插件下载](https://www.danmuji.org/plugins/)
- [LGHUB（罗技键盘/鼠标配置）](https://www.logitechg.com.cn/zh-cn/innovation/g-hub.html)
