# -*- coding: utf-8 -*-

import copy
import datetime
import gc
import os
import sys
import sqlite3
import cv2
import numpy

from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from ImageConvert import *
from MVSDK import *
from camera_lib import enumCameras, openCamera, closeCamera, setSoftTriggerConf, setExposureTime, grabOne
from myDialogMakeTemp import QmyDialogMakeTemp
from myDialogSetParams import QmyDialogSetParams
from ui_MainWidget import Ui_Form as Ui_Widget


##from PyQt5.QtWidgets import
##from PyQt5.QtGui import
##from PyQt5.QtSql import
##from PyQt5.QtMultimedia import
##from PyQt5.QtMultimediaWidgets import


class QmyWidget(QWidget):

   def __init__(self, parent=None):
      super().__init__(parent)  # 调用父类构造函数，创建窗体
      self.ui = Ui_Widget()  # 创建UI对象
      self.ui.setupUi(self)  # 构造UI界面

      self.camera_flag = False

      # 将一部分按钮设置成非使能状态
      self.ui.btnLinkCamera.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnCloseCamera.setEnabled(False)

      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnStopDetect.setEnabled(False)

      self.ui.btnMakeTemp.setEnabled(False)

      self.default_params = {
         'exposure_time': 10000,
         'trigger_delay': 1000000,
         'min_match_count': 10,
         'resize_times': 0.3,
         'max_matches': 500,
         'trees': 5,
         'checks': 50,
         'k': 2,
         'ratio': 0.9
      }

      if not os.path.exists('./config.ini'):
         self.settings = QSettings("./config.ini", QSettings.IniFormat)
         for param_name in self.default_params:
            self.settings.setValue(param_name, self.default_params[param_name])
      self.settings = QSettings("./config.ini", QSettings.IniFormat)


