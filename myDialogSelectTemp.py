# -*- coding: utf-8 -*-
import os
import sys

import cv2
import numpy as np
from PyQt5 import QtGui
import copy

from PyQt5.QtCore import Qt, QItemSelectionModel, QModelIndex
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem

from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

##from PyQt5.QtWidgets import

##from PyQt5.QtGui import

from PyQt5.QtSql import QSqlDatabase, QSqlTableModel

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import


from ui_DialogSelectTemp import Ui_Dialog


class QmyDialogSelectTemp(QDialog):
   def __init__(self, parent=None):
      super().__init__(parent)  # 调用父类构造函数，创建窗体
      self.ui = Ui_Dialog()  # 创建UI对象
      self.ui.setupUi(self)  # 构造UI界面

      self.ui.lineEditSearch.setPlaceholderText("输入型号后点击过滤")
      self.ui.btnSave.setEnabled(False)
      self.ui.btnRevert.setEnabled(False)

      self.selectedTemp = []  # 选择的模板数组

      self.do_showAllTemp()   # 展示所有模板
      self.do_showSelectTemp()   # 展示选择的模板


##  ============自定义功能函数========================
   # 已选择的模板
   def set_temp(self, select_temp):
      self.selectedTemp = copy.deepcopy(select_temp)
      # print(len(self.selectedTemp[0]))


   # 返回选择的模板
   def get_temp(self):
      return copy.deepcopy(self.selectedTemp)


   # 获得列名称
   def __getFieldNames(self):
      emptyRec = self.tableModel.record()     #获取空记录，只有字段名
      self.fldNum={}   #字段名与序号的字典
      for i in range(emptyRec.count()):
         fieldName=emptyRec.fieldName(i)
         self.fldNum.setdefault(fieldName)
         self.fldNum[fieldName]=i
      # print (self.fldNum)


   # 打开表格
   def __openTable(self):
      self.tableModel = QSqlTableModel(self, self.db)
      self.tableModel.setTable("helmet")
      self.tableModel.setSort(self.tableModel.fieldIndex("rowid"), Qt.AscendingOrder)
      self.tableModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
      if self.tableModel.select() == False:
         QMessageBox.critical(self, "出错信息", "打开数据表错误，错误信息\n" + self.tableModel.lastError().text())
         return
      # 获得字段
      self.__getFieldNames()
      # 设置列名
      self.tableModel.setHeaderData(self.fldNum["model"], Qt.Horizontal, "型号")
      self.tableModel.setHeaderData(self.fldNum["size"], Qt.Horizontal, "尺寸")
      self.tableModel.setHeaderData(self.fldNum["color"], Qt.Horizontal, "颜色")
      self.tableModel.setHeaderData(self.fldNum["date"], Qt.Horizontal, "日期")
      self.tableModel.setHeaderData(self.fldNum["width"], Qt.Horizontal, "图片宽")
      self.tableModel.setHeaderData(self.fldNum["height"], Qt.Horizontal, "图片高")
      self.tableModel.setHeaderData(self.fldNum["image"], Qt.Horizontal, "图片")

      # for i in range(1, 11):
      #    self.tableModel.setHeaderData(self.fldNum["descriptor_{}".format(i)], Qt.Horizontal, "0.{}倍描述子".format(i))  # 这两个字段不在tableView中显示
      # self.tableModel.setHeaderData(self.fldNum["descriptor_2"], Qt.Horizontal, "0.2倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_3"], Qt.Horizontal, "0.3倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_4"], Qt.Horizontal, "0.4倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_5"], Qt.Horizontal, "0.5倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_6"], Qt.Horizontal, "0.6倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_7"], Qt.Horizontal, "0.7倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_8"], Qt.Horizontal, "0.8倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_9"], Qt.Horizontal, "0.9倍描述子")
      # self.tableModel.setHeaderData(self.fldNum["descriptor_10"], Qt.Horizontal, "0.10倍描述子")

      self.selModel = QItemSelectionModel(self.tableModel)  # 选择模型
      self.selModel.currentChanged.connect(self.do_currentChanged)  # 当前项变化时触发
      self.selModel.currentRowChanged.connect(self.do_currentRowChanged)  # 选择行变化时

      self.ui.tableViewAllTemp.setModel(self.tableModel)  # 设置数据模型
      self.ui.tableViewAllTemp.setSelectionModel(self.selModel)  # 设置选择模型

      self.ui.tableViewAllTemp.setColumnHidden(self.fldNum["image"], True)  # 隐藏列
      # for i in range(1, 11):
      #    self.ui.tableViewAllTemp.setColumnHidden(self.fldNum["descriptor_{}".format(i)], True)  # 隐藏列


   # 刷新表格(已选模板)
   def __freshTable(self):
      self.ui.tableWidgetSelectTemp.setRowCount(0)
      self.ui.tableWidgetSelectTemp.clearContents()
      # 展示已选模板
      for t in self.selectedTemp:
         column = 0
         row = self.ui.tableWidgetSelectTemp.rowCount()
         self.ui.tableWidgetSelectTemp.insertRow(row)
         for index in t:
            if column == 6:
               break
            item = QTableWidgetItem(str(t[index]))
            self.ui.tableWidgetSelectTemp.setItem(row, column, item)
            column += 1

      # print(self.ui.tableWidgetSelectTemp.rowCount())
      if self.ui.tableWidgetSelectTemp.rowCount() > 0:
         self.ui.btnRemove.setEnabled(True)
         self.ui.btnClear.setEnabled(True)
      else:
         self.ui.btnRemove.setEnabled(False)
         self.ui.btnClear.setEnabled(False)


   # 展示所有模板
   def do_showAllTemp(self):
      # 判断数据库是否存在
      if not os.path.exists('./helmetDB.db3'):
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "没有数据库文件")
         messageBox.exec()
         return -1
      # 打开数据库并展示
      self.db = QSqlDatabase.addDatabase("QSQLITE")
      self.db.setDatabaseName('./helmetDB.db3')
      if self.db.open():
         self.__openTable()
      else:
         QMessageBox.warning(self, "错误", "打开数据库失败")


   # 展示选择的模板
   def do_showSelectTemp(self):
      # 设置表格列名
      self.ui.tableWidgetSelectTemp.setColumnCount(6)
      headerText = ["型号", "尺寸", "颜色", "日期", "图片宽", "图片高"]
      for i in range(len(headerText)):
         headerItem = QTableWidgetItem(headerText[i])
         self.ui.tableWidgetSelectTemp.setHorizontalHeaderItem(i, headerItem)
      # 刷新表格
      self.__freshTable()

      self.ui.tableWidgetSelectTemp.currentItemChanged.connect(self.do_currentRowChanged_2)


