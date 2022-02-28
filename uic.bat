echo off

rem 将子目录 QtApp 下的.ui文件复制到当前目录下，并且编译

call copy .\QtApp\MainWidget.ui  MainWidget.ui
call pyuic5 -o ui_MainWidget.py  MainWidget.ui

call copy .\QtApp\DialogSetParams.ui  DialogSetParams.ui
call pyuic5 -o ui_DialogSetParams.py  DialogSetParams.ui

call copy .\QtApp\DialogMakeTemp.ui  DialogMakeTemp.ui
call pyuic5 -o ui_DialogMakeTemp.py  DialogMakeTemp.ui
