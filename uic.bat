echo off

rem ����Ŀ¼ QtApp �µ�.ui�ļ����Ƶ���ǰĿ¼�£����ұ���
copy .\QtApp\MainWidget.ui  MainWidget.ui

pyuic5 -o ui_MainWidget.py  MainWidget.ui
