echo off

rem ����Ŀ¼ QtApp �µ�.ui�ļ����Ƶ���ǰĿ¼�£����ұ���

call copy .\QtApp\MainWidget.ui  MainWidget.ui
call pyuic5 -o ui_MainWidget.py  MainWidget.ui

call copy .\QtApp\DialogSetParams.ui  DialogSetParams.ui
call pyuic5 -o ui_DialogSetParams.py  DialogSetParams.ui

call copy .\QtApp\DialogMakeTemp.ui  DialogMakeTemp.ui
call pyuic5 -o ui_DialogMakeTemp.py  DialogMakeTemp.ui
