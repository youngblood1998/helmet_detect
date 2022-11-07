# -*- coding: utf-8 -*-

# import copy
import copy
import ctypes
import time
import datetime
import gc
import os
import sys
import sqlite3
# import time
import cv2
import numpy
import csv
from socket import *

from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QSettings, QThread, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

from ImageConvert import *
from MVSDK import *
from camera_lib import enumCameras, openCamera, closeCamera, setSoftTriggerConf, setExposureTime,  \
   setLineTriggerConf
# from detect_lib.sift_flann_new import SiftFlann
from detect_lib.surf_bf_new import SurfBf
from detect_lib.draw_line import drawline, drawgrid
from detect_lib.remove_background import remove_bg
from relay_lib import init_relay, close_relay, test_delay, export_relay, export_arr_relay
# from detect_lib.hist_compare import hist_compare
from myDialogMakeTemp import QmyDialogMakeTemp
from myDialogSetParams import QmyDialogSetParams
from myDialogSelectTemp import QmyDialogSelectTemp
from ui_MainWidget import Ui_Form as Ui_Widget


##from PyQt5.QtWidgets import
##from PyQt5.QtGui import
##from PyQt5.QtSql import
##from PyQt5.QtMultimedia import
##from PyQt5.QtMultimediaWidgets import

# TCP线程
class Runthread(QThread):
   #  通过类成员对象定义信号对象
   signal = pyqtSignal(int)

   def __init__(self, tcp_server_socket):
      super(Runthread, self).__init__()
      self.tcp_server_socket = tcp_server_socket
      self.client_socket = None

   def __del__(self):
      try:
         self.wait()
      except:
         pass

   def run(self):
      try:
         self.client_socket, ip_port = self.tcp_server_socket.accept()
         self.signal.emit(1)
      except:
         return

   def pause(self):
      if self.client_socket:
         self.client_socket.close()
         self.client_socket = None
         self.tcp_server_socket.close()
      else:
         self.tcp_server_socket.close()

   def send(self, string):
      if self.client_socket:
         self.client_socket.send(string.encode('utf-8'))


# 继电器测试的线程
class Relaythread(QThread):
   #  通过类成员对象定义信号对象
   signal_1 = pyqtSignal(int)

   def __init__(self, relay_dic):
      super(Relaythread, self).__init__()
      self.relay_dic = relay_dic

   def __del__(self):
      try:
         self.wait()
      except:
         pass

   def run(self):
      try:
         # 测试继电器
         test_delay(self.relay_dic)
         self.signal_1.emit(1)
      except:
         return


# 继电器触发的线程
class RelayExport_thread(QThread):
   def __init__(self, relay_dic):
      super(RelayExport_thread, self).__init__()
      self.relay_dic = relay_dic

   def __del__(self):
      try:
         self.wait()
      except:
         pass

   def run(self):
      try:
         self.wait()
      except:
         return

   def export(self, port, t):
      # 继电器输出
      export_relay(self.relay_dic, port, t)

   def export_arr(self, port_arr, t):
      # 继电器多端口输出
      export_arr_relay(self.relay_dic, port_arr, t)


# # 触发间隔的线程
# class Interval_thread(QThread):
#    #  通过类成员对象定义信号对象
#    signal_2 = pyqtSignal(int)
#
#    def __init__(self):
#       super(Interval_thread, self).__init__()
#
#    def __del__(self):
#       try:
#          self.wait()
#       except:
#          pass
#
#    def run(self):
#       try:
#          self.wait()
#       except:
#          return
#
#    def sleep(self, t):
#       time.sleep(t)
#       self.signal_2.emit(1)


class QmyWidget(QWidget):

   interval_signal = pyqtSignal(int)

   def __init__(self, parent=None):
      super().__init__(parent)  # 调用父类构造函数，创建窗体
      self.ui = Ui_Widget()  # 创建UI对象
      self.ui.setupUi(self)  # 构造UI界面

      self.camera_flag = False   # 相机开关标志
      self.detect_flag = False   # 检测开关标志
      self.tcp_flag = False      # TCP连接标志
      self.relay_flag = False    # 继电器连接标志
      self.interval_flag = False    # 触发间隔标志
      self.ignore_flag = False      # 是否忽略颜色

      # 将一部分按钮设置成非使能状态
      self.ui.btnLinkCamera.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnCloseCamera.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnStopDetect.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnTCPClose.setEnabled(False)
      self.ui.btnCloseRelay.setEnabled(False)
      self.ui.btnTestRelay.setEnabled(False)
      default_ip = gethostbyname(gethostname())    # 本机ip地址
      self.ui.lineEditAdr.setText(default_ip)
      self.ui.lineEditPort.setText("8080")

      # 默认参数
      self.fixed_params = {
         'exposure_time': 19000,
         'trigger_delay': 1000000,
         'interval_time': 2,
         'delay_time': 0.5,
         'min_match_count': 5,
         'resize_times': 0.1,
         'max_matches': 500,
         'hist1': 0.0,
         'hist2': 0.4,
         'area': 1.25,
         'R': 80,
         'G': 120,
         'B': 120,
         'bg_thresh':8000,
         'trees': 5,
         'checks': 50,
         'k': 2,
         'ratio': 0.9
      }

      self.select_temp = []   # 选择的模板
      self.temp_arr = []   # 选择的模板(包含关键点和描述子)
      # self.temp_arr_ignore = {}  # 忽略颜色时的模板数组
      # self.temp_arr_ignore_index = {}
      self.mythread = None
      # self.interval_thread = None
      self.interval_signal.connect(self.do_interval_set_true)
      self.num = 0      # 继电器端口数

      # 有无默认配置文件，没有的话创建并设置默认参数
      if not os.path.exists('./defaultConfig.ini'):
         self.default_settings = QSettings("./defaultConfig.ini", QSettings.IniFormat)
         for param_name in self.fixed_params:
            self.default_settings.setValue(param_name, self.fixed_params[param_name])
      self.default_settings = QSettings("./defaultConfig.ini", QSettings.IniFormat)

      # 有无配置文件，没有的话创建并设置参数
      if not os.path.exists('./config.ini'):
         self.settings = QSettings("./config.ini", QSettings.IniFormat)
         for param_name in self.fixed_params:
            self.settings.setValue(param_name, self.default_settings.value(param_name))
      self.settings = QSettings("./config.ini", QSettings.IniFormat)

      # 相机回调函数
      self.GrabbingFrameCallbackFuncEx = callbackFuncEx(self.test_callback)
      self.UnGrabbingFrameCallbackFuncEx = callbackFuncEx(self.test_callback)

      # 打开软件时打开继电器
      self.on_btnOpenRelay_clicked()

