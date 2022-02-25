echo off

rem 将子目录 QtApp 下的.ui文件复制到当前目录下，并且编译
copy .\QtApp\MainWidget.ui  MainWidget.ui

pyuic5 -o ui_MainWidget.py  MainWidget.ui
