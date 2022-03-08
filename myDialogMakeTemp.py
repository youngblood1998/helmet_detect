# -*- coding: utf-8 -*-

import sys
import numpy
import cv2
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog

##from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

##from PyQt5.QtWidgets import

##from PyQt5.QtGui import

##from PyQt5.QtSql import

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import


from ui_DialogMakeTemp import Ui_Dialog


class QmyDialogMakeTemp(QDialog):
   def __init__(self, parent=None):
      super().__init__(parent)  # 调用父类构造函数，创建窗体
      self.ui = Ui_Dialog()  # 创建UI对象
      self.ui.setupUi(self)  # 构造UI界面

##  ============自定义功能函数========================
   # 获得图片
   def get_image(self, image):
      self.image = image


   # 展示图片
   def show_image(self):
      image = self.image
      # image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
      print(image.shape)

      # if float(H)/h > float(W)/w:
      #    image = cv2.resize(image, dsize=None, fx=float(W)/w, fy=float(W)/w)
      # else:
      #    image = cv2.resize(image, dsize=None, fx=float(H)/h, fy=float(H)/h)

      # if len(image.shape) == 3:
      #    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      # else:
      #    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

      qt_image = QtGui.QImage(image.data.tobytes(),
                              image.shape[1],
                              image.shape[0],
                              image.shape[1]*3,
                              QtGui.QImage.Format.Format_RGB888)

      w = image.shape[1]
      h = image.shape[0]
      W = self.ui.labTemp.size().width()
      H = self.ui.labTemp.size().height()

      if float(H)/h > float(W)/w:
         self.ui.labTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
      else:
         self.ui.labTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))


##  ===========event处理函数==========================


##  ========由connectSlotsByName()自动连接的槽函数=========


##  ==========自定义槽函数===============================


##  ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序
   form = QmyDialogMakeTemp()  # 创建窗体
   form.show()
   sys.exit(app.exec_())
