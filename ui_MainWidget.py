# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(880, 573)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.grpCamera = QtWidgets.QGroupBox(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.grpCamera.setFont(font)
        self.grpCamera.setObjectName("grpCamera")
        self.gridLayout = QtWidgets.QGridLayout(self.grpCamera)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.labDetectCamera = QtWidgets.QLabel(self.grpCamera)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labDetectCamera.setFont(font)
        self.labDetectCamera.setObjectName("labDetectCamera")
        self.gridLayout.addWidget(self.labDetectCamera, 0, 1, 1, 1)
        self.labLinkCamera = QtWidgets.QLabel(self.grpCamera)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labLinkCamera.setFont(font)
        self.labLinkCamera.setObjectName("labLinkCamera")
        self.gridLayout.addWidget(self.labLinkCamera, 2, 1, 1, 1)
        self.btnLinkCamera = QtWidgets.QPushButton(self.grpCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnLinkCamera.sizePolicy().hasHeightForWidth())
        self.btnLinkCamera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnLinkCamera.setFont(font)
        self.btnLinkCamera.setObjectName("btnLinkCamera")
        self.gridLayout.addWidget(self.btnLinkCamera, 2, 0, 1, 1)
        self.btnDetectCamera = QtWidgets.QPushButton(self.grpCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDetectCamera.sizePolicy().hasHeightForWidth())
        self.btnDetectCamera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnDetectCamera.setFont(font)
        self.btnDetectCamera.setObjectName("btnDetectCamera")
        self.gridLayout.addWidget(self.btnDetectCamera, 0, 0, 1, 1)
        self.btnTestCamera = QtWidgets.QPushButton(self.grpCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTestCamera.sizePolicy().hasHeightForWidth())
        self.btnTestCamera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnTestCamera.setFont(font)
        self.btnTestCamera.setObjectName("btnTestCamera")
        self.gridLayout.addWidget(self.btnTestCamera, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.grpCamera)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 4, 1, 1, 1)
        self.btnCloseCamera = QtWidgets.QPushButton(self.grpCamera)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCloseCamera.sizePolicy().hasHeightForWidth())
        self.btnCloseCamera.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnCloseCamera.setFont(font)
        self.btnCloseCamera.setObjectName("btnCloseCamera")
        self.gridLayout.addWidget(self.btnCloseCamera, 5, 0, 1, 1)
        self.labCloseCamera = QtWidgets.QLabel(self.grpCamera)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labCloseCamera.setFont(font)
        self.labCloseCamera.setObjectName("labCloseCamera")
        self.gridLayout.addWidget(self.labCloseCamera, 5, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.gridLayout.setColumnStretch(1, 4)
        self.verticalLayout_3.addWidget(self.grpCamera)
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.grpDetect = QtWidgets.QGroupBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.grpDetect.setFont(font)
        self.grpDetect.setObjectName("grpDetect")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.grpDetect)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnStartDetect = QtWidgets.QPushButton(self.grpDetect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStartDetect.sizePolicy().hasHeightForWidth())
        self.btnStartDetect.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnStartDetect.setFont(font)
        self.btnStartDetect.setObjectName("btnStartDetect")
        self.verticalLayout.addWidget(self.btnStartDetect)
        self.btnStopDetect = QtWidgets.QPushButton(self.grpDetect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnStopDetect.sizePolicy().hasHeightForWidth())
        self.btnStopDetect.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnStopDetect.setFont(font)
        self.btnStopDetect.setObjectName("btnStopDetect")
        self.verticalLayout.addWidget(self.btnStopDetect)
        self.btnSetParams = QtWidgets.QPushButton(self.grpDetect)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSetParams.sizePolicy().hasHeightForWidth())
        self.btnSetParams.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnSetParams.setFont(font)
        self.btnSetParams.setObjectName("btnSetParams")
        self.verticalLayout.addWidget(self.btnSetParams)
        self.horizontalLayout_2.addWidget(self.grpDetect)
        self.grpTemp = QtWidgets.QGroupBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.grpTemp.setFont(font)
        self.grpTemp.setObjectName("grpTemp")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.grpTemp)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.btnSelectTemp = QtWidgets.QPushButton(self.grpTemp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSelectTemp.sizePolicy().hasHeightForWidth())
        self.btnSelectTemp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnSelectTemp.setFont(font)
        self.btnSelectTemp.setObjectName("btnSelectTemp")
        self.verticalLayout_2.addWidget(self.btnSelectTemp)
        self.btnMakeTemp = QtWidgets.QPushButton(self.grpTemp)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnMakeTemp.sizePolicy().hasHeightForWidth())
        self.btnMakeTemp.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnMakeTemp.setFont(font)
        self.btnMakeTemp.setObjectName("btnMakeTemp")
        self.verticalLayout_2.addWidget(self.btnMakeTemp)
        self.horizontalLayout_2.addWidget(self.grpTemp)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_4.setContentsMargins(-1, -1, 9, 9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_4 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labAdr = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labAdr.sizePolicy().hasHeightForWidth())
        self.labAdr.setSizePolicy(sizePolicy)
        self.labAdr.setObjectName("labAdr")
        self.gridLayout_2.addWidget(self.labAdr, 0, 0, 1, 1)
        self.lineEditAdr = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditAdr.sizePolicy().hasHeightForWidth())
        self.lineEditAdr.setSizePolicy(sizePolicy)
        self.lineEditAdr.setText("")
        self.lineEditAdr.setObjectName("lineEditAdr")
        self.gridLayout_2.addWidget(self.lineEditAdr, 0, 1, 1, 1)
        self.labPort = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labPort.sizePolicy().hasHeightForWidth())
        self.labPort.setSizePolicy(sizePolicy)
        self.labPort.setObjectName("labPort")
        self.gridLayout_2.addWidget(self.labPort, 1, 0, 1, 1)
        self.lineEditPort = QtWidgets.QLineEdit(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditPort.sizePolicy().hasHeightForWidth())
        self.lineEditPort.setSizePolicy(sizePolicy)
        self.lineEditPort.setObjectName("lineEditPort")
        self.gridLayout_2.addWidget(self.lineEditPort, 1, 1, 1, 1)
        self.verticalLayout_10.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnTCPOpen = QtWidgets.QPushButton(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTCPOpen.sizePolicy().hasHeightForWidth())
        self.btnTCPOpen.setSizePolicy(sizePolicy)
        self.btnTCPOpen.setObjectName("btnTCPOpen")
        self.horizontalLayout.addWidget(self.btnTCPOpen)
        self.btnTCPClose = QtWidgets.QPushButton(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTCPClose.sizePolicy().hasHeightForWidth())
        self.btnTCPClose.setSizePolicy(sizePolicy)
        self.btnTCPClose.setObjectName("btnTCPClose")
        self.horizontalLayout.addWidget(self.btnTCPClose)
        self.labTCP = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labTCP.setFont(font)
        self.labTCP.setObjectName("labTCP")
        self.horizontalLayout.addWidget(self.labTCP)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 2)
        self.verticalLayout_10.addWidget(self.frame_5)
        self.horizontalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.btnOpenRelay = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnOpenRelay.sizePolicy().hasHeightForWidth())
        self.btnOpenRelay.setSizePolicy(sizePolicy)
        self.btnOpenRelay.setObjectName("btnOpenRelay")
        self.verticalLayout_11.addWidget(self.btnOpenRelay)
        self.btnCloseRelay = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnCloseRelay.sizePolicy().hasHeightForWidth())
        self.btnCloseRelay.setSizePolicy(sizePolicy)
        self.btnCloseRelay.setObjectName("btnCloseRelay")
        self.verticalLayout_11.addWidget(self.btnCloseRelay)
        self.labRelay = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labRelay.sizePolicy().hasHeightForWidth())
        self.labRelay.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labRelay.setFont(font)
        self.labRelay.setObjectName("labRelay")
        self.verticalLayout_11.addWidget(self.labRelay)
        self.btnTestRelay = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnTestRelay.sizePolicy().hasHeightForWidth())
        self.btnTestRelay.setSizePolicy(sizePolicy)
        self.btnTestRelay.setObjectName("btnTestRelay")
        self.verticalLayout_11.addWidget(self.btnTestRelay)
        self.horizontalLayout_4.addWidget(self.groupBox_3)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_3.addWidget(self.frame_6)
        self.verticalLayout_3.setStretch(0, 4)
        self.verticalLayout_3.setStretch(1, 3)
        self.verticalLayout_3.setStretch(2, 3)
        self.horizontalLayout_3.addWidget(self.frame_3)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.grpInput = QtWidgets.QGroupBox(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.grpInput.setFont(font)
        self.grpInput.setObjectName("grpInput")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.grpInput)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.labInput = QtWidgets.QLabel(self.grpInput)
        self.labInput.setAlignment(QtCore.Qt.AlignCenter)
        self.labInput.setObjectName("labInput")
        self.verticalLayout_4.addWidget(self.labInput)
        self.verticalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_8.addWidget(self.grpInput)
        self.grpOuput = QtWidgets.QGroupBox(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.grpOuput.setFont(font)
        self.grpOuput.setObjectName("grpOuput")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.grpOuput)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labOutput = QtWidgets.QLabel(self.grpOuput)
        self.labOutput.setAlignment(QtCore.Qt.AlignCenter)
        self.labOutput.setObjectName("labOutput")
        self.verticalLayout_5.addWidget(self.labOutput)
        self.verticalLayout_7.addLayout(self.verticalLayout_5)
        self.verticalLayout_8.addWidget(self.grpOuput)
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.verticalLayout_8.addWidget(self.groupBox)
        self.verticalLayout_8.setStretch(0, 8)
        self.verticalLayout_8.setStretch(1, 8)
        self.verticalLayout_8.setStretch(2, 1)
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.horizontalLayout_3.setStretch(0, 5)
        self.horizontalLayout_3.setStretch(1, 6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.grpCamera.setTitle(_translate("Form", "相机"))
        self.labDetectCamera.setText(_translate("Form", "无"))
        self.labLinkCamera.setText(_translate("Form", "未连接"))
        self.btnLinkCamera.setText(_translate("Form", "连接相机"))
        self.btnDetectCamera.setText(_translate("Form", "检测相机"))
        self.btnTestCamera.setText(_translate("Form", "测试相机"))
        self.label.setText(_translate("Form", "未开始测试"))
        self.btnCloseCamera.setText(_translate("Form", "关闭相机"))
        self.labCloseCamera.setText(_translate("Form", "无"))
        self.grpDetect.setTitle(_translate("Form", "检测"))
        self.btnStartDetect.setText(_translate("Form", "开始检测"))
        self.btnStopDetect.setText(_translate("Form", "停止检测"))
        self.btnSetParams.setText(_translate("Form", "设置参数"))
        self.grpTemp.setTitle(_translate("Form", "模板"))
        self.btnSelectTemp.setText(_translate("Form", "选择模板"))
        self.btnMakeTemp.setText(_translate("Form", "拍摄模板"))
        self.groupBox_2.setTitle(_translate("Form", "TCP连接"))
        self.labAdr.setText(_translate("Form", "本地主机地址"))
        self.labPort.setText(_translate("Form", "本地主机端口"))
        self.btnTCPOpen.setText(_translate("Form", "打开"))
        self.btnTCPClose.setText(_translate("Form", "关闭"))
        self.labTCP.setText(_translate("Form", "未开启"))
        self.groupBox_3.setTitle(_translate("Form", "继电器连接"))
        self.btnOpenRelay.setText(_translate("Form", "打开继电器"))
        self.btnCloseRelay.setText(_translate("Form", "关闭继电器"))
        self.labRelay.setText(_translate("Form", "未开启"))
        self.btnTestRelay.setText(_translate("Form", "测试继电器"))
        self.grpInput.setTitle(_translate("Form", "输入图片"))
        self.labInput.setText(_translate("Form", "无图片"))
        self.grpOuput.setTitle(_translate("Form", "匹配结果"))
        self.labOutput.setText(_translate("Form", "无结果"))
        self.groupBox.setTitle(_translate("Form", "结果"))
        self.label_2.setText(_translate("Form", "无"))


