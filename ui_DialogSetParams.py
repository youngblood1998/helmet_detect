# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogSetParams.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(463, 697)
        Dialog.setMinimumSize(QtCore.QSize(463, 697))
        Dialog.setMaximumSize(QtCore.QSize(463, 697))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.formLayout = QtWidgets.QFormLayout(self.frame_2)
        self.formLayout.setObjectName("formLayout")
        self.labExposureTime = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labExposureTime.sizePolicy().hasHeightForWidth())
        self.labExposureTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.labExposureTime.setFont(font)
        self.labExposureTime.setTextFormat(QtCore.Qt.AutoText)
        self.labExposureTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labExposureTime.setObjectName("labExposureTime")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labExposureTime)
        self.spinBoxExposureTime = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxExposureTime.sizePolicy().hasHeightForWidth())
        self.spinBoxExposureTime.setSizePolicy(sizePolicy)
        self.spinBoxExposureTime.setMaximum(1000000)
        self.spinBoxExposureTime.setObjectName("spinBoxExposureTime")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxExposureTime)
        self.spinBoxTriggerDelay = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxTriggerDelay.sizePolicy().hasHeightForWidth())
        self.spinBoxTriggerDelay.setSizePolicy(sizePolicy)
        self.spinBoxTriggerDelay.setMaximum(1000000)
        self.spinBoxTriggerDelay.setObjectName("spinBoxTriggerDelay")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxTriggerDelay)
        self.labTriggerDelay = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labTriggerDelay.sizePolicy().hasHeightForWidth())
        self.labTriggerDelay.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labTriggerDelay.setFont(font)
        self.labTriggerDelay.setTextFormat(QtCore.Qt.AutoText)
        self.labTriggerDelay.setAlignment(QtCore.Qt.AlignCenter)
        self.labTriggerDelay.setObjectName("labTriggerDelay")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labTriggerDelay)
        self.labMinMatchCount = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labMinMatchCount.sizePolicy().hasHeightForWidth())
        self.labMinMatchCount.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labMinMatchCount.setFont(font)
        self.labMinMatchCount.setAlignment(QtCore.Qt.AlignCenter)
        self.labMinMatchCount.setObjectName("labMinMatchCount")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labMinMatchCount)
        self.labResizeTime = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labResizeTime.sizePolicy().hasHeightForWidth())
        self.labResizeTime.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labResizeTime.setFont(font)
        self.labResizeTime.setAlignment(QtCore.Qt.AlignCenter)
        self.labResizeTime.setObjectName("labResizeTime")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labResizeTime)
        self.labMaxMatches = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labMaxMatches.sizePolicy().hasHeightForWidth())
        self.labMaxMatches.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labMaxMatches.setFont(font)
        self.labMaxMatches.setAlignment(QtCore.Qt.AlignCenter)
        self.labMaxMatches.setObjectName("labMaxMatches")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labMaxMatches)
        self.labTree = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labTree.sizePolicy().hasHeightForWidth())
        self.labTree.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labTree.setFont(font)
        self.labTree.setAlignment(QtCore.Qt.AlignCenter)
        self.labTree.setObjectName("labTree")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.labTree)
        self.labChecks = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labChecks.sizePolicy().hasHeightForWidth())
        self.labChecks.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labChecks.setFont(font)
        self.labChecks.setAlignment(QtCore.Qt.AlignCenter)
        self.labChecks.setObjectName("labChecks")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.labChecks)
        self.labRatio = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labRatio.sizePolicy().hasHeightForWidth())
        self.labRatio.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labRatio.setFont(font)
        self.labRatio.setAlignment(QtCore.Qt.AlignCenter)
        self.labRatio.setOpenExternalLinks(False)
        self.labRatio.setObjectName("labRatio")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.labRatio)
        self.labK = QtWidgets.QLabel(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labK.sizePolicy().hasHeightForWidth())
        self.labK.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labK.setFont(font)
        self.labK.setTextFormat(QtCore.Qt.AutoText)
        self.labK.setAlignment(QtCore.Qt.AlignCenter)
        self.labK.setObjectName("labK")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.labK)
        self.spinBoxMinMatchCount = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMinMatchCount.sizePolicy().hasHeightForWidth())
        self.spinBoxMinMatchCount.setSizePolicy(sizePolicy)
        self.spinBoxMinMatchCount.setObjectName("spinBoxMinMatchCount")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.spinBoxMinMatchCount)
        self.doubleSpinBoxResizeTimes = QtWidgets.QDoubleSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxResizeTimes.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxResizeTimes.setSizePolicy(sizePolicy)
        self.doubleSpinBoxResizeTimes.setDecimals(1)
        self.doubleSpinBoxResizeTimes.setMaximum(1.0)
        self.doubleSpinBoxResizeTimes.setSingleStep(0.1)
        self.doubleSpinBoxResizeTimes.setObjectName("doubleSpinBoxResizeTimes")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxResizeTimes)
        self.spinBoxMaxMatches = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMaxMatches.sizePolicy().hasHeightForWidth())
        self.spinBoxMaxMatches.setSizePolicy(sizePolicy)
        self.spinBoxMaxMatches.setMaximum(10000)
        self.spinBoxMaxMatches.setObjectName("spinBoxMaxMatches")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinBoxMaxMatches)
        self.spinBoxTree = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxTree.sizePolicy().hasHeightForWidth())
        self.spinBoxTree.setSizePolicy(sizePolicy)
        self.spinBoxTree.setMaximum(10)
        self.spinBoxTree.setObjectName("spinBoxTree")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBoxTree)
        self.spinBoxChecks = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxChecks.sizePolicy().hasHeightForWidth())
        self.spinBoxChecks.setSizePolicy(sizePolicy)
        self.spinBoxChecks.setMaximum(100)
        self.spinBoxChecks.setObjectName("spinBoxChecks")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBoxChecks)
        self.doubleSpinBoxRatio = QtWidgets.QDoubleSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBoxRatio.sizePolicy().hasHeightForWidth())
        self.doubleSpinBoxRatio.setSizePolicy(sizePolicy)
        self.doubleSpinBoxRatio.setMaximum(1.0)
        self.doubleSpinBoxRatio.setSingleStep(0.01)
        self.doubleSpinBoxRatio.setObjectName("doubleSpinBoxRatio")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxRatio)
        self.spinBoxK = QtWidgets.QSpinBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxK.sizePolicy().hasHeightForWidth())
        self.spinBoxK.setSizePolicy(sizePolicy)
        self.spinBoxK.setMaximum(10)
        self.spinBoxK.setObjectName("spinBoxK")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spinBoxK)
        self.verticalLayout.addWidget(self.frame_2)
        self.btnDefault = QtWidgets.QPushButton(Dialog)
        self.btnDefault.setObjectName("btnDefault")
        self.verticalLayout.addWidget(self.btnDefault)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout.setStretch(0, 9)
        self.verticalLayout.setStretch(2, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labExposureTime.setText(_translate("Dialog", "曝光时间(0~10000000μs)"))
        self.labTriggerDelay.setText(_translate("Dialog", "延迟时间(μs)"))
        self.labMinMatchCount.setText(_translate("Dialog", "最小匹配数"))
        self.labResizeTime.setText(_translate("Dialog", "图片缩小倍数"))
        self.labMaxMatches.setText(_translate("Dialog", "最大特征点数"))
        self.labTree.setText(_translate("Dialog", "tree"))
        self.labChecks.setText(_translate("Dialog", "checks"))
        self.labRatio.setText(_translate("Dialog", "ratio"))
        self.labK.setText(_translate("Dialog", "k"))
        self.btnDefault.setText(_translate("Dialog", "恢复默认值"))


