@echo off
REM 设置 Python 脚本路径（不加双引号）
set SCRIPT_PATH=C:\Users\86156\Desktop\Program\python_work\练习\auto_music.py

REM 使用 call 调用并传入歌名参数，整行加引号防止路径空格出错
call python "%SCRIPT_PATH%" %1