##  ==============自定义功能函数========================
   def do_testCamera(self):
      # 通用属性设置:设置触发模式为off --根据属性类型，直接构造属性节点。如触发模式是 enumNode，构造enumNode节点
      # 自由拉流：TriggerMode 需为 off
      trigModeEnumNode = pointer(GENICAM_EnumNode())
      trigModeEnumNodeInfo = GENICAM_EnumNodeInfo()
      trigModeEnumNodeInfo.pCamera = pointer(self.camera)
      trigModeEnumNodeInfo.attrName = b"TriggerMode"
      nRet = GENICAM_createEnumNode(byref(trigModeEnumNodeInfo), byref(trigModeEnumNode))
      if (nRet != 0):
         print("create TriggerMode Node fail!")
         # 释放相关资源
         # self.streamSource.contents.release(self.streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("构建节点出错")

         return

      nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
      if (nRet != 0):
         print("set TriggerMode value [Off] fail!")
         # 释放相关资源
         trigModeEnumNode.contents.release(trigModeEnumNode)
         # self.streamSource.contents.release(self.streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("设置触发模式出错")

         return

      # 需要释放Node资源
      trigModeEnumNode.contents.release(trigModeEnumNode)

      # 开始拉流
      nRet = self.streamSource.contents.startGrabbing(self.streamSource, c_ulonglong(0), \
                                                 c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
      if (nRet != 0):
         print("startGrabbing fail!")
         # 释放相关资源
         # self.streamSource.contents.release(self.streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("拉流出错")

         return

      self.isGrab = True

      while self.isGrab:
         # 主动取图
         frame = pointer(GENICAM_Frame())
         nRet = self.streamSource.contents.getFrame(self.streamSource, byref(frame), c_uint(1000))
         if (nRet != 0):
            print("getFrame fail! Timeout:[1000]ms")
            # 释放相关资源
            # self.streamSource.contents.release(self.streamSource)

            label = self.ui.label
            label.setStyleSheet('color: red')
            label.setText("主动取图出错")

            return
         else:
            print("getFrame success BlockId = [" + str(frame.contents.getBlockId(frame)) + "], get frame time: " + str(
               datetime.datetime.now()))

         nRet = frame.contents.valid(frame)
         if (nRet != 0):
            print("frame is invalid!")
            # 释放驱动图像缓存资源
            frame.contents.release(frame)
            # 释放相关资源
            # self.streamSource.contents.release(self.streamSource)

            label = self.ui.label
            label.setStyleSheet('color: red')
            label.setText("取帧出错")

            return

         # 给转码所需的参数赋值
         imageParams = IMGCNV_SOpenParam()
         imageParams.dataSize = frame.contents.getImageSize(frame)
         imageParams.height = frame.contents.getImageHeight(frame)
         imageParams.width = frame.contents.getImageWidth(frame)
         imageParams.paddingX = frame.contents.getImagePaddingX(frame)
         imageParams.paddingY = frame.contents.getImagePaddingY(frame)
         imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

         # 将裸数据图像拷出
         imageBuff = frame.contents.getImage(frame)
         userBuff = c_buffer(b'\0', imageParams.dataSize)
         memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)

         # 释放驱动图像缓存
         frame.contents.release(frame)

         # 如果图像格式是 Mono8 直接使用
         if imageParams.pixelForamt == EPixelType.gvspPixelMono8:
            grayByteArray = bytearray(userBuff)
            cvImage = numpy.array(grayByteArray).reshape(imageParams.height, imageParams.width)
         else:
            # 转码 => BGR24
            rgbSize = c_int()
            rgbBuff = c_buffer(b'\0', imageParams.height * imageParams.width * 3)

            nRet = IMGCNV_ConvertToBGR24(cast(userBuff, c_void_p), \
                                         byref(imageParams), \
                                         cast(rgbBuff, c_void_p), \
                                         byref(rgbSize))

            colorByteArray = bytearray(rgbBuff)
            cvImage = numpy.array(colorByteArray).reshape(imageParams.height, imageParams.width, 3)
         # --- end if ---

         cvImage = cv2.resize(cvImage, dsize=None, fx=0.3, fy=0.3, interpolation=cv2.INTER_LINEAR)  # 自己加的

         label = self.ui.label
         label.setStyleSheet('color: green')
         label.setText("测试相机中")

         self.ui.btnTestCamera.setEnabled(False)

         cv2.imshow("Test Camera", cvImage)
         gc.collect()

         if (cv2.waitKey(1) >= 0):
            self.isGrab = False
            break
            # --- end while ---

      cv2.destroyAllWindows()

      label = self.ui.label
      label.setStyleSheet('color: black')
      label.setText("未开始测试")

      # 停止拉流
      nRet = self.streamSource.contents.stopGrabbing(self.streamSource)
      if (nRet != 0):
         print("stopGrabbing fail!")
         # 释放相关资源
         self.streamSource.contents.release(self.streamSource)
         return


   def do_grabOne(self):
      nRet = setSoftTriggerConf(self.camera)
      if ( nRet != 0 ):
         return None

      exposure_time = self.settings.value('exposure_time')
      nRet = setExposureTime(self.camera, int(exposure_time))
      if ( nRet != 0 ):
         return None

      # 开始拉流
      nRet = self.streamSource.contents.startGrabbing(self.streamSource, c_ulonglong(0), \
                                                 c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
      if (nRet != 0):
         return None

      nRet = grabOne(self.camera)
      if ( nRet != 0 ):
         return None

      # 主动取图
      frame = pointer(GENICAM_Frame())
      nRet = self.streamSource.contents.getFrame(self.streamSource, byref(frame), c_uint(10000))
      if (nRet != 0):
         return None
      else:
         print("SoftTrigger getFrame success BlockId = " + str(frame.contents.getBlockId(frame)))
         print("get frame time: " + str(datetime.datetime.now()))

      nRet = frame.contents.valid(frame)
      if (nRet != 0):
         return None

         # 将裸数据图像拷出
      imageSize = frame.contents.getImageSize(frame)
      buffAddr = frame.contents.getImage(frame)
      frameBuff = c_buffer(b'\0', imageSize)
      memmove(frameBuff, c_char_p(buffAddr), imageSize)

      # 给转码所需的参数赋值
      convertParams = IMGCNV_SOpenParam()
      convertParams.dataSize = imageSize
      convertParams.height = frame.contents.getImageHeight(frame)
      convertParams.width = frame.contents.getImageWidth(frame)
      convertParams.paddingX = frame.contents.getImagePaddingX(frame)
      convertParams.paddingY = frame.contents.getImagePaddingY(frame)
      convertParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

      # 释放驱动图像缓存
      frame.contents.release(frame)

      # 如果图像格式是 Mono8 直接使用
      if convertParams.pixelForamt == EPixelType.gvspPixelMono8:
         grayByteArray = bytearray(frameBuff)
         cvImage = numpy.array(grayByteArray).reshape(convertParams.height, convertParams.width)
      else:
         # 转码 => BGR24
         rgbSize = c_int()
         rgbBuff = c_buffer(b'\0', convertParams.height * convertParams.width * 3)

         nRet = IMGCNV_ConvertToBGR24(cast(frameBuff, c_void_p), \
                                      byref(convertParams), \
                                      cast(rgbBuff, c_void_p), \
                                      byref(rgbSize))

         colorByteArray = bytearray(rgbBuff)
         cvImage = numpy.array(colorByteArray).reshape(convertParams.height, convertParams.width, 3)

      nRet = self.streamSource.contents.stopGrabbing(self.streamSource)
      if (nRet != 0):
         return None

      return cvImage


   def do_selectROI(self, image):
      dsize = 0.25
      rImage = cv2.resize(image, dsize=None, fx=dsize, fy=dsize, interpolation=cv2.INTER_LINEAR)
      min_x, min_y, w, h = cv2.selectROI('select_roi', rImage)
      if len(rImage.shape) == 3:
         nImage = image[int(min_y/dsize):int((min_y+h)/dsize), int(min_x/dsize):int((min_x+w)/dsize), :]
      else:
         nImage = image[int(min_y/dsize):int((min_y+h)/dsize), int(min_x/dsize):int((min_x+w)/dsize)]
      cv2.destroyAllWindows()

      return nImage


   def do_createDes(self, im1):
      des_dic = {}
      for i in range(1, 11):
         di = i * 0.1
         img1 = cv2.resize(im1, dsize=None, fx=di, fy=di, interpolation=cv2.INTER_LINEAR)
         # 直方图归一化，应对白色的头盔
         cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
         if len(img1.shape) == 3:
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

         # 初始化SIFT特征检测器
         sift = cv2.SIFT_create()

         # 使用特征检测器找特征点和描述子
         kp1, des1 = sift.detectAndCompute(img1, None)

         name = "descriptor_{}".format(str(i))
         des_dic[name] = copy.deepcopy(des1)

      return des_dic


   def do_sqlInsert(self, image, model, size, color, des_dic):
      if not os.path.exists('./helmetDB.db3'):
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "没有数据库文件")
         messageBox.exec()
         return -1
      conn = sqlite3.connect('helmetDB.db3')
      cursor = conn.cursor()

      sql = 'INSERT into helmet values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'

      x = [model, size, color, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), image.shape[1], image.shape[0],
           image.tobytes()]
      for index in des_dic:
         x.append(des_dic[index].tobytes())
      for i in x:
         print(type(i))
      cursor.execute(sql, x)
      conn.commit()
      cursor.close()
      conn.close()

      return 0