##  ==============自定义功能函数========================
   # 输出csv文件
   def write_csv(self, model, size, color, ok, x, y, angle, imageDraw, area2, area1):
      try:
         print(angle)
         angle = angle * 180 // numpy.pi
         print(angle)
         # 先查看有无文件夹，没有就创建
         if not os.path.exists("../records/"):
            os.mkdir("../records/")

         # 先查看有无文件夹，没有就创建
         if not os.path.exists("../records/" + str(datetime.date.today())):
            os.mkdir("../records/" + str(datetime.date.today()))

         # 根据日期创建csv文件并写入表头
         if not os.path.isfile("../records/" + str(datetime.date.today()) + ".csv"):
            with open("../records/" + str(datetime.date.today()) + ".csv", 'w', newline='') as file:
               writer = csv.writer(file)
               writer.writerow(["", "型号", "尺寸", "颜色", "时间", "OK", "NG", "总数", "X位置", "Y位置", "角度", "实际面积", "模板面积"])

         # 打开csv文件获取相关信息
         with open("../records/" + str(datetime.date.today()) + ".csv", 'r', newline='') as file:
            reader = csv.reader(file)
            reader_list = list(reader)
            length = len(reader_list)
            last_row = reader_list[-1]

         # 写入csv文件
         with open("../records/" + str(datetime.date.today()) + ".csv", "a", newline='') as file:
            writer = csv.writer(file)
            if length == 1:
               if ok:
                  writer.writerow([1, model, size, color, datetime.datetime.now().strftime('%H:%M:%S'),
                                   1, 0, 1, x, y, angle, area2, area1])
               else:
                  writer.writerow([1, "", "", "", datetime.datetime.now().strftime('%H:%M:%S'),
                                   0, 1, 1, 0, 0, 0, 0, 0])
            else:
               if ok:
                  writer.writerow([int(last_row[0]) + 1, model, size, color,
                                   datetime.datetime.now().strftime('%H:%M:%S'), int(last_row[5]) + 1,
                                   last_row[6], int(last_row[7]) + 1, x, y, angle, area2, area1])
               else:
                  writer.writerow([int(last_row[0]) + 1, "", "", "",
                                   datetime.datetime.now().strftime('%H:%M:%S'), last_row[5],
                                   int(last_row[6]) + 1, int(last_row[7]) + 1, 0, 0, 0, 0, 0])
         # 保存图片
         image = cv2.resize(imageDraw, dsize=(134, 73), interpolation=cv2.INTER_LINEAR)
         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
         if last_row[0] == '':
            cv2.imwrite("../records/" + str(datetime.date.today()) + "/" + str(1) + ".png", image)
         else:
            cv2.imwrite("../records/" + str(datetime.date.today()) + "/" + str(int(last_row[0]) + 1) + ".png", image)
      except Exception as e:
         QMessageBox.warning(self, "错误", "打开csv文件时系统无法保存数据！")


   # 软触发得到一张图，用于创建模板
   def grabOne(self):
      # 创建control节点
      acqCtrlInfo = GENICAM_AcquisitionControlInfo()
      acqCtrlInfo.pCamera = pointer(self.camera)
      acqCtrl = pointer(GENICAM_AcquisitionControl())
      nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
      if (nRet != 0):
         print("create AcquisitionControl fail!")
         return -1

      # 执行一次软触发
      trigSoftwareCmdNode = acqCtrl.contents.triggerSoftware(acqCtrl)
      nRet = trigSoftwareCmdNode.execute(byref(trigSoftwareCmdNode))
      if (nRet != 0):
         print("Execute triggerSoftware fail!")
         # 释放相关资源
         trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
         acqCtrl.contents.release(acqCtrl)
         return -1

      # 释放相关资源
      trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
      acqCtrl.contents.release(acqCtrl)
      return 0


   # 回调函数，用于检测
   def test_callback(self, frame, userInfo):
      # self.interval_thread.sleep(int(self.settings.value('interval_time')))

      nRet = frame.contents.valid(frame)
      if (nRet != 0):
         print("frame is invalid!")
         # 释放驱动图像缓存资源
         frame.contents.release(frame)
         return -1

      print("BlockId = %d userInfo = %s" % (frame.contents.getBlockId(frame), c_char_p(userInfo).value))

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

      # 释放驱动图像缓存资源
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

      print("触发传感器")
      # 判断是否在间隔时间内，是则不执行检测
      if not self.interval_flag:
         print("进行检测")
         self.interval_signal.emit(1)

         # 格式转换
         if len(cvImage.shape) == 3:
            cvtImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
         else:
            cvtImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB)

         # 显示输入
         try:
            qt_image = QtGui.QImage(cvtImage.data,
                                    cvtImage.shape[1],
                                    cvtImage.shape[0],
                                    cvtImage.shape[1] * 3,
                                    QtGui.QImage.Format.Format_RGB888)

            w = cvtImage.shape[1]   # 图像宽度
            h = cvtImage.shape[0]   # 图像高度
            W = self.ui.labInput.size().width()    # 显示框的宽度
            H = self.ui.labInput.size().height()   # 显示框的高度

            # 自适应图像宽高
            if float(H) / h > float(W) / w:
               self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
            else:
               self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
         except Exception as e:
            QMessageBox.warning(self, "警告", "图片输入出错")

         # 清空输入图像和输出图像
         self.ui.labOutput.clear()
         self.ui.label_2.clear()

         # # 检测
         # sift = SiftFlann(min_match_count=int(self.settings.value("min_match_count")),
         #                  resize_times=float(self.settings.value("resize_times")),
         #                  max_matches=int(self.settings.value("max_matches")),
         #                  trees=int(self.settings.value("trees")),
         #                  checks=int(self.settings.value("checks")),
         #                  k=int(self.settings.value("k")),
         #                  ratio=float(self.settings.value("ratio"))
         #                  )
         # # kp2, des2 = self.do_createDes(cvtImage)
         # # 返回结果，模板、方向、画出匹配框的图像
         # result, dir, imageDraw, angle, x, y = sift.match(self.temp_arr, cvtImage)

         # 检测
         surf = SurfBf(min_match_count=int(self.settings.value("min_match_count")),
                          resize_times=float(self.settings.value("resize_times")),
                          max_matches=int(self.settings.value("max_matches")),
                          trees=int(self.settings.value("trees")),
                          checks=int(self.settings.value("checks")),
                          k=int(self.settings.value("k")),
                          ratio=float(self.settings.value("ratio")),
                          hist2=float(self.settings.value("hist2")), area=float(self.settings.value("area")),
                          bg_color=(int(self.settings.value("R")), int(self.settings.value("G")), int(self.settings.value("B"))),
                          bg_thresh=int(self.settings.value("bg_thresh"))
                          )
         # kp2, des2 = self.do_createDes(cvtImage)
         #
         # # 直方图对比过滤模板
         # if len(cvImage.shape) == 3:
         #    resize_cvtImage = cv2.resize(cvtImage, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
         #    height = resize_cvtImage.shape[0]
         #    width = resize_cvtImage.shape[1]
         #    resize_cvtImage = resize_cvtImage[int(height*0.4):int(height*0.6),int(width*0.4):int(width*0.6),:]
         #    detect_temp_arr = []
         #    for detect_temp in self.temp_arr:
         #       resize_detect_temp = cv2.resize(detect_temp['image'], dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
         #       match = hist_compare(resize_cvtImage, resize_detect_temp)
         #       if match > float(self.settings.value('hist1')):
         #          detect_temp_arr.append(detect_temp)
         # else:
         #    detect_temp_arr = self.temp_arr
         #
         # # 返回结果，模板、方向、画出匹配框的图像
         # result, dir, imageDraw, angle, x, y = surf.match(detect_temp_arr, cvtImage)
         result, dir, imageDraw, angle, x, y, area2, area1 = surf.match(self.temp_arr, cvtImage, self.ignore_flag)

         # # 左右反转再检测,似乎有一点效果
         # if (angle > 0.2 and angle < numpy.pi/2-0.2) or (angle > -numpy.pi+0.2 and angle < -numpy.pi/2-0.2):
         #    cvtImage_flip = cv2.flip(cvtImage, 1)
         #    result, dir_useless, imageDraw_useless, angle_useless, x_useless, y_useless = surf.match(self.temp_arr, cvtImage_flip, self.ignore_flag)

         # # 旋转到与模板同一角度再检测
         # if (angle > 0.2 and angle < numpy.pi - 0.2) or (angle > -numpy.pi + 0.2 and angle < - 0.2):
         #
         #    rows, cols = cvtImage.shape[:2]
         #    center = (cols / 2, rows / 2)
         #    angle_ = int(angle*180/numpy.pi)
         #    scale = 1
         #
         #    M = cv2.getRotationMatrix2D(center, angle_, scale)
         #    cvtImage_rotate = cv2.warpAffine(src=cvtImage, M=M, dsize=None, borderValue=(0, 0, 0))
         #    result, dir_useless, imageDraw_useless, angle_useless, x_useless, y_useless = surf.match(self.temp_arr, cvtImage_rotate, self.ignore_flag)

         # 匹配结果不为空，则显示输入输出图像
         if not result is None:
            print("匹配结果:" + result["model"] + result["size"])
            print("\n")
            # 显示画出匹配框的图像
            try:
               qt_image = QtGui.QImage(imageDraw.data,
                                       imageDraw.shape[1],
                                       imageDraw.shape[0],
                                       imageDraw.shape[1] * 3,
                                       QtGui.QImage.Format.Format_RGB888)

               w = imageDraw.shape[1]
               h = imageDraw.shape[0]
               W = self.ui.labInput.size().width()
               H = self.ui.labInput.size().height()

               if float(H) / h > float(W) / w:
                  self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
               else:
                  self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
            except Exception as e:
               QMessageBox.warning(self, "警告", "图片输入出错")
            # 显示输出图像
            image = result["image"]
            try:
               qt_image = QtGui.QImage(image.data,
                                       image.shape[1],
                                       image.shape[0],
                                       image.shape[1] * 3,
                                       QtGui.QImage.Format.Format_RGB888)

               w = image.shape[1]
               h = image.shape[0]
               W = self.ui.labOutput.size().width()
               H = self.ui.labOutput.size().height()

               if float(H) / h > float(W) / w:
                  self.ui.labOutput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
               else:
                  self.ui.labOutput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
            except Exception as e:
               QMessageBox.warning(self, "警告", "图片输入出错")

            # 显示输出信息
            label = self.ui.label_2
            label.setStyleSheet('color: green')
            s = "前" if dir==0 else "后"
            label.setText("型号："+result["model"]+"；\t尺寸："+result["size"]+"；\t方向："+str(s))
            # self.ui.label_2.setText("型号："+result["model"]+"；尺寸:"+result["size"]+"；方向："+angle)
            # 写入csv
            self.write_csv(result["model"], result["size"], result["color"], True, x, y, angle, imageDraw)
            # 传输数据
            if self.mythread:
               string = result["model"]+";"+result["size"]+";"+result["color"]+";"+str(dir)+";"+str(x)+";"+str(y)+";"+str(angle)
               self.mythread.send(string)
            # 继电器输出
            # if self.relay_flag:
            #    self.relay_export_thread.export(result["port"], float(self.settings.value("delay_time")))
               # export_relay(self.relay_dic, result["port"])
            if (dir == 0 and result["forward"] == 1) or (dir == 1 and result["backward"] == 1):
               if self.relay_flag:
                  # 判断是否多端口同时输出
                  if int(result["check"]) == 0:
                     if result["port_index"] < len(result["port"]):
                        while result["port"][result["port_index"]] > self.num and result["port_index"] < len(
                              result["port"]):
                           result["port_index"] = result["port_index"] + 1
                        if result["port_index"] < len(result["port"]):
                           text = str(label.text()) + "；\t输出端口：" + str(result["port"][result["port_index"]])
                           label.setText(text)
                           self.relay_export_thread.export(result["port"][result["port_index"]],
                                                           float(self.settings.value("delay_time")))
                           result["port_index"] = result["port_index"] + 1
                        if result["port_index"] >= len(result["port"]):
                           result["port_index"] = 0
                  else:
                     text = str(label.text()) + "；\t输出端口：" + str(result["port"])
                     label.setText(text)
                     self.relay_export_thread.export_arr(result["port"], float(self.settings.value("delay_time")))
                  # # 是否忽略颜色
                  # if self.ignore_flag:
                  #    if int(result["check"]) == 0:
                  #       name = result["model"]+result["size"]
                  #       if self.temp_arr_ignore_index[name] < len(self.temp_arr_ignore[name]):
                  #          while self.temp_arr_ignore[name][self.temp_arr_ignore_index[name]] > self.num and self.temp_arr_ignore_index[name] < len(self.temp_arr_ignore[name]):
                  #             self.temp_arr_ignore_index[name] = self.temp_arr_ignore_index[name]+1
                  #          if self.temp_arr_ignore_index[name] < len(self.temp_arr_ignore[name]):
                  #             text = str(label.text()) + "；\t输出端口：" + str(self.temp_arr_ignore[name][self.temp_arr_ignore_index[name]])
                  #             label.setText(text)
                  #             self.relay_export_thread.export(self.temp_arr_ignore[name][self.temp_arr_ignore_index[name]], float(self.settings.value("delay_time")))
                  #             self.temp_arr_ignore_index[name] = self.temp_arr_ignore_index[name]+1
                  #          if self.temp_arr_ignore_index[name] >= len(self.temp_arr_ignore[name]):
                  #             self.temp_arr_ignore_index[name] = 0
                  #    else:
                  #       self.relay_export_thread.export_arr(self.temp_arr_ignore[result["model"]+result["size"]], float(self.settings.value("delay_time")))
                  # else:
                  #    # 判断是否多端口同时输出
                  #    if int(result["check"]) == 0:
                  #       if result["port_index"] < len(result["port"]):
                  #          while result["port"][result["port_index"]] > self.num and result["port_index"] < len(result["port"]):
                  #             result["port_index"] = result["port_index"]+1
                  #          if result["port_index"] < len(result["port"]):
                  #             text = str(label.text()) + "；\t输出端口：" + str(result["port"][result["port_index"]])
                  #             label.setText(text)
                  #             self.relay_export_thread.export(result["port"][result["port_index"]], float(self.settings.value("delay_time")))
                  #             result["port_index"] = result["port_index"]+1
                  #          if result["port_index"] >= len(result["port"]):
                  #             result["port_index"] = 0
                  #    else:
                  #       self.relay_export_thread.export_arr(result["port"], float(self.settings.value("delay_time")))
         else:
            label = self.ui.label_2
            label.setStyleSheet('color: red')
            self.ui.label_2.setText("无匹配结果")
            # 写入csv
            self.write_csv("", "", "", False, 0, 0, 0, imageDraw)
            # 传输数据
            if self.mythread:
               string = ";" + ";" + ";" + str(-1) + ";" + str(0) + ";" + str(0) + ";" + str(0)
               self.mythread.send(string)
            # # 继电器输出
            # if self.relay_flag:
            #    self.relay_export_thread.export(self.num, float(self.settings.value("delay_time")))
               # export_relay(self.relay_dic, self.num)
         gc.collect()


   # 测试相机
   def do_testCamera(self):
      # 创建流对象
      streamSourceInfo = GENICAM_StreamSourceInfo()
      streamSourceInfo.channelId = 0
      streamSourceInfo.pCamera = pointer(self.camera)

      streamSource = pointer(GENICAM_StreamSource())
      nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))

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
         streamSource.contents.release(streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("构建节点出错，请重试")

         return

      nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
      if (nRet != 0):
         print("set TriggerMode value [Off] fail!")
         # 释放相关资源
         trigModeEnumNode.contents.release(trigModeEnumNode)
         streamSource.contents.release(streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("设置触发模式出错，请重试")

         return

      # 需要释放Node资源
      trigModeEnumNode.contents.release(trigModeEnumNode)

      # 开始拉流
      nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0), \
                                                 c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
      if (nRet != 0):
         print("startGrabbing fail!")
         # 释放相关资源
         streamSource.contents.release(streamSource)

         label = self.ui.label
         label.setStyleSheet('color: red')
         label.setText("拉流出错，请重试")

         return

      self.isGrab = True

      while self.isGrab:
         # 主动取图
         frame = pointer(GENICAM_Frame())
         nRet = streamSource.contents.getFrame(streamSource, byref(frame), c_uint(1000))
         if (nRet != 0):
            print("getFrame fail! Timeout:[1000]ms")
            # 释放相关资源
            streamSource.contents.release(streamSource)

            label = self.ui.label
            label.setStyleSheet('color: red')
            label.setText("主动取图出错，请重试")

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
            streamSource.contents.release(streamSource)

            label = self.ui.label
            label.setStyleSheet('color: red')
            label.setText("取帧出错，请重试")

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

            if (nRet != 0):
               print("image convert fail! errorCode = " + str(nRet))
               label = self.ui.label
               label.setStyleSheet('color: red')
               label.setText("图像转换出错，请重试")
               # 释放相关资源
               streamSource.contents.release(streamSource)
               return -1

            colorByteArray = bytearray(rgbBuff)
            cvImage = numpy.array(colorByteArray).reshape(imageParams.height, imageParams.width, 3)
         # --- end if ---

         # 将相机内容缩小显示
         cvImage = cv2.resize(cvImage, dsize=None, fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)

         # # 格式转换
         # if len(cvImage.shape) == 3:
         #    cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
         # else:
         #    cvImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB)
         # 格式转换
         if len(cvImage.shape) == 3:
            pass
         else:
            cvImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2BGR)

         label = self.ui.label
         label.setStyleSheet('color: green')
         label.setText("测试相机中")

         self.ui.btnTestCamera.setEnabled(False)

         # 画网格
         drawgrid(cvImage, 2)

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
      nRet = streamSource.contents.stopGrabbing(streamSource)
      if (nRet != 0):
         print("stopGrabbing fail!")
         streamSource.contents.release(streamSource)
         # 释放相关资源
         return

      # 释放相关资源
      streamSource.contents.release(streamSource)


   # 软触发得到一张图并返回
   def do_grabOne(self):
      # 创建流对象
      # streamSourceInfo = GENICAM_StreamSourceInfo()
      # streamSourceInfo.channelId = 0
      # streamSourceInfo.pCamera = pointer(self.camera)
      #
      # streamSource = pointer(GENICAM_StreamSource())
      # nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))

      # 设置软触发
      nRet = setSoftTriggerConf(self.camera)
      if ( nRet != 0 ):
         print("set soft trigger fail")
         return None

      # 设置曝光时间
      exposure_time = self.settings.value('exposure_time')
      nRet = setExposureTime(self.camera, int(exposure_time))
      if ( nRet != 0 ):
         print("set exposure time fail")
         return None

      # 开始拉流
      nRet = self.streamSource.contents.startGrabbing(self.streamSource, c_ulonglong(0), \
                                                 c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
      if (nRet != 0):
         print("grabbing fail")
         return None

      # nRet = grabOne(self.camera, self.streamSource)
      # 执行软触发
      nRet = self.grabOne()
      if ( nRet != 0 ):
         print("grab one fail")
         return None

      # 主动取图
      frame = pointer(GENICAM_Frame())
      nRet = self.streamSource.contents.getFrame(self.streamSource, byref(frame), c_uint(1000))
      if (nRet != 0):
         print("get frame fail")
         return None
      else:
         print("SoftTrigger getFrame success BlockId = " + str(frame.contents.getBlockId(frame)))
         print("get frame time: " + str(datetime.datetime.now()))

      nRet = frame.contents.valid(frame)
      if (nRet != 0):
         frame.contents.release(frame)
         print("frame is not valid")
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

      # 停止拉流
      nRet = self.streamSource.contents.stopGrabbing(self.streamSource)
      if (nRet != 0):
         return None

      # # 释放相关资源
      # streamSource.contents.release(streamSource)

      # 格式转换
      if len(cvImage.shape) == 3:
         cvImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
      else:
         cvImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB)

      return cvImage


   # 模板感兴趣区域选取
   def do_selectROI(self, image):
      dsize = 0.25
      rImage = cv2.resize(image, dsize=None, fx=dsize, fy=dsize, interpolation=cv2.INTER_LINEAR)
      # selectROI和imshow的默认类型是BGR
      rImage = cv2.cvtColor(rImage, cv2.COLOR_RGB2BGR)
      # 画网格
      # drawgrid(rImage, 10)
      min_x, min_y, w, h = cv2.selectROI('select_roi', rImage)
      if len(rImage.shape) == 3:
         nImage = image[int(min_y/dsize):int((min_y+h)/dsize), int(min_x/dsize):int((min_x+w)/dsize), :]
      else:
         nImage = image[int(min_y/dsize):int((min_y+h)/dsize), int(min_x/dsize):int((min_x+w)/dsize)]
      cv2.destroyAllWindows()

      return nImage


   # 生成关键点和描述子
   def do_createDes(self, im1):
      # 缩放图像
      di = float(self.settings.value("resize_times"))
      img1 = cv2.resize(im1, dsize=None, fx=di, fy=di, interpolation=cv2.INTER_LINEAR)
      # 直方图归一化，应对白色的头盔
      # cv2.normalize(img1, img1, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
      if len(img1.shape) == 3:
         img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)

      # 限制对比度的自适应阈值均衡化
      clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
      img1 = clahe.apply(img1)

      # # 初始化SIFT特征检测器
      # sift = cv2.SIFT_create()
      # # 使用特征检测器找特征点和描述子
      # kp1, des1 = sift.detectAndCompute(img1, None)

      # 初始化SURF特征检测器
      surf = cv2.xfeatures2d.SURF_create()
      # 使用特征检测器找特征点和描述子
      kp1, des1 = surf.detectAndCompute(img1, None)

      return kp1, des1


   # 执行模板的数据库插入
   def do_sqlInsert(self, image, model, size, color, area):
      # 判断有无数据库，没有的话提示
      if not os.path.exists('./helmetDB.db3'):
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "没有数据库文件")
         messageBox.exec()
         return -1

      # 连接数据库
      conn = sqlite3.connect('helmetDB.db3')
      cursor = conn.cursor()

      # 执行插入
      sql = 'INSERT into helmet values (?,?,?,?,?,?,?,?,?)'
      exposure_time = int(self.settings.value('exposure_time'))
      x = [model, size, color, exposure_time, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), image.shape[1], image.shape[0], area,
           image.tobytes()]
      cursor.execute(sql, x)
      conn.commit()

      # 关闭数据库
      cursor.close()
      conn.close()

      return 0


   # 检测，通过回调函数
   def do_detect(self):
      # 注册拉流回调函数
      userInfo = b"jay"
      nRet = self.streamSource.contents.attachGrabbingEx(self.streamSource, self.GrabbingFrameCallbackFuncEx, userInfo)
      if (nRet != 0):
         print("attachGrabbingEx fail!")
         return -1

      # 设置外触发
      nRet = setLineTriggerConf(self.camera, int(self.settings.value("trigger_delay")))
      if (nRet != 0):
         print("set LineTriggerConf fail!")
         return -1
      else:
         print("set LineTriggerConf success!")

      # 设置曝光时间
      nRet = setExposureTime(self.camera, int(self.settings.value("exposure_time")))
      if (nRet != 0):
         print("set ExposureTime fail")
         return -1

      # 开始拉流
      nRet = self.streamSource.contents.startGrabbing(self.streamSource, c_ulonglong(0), \
                                                 c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
      if (nRet != 0):
         print("startGrabbing fail!")
         return -1


   # 停止检测
   def do_stopDetect(self):

      # 停止拉流
      nRet = self.streamSource.contents.stopGrabbing(self.streamSource)
      if (nRet != 0):
         print("stopGrabbing fail!")
         return -1

      # 反注册回调函数
      userInfo = b"jay"
      nRet = self.streamSource.contents.detachGrabbingEx(self.streamSource, self.UnGrabbingFrameCallbackFuncEx, userInfo)
      if (nRet != 0):
         print("detachGrabbingEx fail!")
         return -1


   # 返回生成的模板字典数组
   def do_selectTempArr(self):
      temp_arr = []

      # 模板字典
      for t in self.select_temp:
         temp = {}
         # 继电器端口数组
         if t["port"] == "":
            temp["port"] = []
         else:
            try:
               # 根据‘，’和‘,’分割成数组
               arr = t["port"].split(',')
               temp["port"] = []
               for a in arr:
                  temp["port"].extend(a.split("，"))
               # 转换为int类型
               for i in range(len(temp["port"])):
                  # print(temp["port"][i])
                  temp["port"][i] = int(temp["port"][i])
            except:
               return None
         # print(temp["port"])
         # 用于继电器端口循环输出的索引
         temp["port_index"] = 0
         temp["check"] = t["check"]
         temp["forward"] = t["forward"]
         temp["backward"] = t["backward"]
         temp["model"] = t["model"]
         temp["size"] = t["size"]
         temp["color"] = t["color"]
         temp["width"] = int(t["width"])
         temp["height"] = int(t["height"])
         temp["area"] = int(t["area"])
         image = numpy.frombuffer(t["image"], dtype=numpy.uint8)
         temp["image"] = numpy.reshape(image, (temp["height"], temp["width"], -1))
         kp, des = self.do_createDes(temp["image"])
         temp["kp"] = kp
         temp["des"] = des
         # temp["descriptor"] = numpy.reshape(numpy.frombuffer(t[des_index]), (-1, 128))
         temp_arr.append(temp)
      return temp_arr


   # def do_ignore_temp_arr(self):
   #    for t in self.temp_arr:
   #       if t["model"]+t["size"] in self.temp_arr_ignore:
   #          self.temp_arr_ignore[t["model"]+t["size"]] = list(set(self.temp_arr_ignore[t["model"]+t["size"]]) | set(t["port"]))
   #       else:
   #          self.temp_arr_ignore[t["model"]+t["size"]] = t["port"]
   #       self.temp_arr_ignore_index[t["model"]+t["size"]] = 0
   #    print(self.temp_arr_ignore)
   #    print(self.temp_arr_ignore_index)


   def do_TCPLink(self, a):
      label = self.ui.labTCP
      label.setStyleSheet('color: green')
      label.setText("连接成功")

      self.tcp_flag = True


   def do_testRelay_finish(self):
      self.ui.btnCloseRelay.setEnabled(True)
      self.ui.btnTestRelay.setEnabled(True)


   def do_interval_set_true(self):
      self.interval_flag = True
      # 设置一个定时器，单次触发
      self.timer = QTimer()
      self.timer.timeout.connect(self.do_interval_set_false)
      self.timer.setSingleShot(True)
      self.timer.start(int(self.settings.value('interval_time')) * 1000)


   def do_interval_set_false(self):
      self.interval_flag = False


##  ==============event处理函数==========================
   # 关闭事件
   def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
      ret = QMessageBox.warning(self, "提示", "确定退出吗？", QMessageBox.Yes | QMessageBox.No)
      # 是否关闭，是则停止检测关闭相机
      if ret == QMessageBox.Yes:
         if self.detect_flag:
            self.do_stopDetect()
            print("停止检测")
         if self.camera_flag:
            closeCamera(self.camera)
            print("关闭相机")
            # 释放相关资源
            self.streamSource.contents.release(self.streamSource)
         if self.relay_flag:
            close_relay(self.relay_dic)
         a0.accept()
      else:
         a0.ignore()


##  ==========由connectSlotsByName()自动连接的槽函数============
   # 检测相机
   @pyqtSlot()
   def on_btnDetectCamera_clicked(self):
      # image_arr = ["w-L-l.bmp", "w-L-r.bmp", "b-L-l.bmp", "b-L-r.bmp"]
      # image_arr = ["w-M-l.bmp", "w-M-r.bmp", "b-M-l.bmp", "b-M-r.bmp"]
      # image_arr = ["b-M-l-1.bmp", "b-M-r-1.bmp", "b-M-l.bmp", "b-M-r.bmp"]
      image_arr = ["w-M-l.bmp"]
      # image_arr = ["w-M-l-1.bmp", "w-M-r-1.bmp", "w-M-l.bmp", "w-M-r.bmp"]
      for image_name in image_arr:
         start = time.time()
         # cvImage = cv2.imread("./data_test/20220805/L/" + image_name)
         cvImage = cv2.imread("./data_test/20220805/M/" + image_name)
         # cvImage = cv2.imread("./data_test/20220805/S/" + image_name)
         # 格式转换
         if len(cvImage.shape) == 3:
            cvtImage = cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB)
         else:
            cvtImage = cv2.cvtColor(cvImage, cv2.COLOR_GRAY2RGB)

         # 显示输入
         try:
            qt_image = QtGui.QImage(cvtImage.data,
                                    cvtImage.shape[1],
                                    cvtImage.shape[0],
                                    cvtImage.shape[1] * 3,
                                    QtGui.QImage.Format.Format_RGB888)

            w = cvtImage.shape[1]  # 图像宽度
            h = cvtImage.shape[0]  # 图像高度
            W = self.ui.labInput.size().width()  # 显示框的宽度
            H = self.ui.labInput.size().height()  # 显示框的高度

            # 自适应图像宽高
            if float(H) / h > float(W) / w:
               self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
            else:
               self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
         except Exception as e:
            QMessageBox.warning(self, "警告", "图片输入出错")

         # 清空输入图像和输出图像
         self.ui.labOutput.clear()
         self.ui.label_2.clear()

         # # 检测
         # sift = SiftFlann(min_match_count=int(self.settings.value("min_match_count")),
         #                  resize_times=float(self.settings.value("resize_times")),
         #                  max_matches=int(self.settings.value("max_matches")),
         #                  trees=int(self.settings.value("trees")),
         #                  checks=int(self.settings.value("checks")),
         #                  k=int(self.settings.value("k")),
         #                  ratio=float(self.settings.value("ratio"))
         #                  )
         # # kp2, des2 = self.do_createDes(cvtImage)
         # # 返回结果，模板、方向、画出匹配框的图像
         # result, dir, imageDraw, angle, x, y = sift.match(self.temp_arr, cvtImage)

         # 检测
         surf = SurfBf(min_match_count=int(self.settings.value("min_match_count")),
                       resize_times=float(self.settings.value("resize_times")),
                       max_matches=int(self.settings.value("max_matches")),
                       trees=int(self.settings.value("trees")),
                       checks=int(self.settings.value("checks")),
                       k=int(self.settings.value("k")),
                       ratio=float(self.settings.value("ratio")),
                       hist2=float(self.settings.value("hist2")), area=float(self.settings.value("area"))
                       )
         # kp2, des2 = self.do_createDes(cvtImage)

         # # 直方图对比过滤模板
         # if len(cvImage.shape) == 3:
         #    resize_cvtImage = cv2.resize(cvtImage, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
         #    height = resize_cvtImage.shape[0]
         #    width = resize_cvtImage.shape[1]
         #    resize_cvtImage = resize_cvtImage[int(height*0.4):int(height*0.6),int(width*0.4):int(width*0.6),:]
         #    detect_temp_arr = []
         #    for detect_temp in self.temp_arr:
         #       resize_detect_temp = cv2.resize(detect_temp['image'], dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
         #       match = hist_compare(resize_cvtImage, resize_detect_temp)
         #       if match > float(self.settings.value('hist1')):
         #          detect_temp_arr.append(detect_temp)
         # else:
         #    detect_temp_arr = self.temp_arr
         #
         # # 返回结果，模板、方向、画出匹配框的图像
         # result, dir, imageDraw, angle, x, y = surf.match(detect_temp_arr, cvtImage)
         result, dir, imageDraw, angle, x, y, area2, area1 = surf.match(self.temp_arr, cvtImage, False)

         # # 左右反转再检测
         # if (angle > 0.2 and angle < numpy.pi / 2 - 0.2) or (angle > -numpy.pi + 0.2 and angle < -numpy.pi / 2 - 0.2):
         #    cvtImage_flip = cv2.flip(cvtImage, 1)
         #    result, dir_useless, imageDraw_useless, angle_useless, x_useless, y_useless = surf.match(self.temp_arr,
         #                                                                                             cvtImage_flip)

         # # if (angle > 0.2 and angle < numpy.pi / 2 - 0.2) or (angle > -numpy.pi + 0.2 and angle < -numpy.pi / 2 - 0.2):
         # if (angle > 0.2 and angle < numpy.pi - 0.2) or (angle > -numpy.pi + 0.2 and angle < - 0.2):
         #    rows, cols = cvtImage.shape[:2]
         #
         #    center = (cols / 2, rows / 2)
         #    angle_ = int(angle * 180 / numpy.pi)
         #    scale = 1
         #
         #    M = cv2.getRotationMatrix2D(center, angle_, scale)
         #    cvtImage_rotate = cv2.warpAffine(src=cvtImage, M=M, dsize=None, borderValue=(0, 0, 0))
         #    result, dir_useless, imageDraw, angle_useless, x_useless, y_useless = surf.match(self.temp_arr,
         #                                                                                     cvtImage_rotate, True)

         # 匹配结果不为空，则显示输入输出图像
         if not result is None:
            print("匹配结果:" + result["model"] + result["size"])
            print("\n")
            # 显示画出匹配框的图像
            try:
               qt_image = QtGui.QImage(imageDraw.data,
                                       imageDraw.shape[1],
                                       imageDraw.shape[0],
                                       imageDraw.shape[1] * 3,
                                       QtGui.QImage.Format.Format_RGB888)

               w = imageDraw.shape[1]
               h = imageDraw.shape[0]
               W = self.ui.labInput.size().width()
               H = self.ui.labInput.size().height()

               if float(H) / h > float(W) / w:
                  self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
               else:
                  self.ui.labInput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
            except Exception as e:
               QMessageBox.warning(self, "警告", "图片输入出错")
            # 显示输出图像
            image = result["image"]
            try:
               qt_image = QtGui.QImage(image.data,
                                       image.shape[1],
                                       image.shape[0],
                                       image.shape[1] * 3,
                                       QtGui.QImage.Format.Format_RGB888)

               w = image.shape[1]
               h = image.shape[0]
               W = self.ui.labOutput.size().width()
               H = self.ui.labOutput.size().height()

               if float(H) / h > float(W) / w:
                  self.ui.labOutput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
               else:
                  self.ui.labOutput.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
            except Exception as e:
               QMessageBox.warning(self, "警告", "图片输入出错")

            # 显示输出信息
            label = self.ui.label_2
            label.setStyleSheet('color: green')
            s = "前" if dir == 0 else "后"
            label.setText("型号：" + result["model"] + "；\t尺寸:" + result["size"] + "；\t方向：" + str(s)+"；\t颜色："+result["color"])
            # self.ui.label_2.setText("型号："+result["model"]+"；尺寸:"+result["size"]+"；方向："+angle)
            # 写入csv
            self.write_csv(result["model"], result["size"], result["color"], True, x, y, angle, imageDraw, area2, area1)
            # 传输数据
            if self.mythread:
               string = result["model"] + ";" + result["size"] + ";" + result["color"] + ";" + str(dir) + ";" + str(
                  x) + ";" + str(y) + ";" + str(angle)
               self.mythread.send(string)
            # 继电器输出
            if self.relay_flag:
               export_relay(self.relay_dic, result["port"])
         else:
            if dir == -1:
               self.ui.labInput.clear()
            else:
               label = self.ui.label_2
               label.setStyleSheet('color: red')
               self.ui.label_2.setText("无匹配结果")
               # 写入csv
               self.write_csv("", "", "", False, 0, 0, 0, cvtImage, 0, 0)
               # 传输数据
               if self.mythread:
                  string = ";" + ";" + ";" + str(-1) + ";" + str(0) + ";" + str(0) + ";" + str(0)
                  self.mythread.send(string)
               # 继电器输出
               if self.relay_flag:
                  export_relay(self.relay_dic, self.num)
            # print(time.time()-start)
      gc.collect()


   # 连接相机
   @pyqtSlot()
   def on_btnLinkCamera_clicked(self):
      # 打开相机
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

            lab = self.ui.labCloseCamera
            lab.setStyleSheet('color: black')
            lab.setText("无")

            # 按钮的使能和不使能
            self.ui.btnLinkCamera.setEnabled(False)
            # self.ui.btnDetectCamera.setEnabled(False)
            self.ui.btnTestCamera.setEnabled(True)
            self.ui.btnCloseCamera.setEnabled(True)
            self.ui.btnStartDetect.setEnabled(True)
            self.ui.btnMakeTemp.setEnabled(True)
            # 设置相机开关标志
            self.camera_flag = True


   # 测试相机
   @pyqtSlot()
   def on_btnTestCamera_clicked(self):
      # 按钮置为不使能
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnCloseCamera.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      # 测试相机
      self.do_testCamera()
      # 按钮使能
      self.ui.btnTestCamera.setEnabled(True)
      self.ui.btnCloseCamera.setEnabled(True)
      self.ui.btnStartDetect.setEnabled(True)
      self.ui.btnMakeTemp.setEnabled(True)


   # 关闭相机
   @pyqtSlot()
   def on_btnCloseCamera_clicked(self):
      # 如果在检测，则停止
      if self.detect_flag:
         self.do_stopDetect()
         self.detect_flag =False
      # 关闭相机
      nRet = closeCamera(self.camera)
      if (nRet != 0):
         print("closeCamera fail")
         # 释放相关资源
         self.streamSource.contents.release(self.streamSource)

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
      # 按钮
      self.ui.btnCloseCamera.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnLinkCamera.setEnabled(True)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnStopDetect.setEnabled(False)
      self.ui.btnSetParams.setEnabled(True)
      self.ui.btnSelectTemp.setEnabled(True)
      # 相机开关标志
      self.camera_flag = False


   # 开始检测
   @pyqtSlot()
   def on_btnStartDetect_clicked(self):
      # self.interval_thread = Interval_thread()
      # self.interval_thread.start()
      # self.interval_thread.signal_2.connect(self.do_interval_set_false)

      # 没有模板则提示
      if len(self.select_temp) == 0:
         QMessageBox.warning(self, "警告", "请选择模板")
         return
      # 按钮
      self.ui.btnStartDetect.setEnabled(False)
      self.ui.btnStopDetect.setEnabled(True)
      self.ui.btnSetParams.setEnabled(False)
      self.ui.btnSelectTemp.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnTestCamera.setEnabled(False)
      # 检测并设置标志
      if self.relay_flag:
         self.relay_export_thread = RelayExport_thread(self.relay_dic)
      self.do_detect()
      self.detect_flag = True


   # 停止检测
   @pyqtSlot()
   def on_btnStopDetect_clicked(self):
      # 停止检测并设置标志
      self.do_stopDetect()
      self.detect_flag = False
      # 关闭相机并释放资源
      nRet = closeCamera(self.camera)
      if (nRet != 0):
         print("closeCamera fail")
      self.streamSource.contents.release(self.streamSource)
      # 重新打开相机
      nRet = openCamera(self.camera)
      streamSourceInfo = GENICAM_StreamSourceInfo()
      streamSourceInfo.channelId = 0
      streamSourceInfo.pCamera = pointer(self.camera)
      self.streamSource = pointer(GENICAM_StreamSource())
      nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(self.streamSource))
      # 判断相机是否打开变换按钮
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
      # 跳出参数窗口
      dialogSetParams = QmyDialogSetParams()

      # 用于传输的默认参数
      self.default_params = {}
      for param_name in self.fixed_params:
         if param_name == 'resize_times' or param_name == 'ratio' or param_name == 'hist1' or param_name == 'hist2' or param_name == 'area' or param_name == 'delay_time':
            self.default_params[param_name] = float(self.default_settings.value(param_name))
         else:
            self.default_params[param_name] = int(self.default_settings.value(param_name))

      dialogSetParams.set_default_params(self.default_params)
      dialogSetParams.set_init_params()
      ret = dialogSetParams.exec()
      # 根据选择决定是否更改参数
      if ret:
         new_params = dialogSetParams.get_new_params()
         print(new_params)
         self.settings = QSettings("./config.ini", QSettings.IniFormat)
         old_resize = self.settings.value("resize_times")
         new_resize = new_params["resize_times"]
         for param_name in new_params:
            self.settings.setValue(param_name, new_params[param_name])
         # 判断resize_times是否改变确定是否更改关键点和描述子
         if round(float(old_resize), 1) != round(new_resize, 1) and len(self.temp_arr) != 0:
            print("重新生成描述子")
            for t in self.temp_arr:
               kp, des = self.do_createDes(t["image"])
               t["kp"] = kp
               t["des"] = des


   # 选择模板
   @pyqtSlot()
   def on_btnSelectTemp_clicked(self):
      # 跳出选择模板窗口
      select_flag = False
      while not select_flag:
         dialogSelectTemp = QmyDialogSelectTemp()

         dialogSelectTemp.set_temp(self.select_temp, self.num)
         dialogSelectTemp.set_ignore_flag(self.ignore_flag)
         dialogSelectTemp.do_showSelectTemp()
         ret = dialogSelectTemp.exec()
         # 根据选择的模板生成数组
         if ret:
            self.select_temp = dialogSelectTemp.get_temp()
            self.ignore_flag = dialogSelectTemp.get_ignore_flag()
            # print(len(self.select_temp))
            temp_arr = self.do_selectTempArr()
            # 判断端口参数设置是否出错，出错重新设置
            if not temp_arr is None:
               self.temp_arr = temp_arr
               # self.do_ignore_temp_arr()
               print("选择了"+str(len(self.temp_arr))+"模板")
               for t in self.select_temp:
                  print(t["model"]+"的输出端口号："+str(t["port"]))
               select_flag = True
            else:
               QMessageBox.warning(self, "提示", "请在输出端口按照 1,2,3 格式输入", QMessageBox.Yes)
         else:
            select_flag = True
      # print(len(self.temp_arr))
      # for i in self.temp_arr:
      #    print(i["des"])


   # 拍摄模板
   @pyqtSlot()
   def on_btnMakeTemp_clicked(self):
      # 按钮
      self.ui.btnTestCamera.setEnabled(False)
      self.ui.btnMakeTemp.setEnabled(False)
      self.ui.btnStartDetect.setEnabled(False)
      # 获得一张图
      image = self.do_grabOne()
      if image is None:
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "请关闭相机后连接相机并重试")
         messageBox.exec()
         if self.camera_flag:
            self.ui.btnTestCamera.setEnabled(True)
            self.ui.btnMakeTemp.setEnabled(True)
            self.ui.btnStartDetect.setEnabled(True)
         return
      # 计算面积
      R = self.settings.value("R")
      G = self.settings.value("G")
      B = self.settings.value("B")
      bg_thresh = int(self.settings.value("bg_thresh"))
      bg_color = [int(R), int(G), int(B)]

      image_resize = cv2.resize(image, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
      area, binary_ = remove_bg(bg_color, bg_thresh, image_resize)

      # 选择感兴趣区域
      nImage = self.do_selectROI(image)
      if len(nImage) != 0:
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
            # if len(image.shape) == 3:
            #    nImage = cv2.cvtColor(nImage, cv2.COLOR_BGR2RGB)
            # else:
            #    nImage = cv2.cvtColor(nImage, cv2.COLOR_GRAY2RGB)
            ret = self.do_sqlInsert(nImage, model, size, color, area)

            if ret == 0:
               # messageBox = QMessageBox(QMessageBox.about, "ok", "数据库插入成功")
               QMessageBox.about(self, 'about', '数据库插入成功')
               # messageBox.exec()


      if self.camera_flag:
         self.ui.btnTestCamera.setEnabled(True)
         self.ui.btnMakeTemp.setEnabled(True)
         self.ui.btnStartDetect.setEnabled(True)


   # 开启主机
   @pyqtSlot()
   def on_btnTCPOpen_clicked(self):
      ip = self.ui.lineEditAdr.text()
      port = int(self.ui.lineEditPort.text())
      address = (ip, port)

      self.tcp_server_socket = socket(AF_INET, SOCK_STREAM)
      self.tcp_server_socket.bind(address)
      self.tcp_server_socket.listen(128)

      label = self.ui.labTCP
      label.setStyleSheet('color: green')
      label.setText("等待连接")

      # client_socket, ip_port = self.tcp_server_socket.accept()
      self.mythread = Runthread(self.tcp_server_socket)
      self.mythread.start()

      self.mythread.signal.connect(self.do_TCPLink)

      self.ui.btnTCPClose.setEnabled(True)
      self.ui.btnTCPOpen.setEnabled(False)


   # 关闭主机
   @pyqtSlot()
   def on_btnTCPClose_clicked(self):
      # self.tcp_server_socket.close()
      self.mythread.pause()

      label = self.ui.labTCP
      label.setStyleSheet('color: black')
      label.setText("未开启")

      self.tcp_flag = False
      self.ui.btnTCPClose.setEnabled(False)
      self.ui.btnTCPOpen.setEnabled(True)

      self.mythread = None


   # 打开继电器
   @pyqtSlot()
   def on_btnOpenRelay_clicked(self):
      # 继电器初始化，拿到继电器字典
      self.relay_dic = init_relay()
      print(self.relay_dic)
      if len(self.relay_dic) != 0:
         # 计算端口数
         num = 0
         for key, value in self.relay_dic.items():
            num += value-1
         self.num = num

         label = self.ui.labRelay
         label.setStyleSheet('color: green')
         label.setText(str(len(self.relay_dic))+"个继电器,"+str(num)+"个端口")

         self.ui.btnOpenRelay.setEnabled(False)
         self.ui.btnCloseRelay.setEnabled(True)
         self.ui.btnTestRelay.setEnabled(True)

         self.relay_flag = True  # 继电器开关标志
      else:
         label = self.ui.labRelay
         label.setStyleSheet('color: red')
         label.setText("未检测到继电器")


   # 关闭继电器
   @pyqtSlot()
   def on_btnCloseRelay_clicked(self):
      close_relay(self.relay_dic)

      label = self.ui.labRelay
      label.setStyleSheet('color: black')
      label.setText("未开启")

      self.ui.btnOpenRelay.setEnabled(True)
      self.ui.btnCloseRelay.setEnabled(False)
      self.ui.btnTestRelay.setEnabled(False)

      self.relay_flag = False


   # 测试继电器
   @pyqtSlot()
   def on_btnTestRelay_clicked(self):
      # 在检测中则不能测试继电器
      if self.detect_flag:
         return
      self.ui.btnCloseRelay.setEnabled(False)
      self.ui.btnTestRelay.setEnabled(False)
      self.relay_thread = Relaythread(self.relay_dic)
      self.relay_thread.signal_1.connect(self.do_testRelay_finish)
      self.relay_thread.start()


##  =============自定义槽函数===============================


##  ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序

   form = QmyWidget()  # 创建窗体
   form.show()

   sys.exit(app.exec_())
   os._exit(0)