##  ===========event处理函数==========================


##  ========由connectSlotsByName()自动连接的槽函数=========
   # 保存更改
   @pyqtSlot()
   def on_btnSave_clicked(self):
      res = self.tableModel.submitAll()
      if res == False:
         QMessageBox.information(self, "消息", "数据保存错误，出错信息\n"+self.tableModel.lastError().text())
      else:
         self.ui.btnSave.setEnabled(False)
         self.ui.btnRevert.setEnabled(False)


   # 撤销更改
   @pyqtSlot()
   def on_btnRevert_clicked(self):
      self.tableModel.revertAll()
      self.ui.btnSave.setEnabled(False)
      self.ui.btnRevert.setEnabled(False)


   # 删除模板
   @pyqtSlot()
   def on_btnDelete_clicked(self):
      if self.tableModel.isDirty():
         QMessageBox.information(self, "消息", "请保存或取消之前的修改之后再进行删除")
      else:
         curIndex = self.selModel.currentIndex()
         ret = QMessageBox.warning(self, "警告", "确定删除该条数据吗", QMessageBox.Ok | QMessageBox.No, QMessageBox.No)
         if ret == QMessageBox.Ok:
            self.tableModel.removeRow(curIndex.row())
            self.tableModel.submitAll()
         else:
            return


   # 过滤模板
   @pyqtSlot()
   def on_btnSearch_clicked(self):
      self.tableModel.setFilter("model like '%{}%'".format(self.ui.lineEditSearch.text()))


   # 选择模板
   @pyqtSlot()
   def on_btnSelect_clicked(self):
      temp = {}
      for i in self.fldNum:
         temp[i] = self.curRec.value(i)
      self.selectedTemp.append(temp)
      # 刷新表格
      self.__freshTable()


   # 移除已选模板
   @pyqtSlot()
   def on_btnRemove_clicked(self):
      curRow = self.ui.tableWidgetSelectTemp.currentRow()
      # if curRow == -1:
      #    return
      # for i in range(len(self.selectedTemp)):
      #    flag = True
      #    itemModel = self.ui.tableWidgetSelectTemp.item(curRow, 0).text()
      #    itemSize = self.ui.tableWidgetSelectTemp.item(curRow, 1).text()
      #    itemColor = self.ui.tableWidgetSelectTemp.item(curRow, 2).text()
      #    itemDate = self.ui.tableWidgetSelectTemp.item(curRow, 3).text()
      #    itemWidth = int(self.ui.tableWidgetSelectTemp.item(curRow, 4).text())
      #    itemHeight = int(self.ui.tableWidgetSelectTemp.item(curRow, 5).text())
      #
      #    if ((itemModel != self.selectedTemp[i]["model"]) | (itemSize != self.selectedTemp[i]["size"]) |
      #       (itemColor != self.selectedTemp[i]["color"]) | (itemDate != self.selectedTemp[i]["date"]) |
      #       (itemWidth != self.selectedTemp[i]["width"]) | (itemHeight != self.selectedTemp[i]["height"])):
      #       flag = False
      #
      #    if flag == True:
      #       self.selectedTemp.pop(i)
      #       break
      self.selectedTemp.pop(curRow)
      # 刷新
      self.__freshTable()


   # 清空选择
   @pyqtSlot()
   def on_btnClear_clicked(self):
      self.ui.tableWidgetSelectTemp.setRowCount(0)
      self.ui.tableWidgetSelectTemp.clearContents()
      self.selectedTemp.clear()


