# -*- coding: utf-8 -*-
import os
import sys

from PyQt5.QtCore import Qt, QItemSelectionModel, QModelIndex
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

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

      self.do_showAllTemp()


##  ============自定义功能函数========================
   def __getFieldNames(self):
      emptyRec = self.tableModel.record()     #获取空记录，只有字段名
      self.fldNum={}   #字段名与序号的字典
      for i in range(emptyRec.count()):
         fieldName=emptyRec.fieldName(i)
         self.fldNum.setdefault(fieldName)
         self.fldNum[fieldName]=i
      print (self.fldNum)


   def __openTable(self):
      self.tableModel = QSqlTableModel(self, self.db)
      self.tableModel.setTable("helmet")
      self.tableModel.setSort(self.tableModel.fieldIndex("rowid"), Qt.AscendingOrder)
      self.tableModel.setEditStrategy(QSqlTableModel.OnManualSubmit)
      if self.tableModel.select() == False:
         QMessageBox.critical(self, "出错信息", "打开数据表错误，错误信息\n" + self.tableModel.lastError().text())
         return
      self.__getFieldNames()

      self.tableModel.setHeaderData(self.fldNum["model"], Qt.Horizontal, "型号")
      self.tableModel.setHeaderData(self.fldNum["size"], Qt.Horizontal, "尺寸")
      self.tableModel.setHeaderData(self.fldNum["color"], Qt.Horizontal, "颜色")
      self.tableModel.setHeaderData(self.fldNum["date"], Qt.Horizontal, "日期")
      self.tableModel.setHeaderData(self.fldNum["width"], Qt.Horizontal, "图片宽")
      self.tableModel.setHeaderData(self.fldNum["height"], Qt.Horizontal, "图片高")
      self.tableModel.setHeaderData(self.fldNum["image"], Qt.Horizontal, "图片")

      self.tableModel.setHeaderData(self.fldNum["descriptor_1"], Qt.Horizontal, "0.1倍描述子")  # 这两个字段不在tableView中显示
      self.tableModel.setHeaderData(self.fldNum["descriptor_2"], Qt.Horizontal, "0.2倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_3"], Qt.Horizontal, "0.3倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_4"], Qt.Horizontal, "0.4倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_5"], Qt.Horizontal, "0.5倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_6"], Qt.Horizontal, "0.6倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_7"], Qt.Horizontal, "0.7倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_8"], Qt.Horizontal, "0.8倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_9"], Qt.Horizontal, "0.9倍描述子")
      self.tableModel.setHeaderData(self.fldNum["descriptor_10"], Qt.Horizontal, "0.10倍描述子")

      self.selModel = QItemSelectionModel(self.tableModel)  # 选择模型
      self.selModel.currentChanged.connect(self.do_currentChanged)  # 当前项变化时触发
      self.selModel.currentRowChanged.connect(self.do_currentRowChanged)  # 选择行变化时

      self.ui.tableViewAllTemp.setModel(self.tableModel)  # 设置数据模型
      self.ui.tableViewAllTemp.setSelectionModel(self.selModel)  # 设置选择模型

      self.ui.tableViewAllTemp.setColumnHidden(self.fldNum["image"], True)  # 隐藏列
      for i in range(1, 11):
         self.ui.tableViewAllTemp.setColumnHidden(self.fldNum["descriptor_{}".format(i)], True)  # 隐藏列



   def do_showAllTemp(self):
      if not os.path.exists('./helmetDB.db3'):
         messageBox = QMessageBox(QMessageBox.Warning, "warning", "没有数据库文件")
         messageBox.exec()
         return -1
      self.db = QSqlDatabase.addDatabase("QSQLITE")
      self.db.setDatabaseName('./helmetDB.db3')
      if self.db.open():
         self.__openTable()
      else:
         QMessageBox.warning(self, "错误", "打开数据库失败")

##  ===========event处理函数==========================


##  ========由connectSlotsByName()自动连接的槽函数=========
   @pyqtSlot()
   def on_btnSave_clicked(self):
      res = self.tableModel.submitAll()
      if res == False:
         QMessageBox.information(self, "消息", "数据保存错误，出错信息\n"+self.tableModel.lastError().text())
      else:

         self.ui.btnSave.setEnabled(False)
         self.ui.btnRevert.setEnabled(False)

   @pyqtSlot()
   def on_btnRevert_clicked(self):
      self.tableModel.revertAll()
      self.ui.btnSave.setEnabled(False)
      self.ui.btnRevert.setEnabled(False)

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

##  ==========自定义槽函数===============================
   def do_currentChanged(self):
      self.ui.btnSave.setEnabled(self.tableModel.isDirty())
      self.ui.btnRevert.setEnabled(self.tableModel.isDirty())

   def do_currentRowChanged(self):
      print("行变化")

##  ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序
   form = QmyDialogSelectTemp()  # 创建窗体
   form.show()
   sys.exit(app.exec_())