##  ==============event处理函数==========================


##  ==========由connectSlotsByName()自动连接的槽函数============
   # 检测相机
   @pyqtSlot()
   def on_btnDetectCamera_clicked(self):
      # 发现相机
      cameraCnt, cameraList = enumCameras()
      if cameraCnt is None:
         # 设置标签
         label = self.ui.labDetectCamera
         label.setStyleSheet('color: red')
         label.setText("检测不到相机")
      else:
         # 设置标签
         label = self.ui.labDetectCamera
         label.setStyleSheet('color: green')
         label.setText("检测到相机")
         # 显示相机信息
         for index in range(0, cameraCnt):
            camera = cameraList[index]
            print("\nCamera Id = " + str(index))
            print("Key           = " + str(camera.getKey(camera)))
            print("vendor name   = " + str(camera.getVendorName(camera)))
            print("Model  name   = " + str(camera.getModelName(camera)))
            print("Serial number = " + str(camera.getSerialNumber(camera)))
         self.camera = cameraList[0]

         # 连接相机按钮设为使能
         if not self.camera_flag:
            self.ui.btnLinkCamera.setEnabled(True)


   # 连接相机
   @pyqtSlot()
   def on_btnLinkCamera_clicked(self):
      nRet = openCamera(self.camera)
      if (nRet != 0):
         lab = self.ui.labLinkCamera
         lab.setStyleSheet('color: red')
         lab.setText("连接相机出错")
      else:
         # 创建流对象
         streamSourceInfo = GENICAM_StreamSourceInfo()
         streamSourceInfo.channelId = 0
         streamSourceInfo.pCamera = pointer(self.camera)

         self.streamSource = pointer(GENICAM_StreamSource())
         nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(self.streamSource))
         if (nRet != 0):
            lab = self.ui.labLinkCamera
            lab.setStyleSheet('color: red')
            lab.setText("连接相机出错")
         else:
            lab = self.ui.labLinkCamera
            lab.setStyleSheet('color: green')
            lab.setText("成功连接相机")

            # 按钮的使能和不使能
            self.ui.btnLinkCamera.setEnabled(False)
            # self.ui.btnDetectCamera.setEnabled(False)
            self.ui.btnTestCamera.setEnabled(True)
            self.ui.btnCloseCamera.setEnabled(True)
            self.ui.btnStartDetect.setEnabled(True)
            self.ui.btnMakeTemp.setEnabled(True)

            self.camera_flag = True


   # 测试相机
   @pyqtSlot()
   def on_btnTestCamera_clicked(self):
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnCloseCamera.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)

      self.do_testCamera()

      self.ui.btnTestCamera.setEnabled(True)
      self.ui.btnCloseCamera.setEnabled(True)
      self.ui.btnStartDetect.setEnabled(True)
      self.ui.btnMakeTemp.setEnabled(True)


   # 关闭相机
   @pyqtSlot()
   def on_btnCloseCamera_clicked(self):
      nRet = closeCamera(self.camera)
      if (nRet != 0):
         print("closeCamera fail")
         # 释放相关资源
         # self.streamSource.contents.release(self.streamSource)

         lab = self.ui.labCloseCamera
         lab.setStyleSheet('color: red')
         lab.setText("关闭相机出错")

         return

      # 释放相关资源
      self.streamSource.contents.release(self.streamSource)

      lab = self.ui.labLinkCamera
      lab.setStyleSheet('color: black')
      lab.setText("未连接")

      lab = self.ui.labCloseCamera
      lab.setStyleSheet('color: green')
      lab.setText("关闭相机成功")

      self.ui.btnCloseCamera.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnLinkCamera.setEnabled(True)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      self.camera_flag = False

   # 开始检测
   @pyqtSlot()
   def on_btnStartDetect_clicked(self):
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnStopDetect.setEnabled(True)
      self.ui.btnSetParams.setEnabled(False)
      self.ui.btnSelectTemp.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)

   # 停止检测
   @pyqtSlot()
   def on_btnStopDetect_clicked(self):
      if self.camera_flag:
         self.ui.btnStartDetect.setEnabled(True)
         self.ui.btnMakeTemp.setEnabled(True)
         self.ui.btnTestCamera.setEnabled(True)
      self.ui.btnStopDetect.setEnabled(False)
      self.ui.btnSetParams.setEnabled(True)
      self.ui.btnSelectTemp.setEnabled(True)


   # 设置参数
   @pyqtSlot()
   def on_btnSetParams_clicked(self):
      dialogSetParams = QmyDialogSetParams()
      dialogSetParams.set_default_params(self.default_params)
      dialogSetParams.set_init_params()
      ret = dialogSetParams.exec()

      if ret:
         new_params = dialogSetParams.get_new_params()
         self.settings = QSettings("./config.ini", QSettings.IniFormat)
         for param_name in new_params:
            self.settings.setValue(param_name, new_params[param_name])


   # 选择模板
   @pyqtSlot()
   def on_btnSelectTemp_clicked(self):
      print("选择模板")

   # 拍摄模板
   @pyqtSlot()
   def on_btnMakeTemp_clicked(self):
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)

      image = self.do_grabOne()
      if image is None:
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "请重试")
         messageBox.exec()

      nImage = self.do_selectROI(image)
      if len(nImage) != 0:
         des_dic = self.do_createDes(nImage)

         dialogMakeTemp = QmyDialogMakeTemp()
         dialogMakeTemp.get_image(nImage)
         dialogMakeTemp.show_image()
         ret = dialogMakeTemp.exec()
         while ret and (dialogMakeTemp.ui.lineEditColor.text()=="" or dialogMakeTemp.ui.lineEditModel.text()==""):
            messageBox = QMessageBox(QMessageBox.Warning, "warning", "请填写型号和颜色")
            messageBox.exec()
            ret = dialogMakeTemp.exec()
         if ret:
            model = dialogMakeTemp.ui.lineEditModel.text()
            size = dialogMakeTemp.ui.comboBoxSize.currentText()
            color = dialogMakeTemp.ui.lineEditColor.text()

            ret = self.do_sqlInsert(nImage, model, size, color, des_dic)

            if ret == 0:
               # messageBox = QMessageBox(QMessageBox.about, "ok", "数据库插入成功")
               QMessageBox.about(self, 'about', '数据库插入成功')
               # messageBox.exec()


      if self.camera_flag:
         self.ui.btnTestCamera.setEnabled(True)
         self.ui.btnMakeTemp.setEnabled(True)
         self.ui.btnStartDetect.setEnabled(True)

##  =============自定义槽函数===============================


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序

   form = QmyWidget()  # 创建窗体
   form.show()

   sys.exit(app.exec_())