##  ==========自定义槽函数===============================
   # item更改时触发
   def do_currentChanged(self):
      self.ui.btnSave.setEnabled(self.tableModel.isDirty())
      self.ui.btnRevert.setEnabled(self.tableModel.isDirty())


   # 行更改时触发(所有模板)
   def do_currentRowChanged(self, current, previous):
      curRec = self.tableModel.record(current.row())
      self.curRec = curRec
      if curRec.isNull("image"):
         self.ui.labAllTemp.clear()
      else:
         # 展示所在行模板图片
         image_data = curRec.value("image")
         width = curRec.value("width")
         height = curRec.value("height")
         image = np.frombuffer(image_data, dtype=np.uint8)
         # if int(width)*int(height) == len(image):
         #    image = np.reshape(image, (int(height), int(width)))
         #    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
         # elif int(width)*int(height)*3 == len(image):
         #    image = np.reshape(image, (int(height), int(width), 3))
         try:
            image = np.reshape(image, (int(height), int(width), 3))
            qt_image = QtGui.QImage(image.data,
                                    image.shape[1],
                                    image.shape[0],
                                    image.shape[1] * 3,
                                    QtGui.QImage.Format.Format_RGB888)

            w = image.shape[1]
            h = image.shape[0]
            W = self.ui.labAllTemp.size().width()
            H = self.ui.labAllTemp.size().height()

            if float(H) / h > float(W) / w:
               self.ui.labAllTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
            else:
               self.ui.labAllTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
         except Exception as e:
            QMessageBox.warning(self, "警告", "图片数据出错")


   # 行更改时触发(选择的模板)
   def do_currentRowChanged_2(self, current, previous):
      if current is None:
         return
      row = current.row()
      # 展示图片
      image_data = self.selectedTemp[row]["image"]
      width = self.selectedTemp[row]["width"]
      height = self.selectedTemp[row]["height"]
      image = np.frombuffer(image_data, dtype=np.uint8)
      image = np.reshape(image, (int(height), int(width), 3))
      try:
         qt_image = QtGui.QImage(image.data,
                                 image.shape[1],
                                 image.shape[0],
                                 image.shape[1] * 3,
                                 QtGui.QImage.Format.Format_RGB888)

         w = image.shape[1]
         h = image.shape[0]
         W = self.ui.labSelectTemp.size().width()
         H = self.ui.labSelectTemp.size().height()

         if float(H) / h > float(W) / w:
            self.ui.labSelectTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToWidth(W))
         else:
            self.ui.labSelectTemp.setPixmap(QtGui.QPixmap.fromImage(qt_image).scaledToHeight(H))
      except Exception as e:
         QMessageBox.warning(self, "警告", "图片数据出错")


##  ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序
   form = QmyDialogSelectTemp()  # 创建窗体
   form.show()
   sys.exit(app.exec_())
