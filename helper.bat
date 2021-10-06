@echo off

:main
echo.
echo ========================================
echo.
echo 由于 `hexo-cli` 的限制，与 Hexo 相关的命
echo 令运行完成后无法退回到主菜单，要选择其他
echo 选项，请重新运行 bat 文件
echo.
echo 1. 清理 Hexo 的临时文件
echo 2. 开启 Hexo 本地开发服务端
echo 3. 生成可发布到生产环境的文件
echo 4. 使用 Brotli 压缩 public 中的资源文件
echo 5. 使用 GZip 压缩 public 中的资源文件
echo 6. 清除 public 中的压缩文件
echo 7. 将 source/img 中的图片转换为 webp
echo 8. 在当前目录打开 cmd
echo 0. 退出
echo.
echo ========================================
echo.
set /p choice=请选择对应数字后回车：
if /i "%choice%"=="1" goto clean
if /i "%choice%"=="2" goto serve
if /i "%choice%"=="3" goto build
if /i "%choice%"=="4" goto brotli
if /i "%choice%"=="5" goto gzip
if /i "%choice%"=="6" goto delete_compressed
if /i "%choice%"=="7" goto webp
if /i "%choice%"=="8" goto c

if /i "%choice%"=="0" exit
cls&set choice=&goto main

:clean
cls&set choice=
hexo clean
goto main

:serve
cls&set choice=
hexo s
goto main

:build
cls&set choice=
start hexo g
goto main

:brotli
cls&set choice=
python .\python_scripts\compress_by_brotli.py
goto main

:gzip
cls&set choice=
python .\python_scripts\compress_by_gzip.py
goto main

:delete_compressed
cls&set choice=
python .\python_scripts\delete_compressed.py
goto main

:webp
cls&set choice=
python .\python_scripts\convert_img2webp.py
goto main

:c
start cmd
exit