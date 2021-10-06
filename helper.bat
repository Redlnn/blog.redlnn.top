@echo off

:main
echo.
echo ========================================
echo.
echo ���� `hexo-cli` �����ƣ��� Hexo ��ص���
echo ��������ɺ��޷��˻ص����˵���Ҫѡ������
echo ѡ����������� bat �ļ�
echo.
echo 1. ���� Hexo ����ʱ�ļ�
echo 2. ���� Hexo ���ؿ��������
echo 3. ���ɿɷ����������������ļ�
echo 4. ʹ�� Brotli ѹ�� public �е���Դ�ļ�
echo 5. ʹ�� GZip ѹ�� public �е���Դ�ļ�
echo 6. ��� public �е�ѹ���ļ�
echo 7. �� source/img �е�ͼƬת��Ϊ webp
echo 8. �ڵ�ǰĿ¼�� cmd
echo 0. �˳�
echo.
echo ========================================
echo.
set /p choice=��ѡ���Ӧ���ֺ�س���
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