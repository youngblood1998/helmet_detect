# -*- coding: utf-8 -*-

import sys

from PyQt5.QtWidgets import QApplication, QDialog

from PyQt5.QtCore import  pyqtSlot,QSettings

##from PyQt5.QtWidgets import

##from PyQt5.QtGui import

##from PyQt5.QtSql import

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import


from ui_DialogSetParams import Ui_Dialog


class QmyDialogSetParams(QDialog):
   def __init__(self, parent=None):
      super().__init__(parent)  # 调用父类构造函数，创建窗体
      self.ui = Ui_Dialog()  # 创建UI对象
      self.ui.setupUi(self)  # 构造UI界面


##  ============自定义功能函数========================
   def set_default_params(self, default_params):
      # 默认参数获得
      self.default_params = default_params


   def set_init_params(self):
      # 根据配置文件设置初始参数
      setting = QSettings('./config.ini', QSettings.IniFormat)
      self.ui.spinBoxExposureTime.setValue(int(setting.value('exposure_time')))
      self.ui.spinBoxTriggerDelay.setValue(int(setting.value('trigger_delay')))
      self.ui.spinBoxIntervalTime.setValue(int(setting.value('interval_time')))
      self.ui.doubleSpinBoxDelay.setValue(float(setting.value('delay_time')))
      self.ui.spinBoxMinMatchCount.setValue(int(setting.value('min_match_count')))
      self.ui.doubleSpinBoxResizeTimes.setValue(float(setting.value('resize_times')))
      self.ui.spinBoxMaxMatches.setValue(int(setting.value('max_matches')))
      self.ui.doubleSpinBoxHist1.setValue(float(setting.value('hist1')))
      self.ui.doubleSpinBoxHist2.setValue(float(setting.value('hist2')))
      self.ui.doubleSpinBoxArea.setValue(float(setting.value('area')))
      self.ui.spinBoxR.setValue(int(setting.value('R')))
      self.ui.spinBoxG.setValue(int(setting.value('G')))
      self.ui.spinBoxB.setValue(int(setting.value('B')))
      self.ui.spinBoxBgThresh.setValue(int(setting.value('bg_thresh')))
      self.ui.spinBoxTree.setValue(int(setting.value('trees')))
      self.ui.spinBoxChecks.setValue(int(setting.value('checks')))
      self.ui.spinBoxK.setValue(int(setting.value('k')))
      self.ui.doubleSpinBoxRatio.setValue(float(setting.value('ratio')))


   def get_new_params(self):
      # 新的参数返回
      new_params = {
         'exposure_time': self.ui.spinBoxExposureTime.value(),
         'trigger_delay': self.ui.spinBoxTriggerDelay.value(),
         'interval_time': self.ui.spinBoxIntervalTime.value(),
         'delay_time': self.ui.doubleSpinBoxDelay.value(),
         'min_match_count': self.ui.spinBoxMinMatchCount.value(),
         'resize_times': self.ui.doubleSpinBoxResizeTimes.value(),
         'max_matches': self.ui.spinBoxMaxMatches.value(),
         'hist1': self.ui.doubleSpinBoxHist1.value(),
         'hist2': self.ui.doubleSpinBoxHist2.value(),
         'area': self.ui.doubleSpinBoxArea.value(),
         'R': self.ui.spinBoxR.value(),
         'G': self.ui.spinBoxG.value(),
         'B': self.ui.spinBoxB.value(),
         'bg_thresh': self.ui.spinBoxBgThresh.value(),
         'trees': self.ui.spinBoxTree.value(),
         'checks': self.ui.spinBoxChecks.value(),
         'k': self.ui.spinBoxK.value(),
         'ratio': self.ui.doubleSpinBoxRatio.value()
      }
      return new_params


##  ===========event处理函数==========================


##  ========由connectSlotsByName()自动连接的槽函数=========
   @pyqtSlot()
   def on_btnDefault_clicked(self):
      # 恢复默认参数
      self.ui.spinBoxExposureTime.setValue(self.default_params['exposure_time'])
      self.ui.spinBoxTriggerDelay.setValue(self.default_params['trigger_delay'])
      self.ui.spinBoxIntervalTime.setValue(self.default_params['interval_time'])
      self.ui.doubleSpinBoxDelay.setValue(self.default_params['delay_time'])
      self.ui.spinBoxMinMatchCount.setValue(self.default_params['min_match_count'])
      self.ui.doubleSpinBoxResizeTimes.setValue(self.default_params['resize_times'])
      self.ui.spinBoxMaxMatches.setValue(self.default_params['max_matches'])
      self.ui.doubleSpinBoxHist1.setValue(self.default_params['hist1'])
      self.ui.doubleSpinBoxHist2.setValue(self.default_params['hist2'])
      self.ui.doubleSpinBoxArea.setValue(self.default_params['area'])
      self.ui.spinBoxR.setValue(self.default_params['R'])
      self.ui.spinBoxG.setValue(self.default_params['G'])
      self.ui.spinBoxB.setValue(self.default_params['B'])
      self.ui.spinBoxBgThresh.setValue(self.default_params['bg_thresh'])
      self.ui.spinBoxTree.setValue(self.default_params['trees'])
      self.ui.spinBoxChecks.setValue(self.default_params['checks'])
      self.ui.spinBoxK.setValue(self.default_params['k'])
      self.ui.doubleSpinBoxRatio.setValue(self.default_params['ratio'])


   @pyqtSlot()
   def on_btnSetDefault_clicked(self):
      self.default_settings = QSettings("./defaultConfig.ini", QSettings.IniFormat)
      new_default_params = {
         'exposure_time': self.ui.spinBoxExposureTime.value(),
         'trigger_delay': self.ui.spinBoxTriggerDelay.value(),
         'interval_time': self.ui.spinBoxIntervalTime.value(),
         'delay_time': self.ui.doubleSpinBoxDelay.value(),
         'min_match_count': self.ui.spinBoxMinMatchCount.value(),
         'resize_times': self.ui.doubleSpinBoxResizeTimes.value(),
         'max_matches': self.ui.spinBoxMaxMatches.value(),
         'hist1': self.ui.doubleSpinBoxHist1.value(),
         'hist2': self.ui.doubleSpinBoxHist2.value(),
         'area': self.ui.doubleSpinBoxArea.value(),
         'R': self.ui.spinBoxR.value(),
         'G': self.ui.spinBoxG.value(),
         'B': self.ui.spinBoxB.value(),
         'bg_thresh': self.ui.spinBoxBgThresh.value(),
         'trees': self.ui.spinBoxTree.value(),
         'checks': self.ui.spinBoxChecks.value(),
         'k': self.ui.spinBoxK.value(),
         'ratio': self.ui.doubleSpinBoxRatio.value()
      }
      for param_name in new_default_params:
         self.default_settings.setValue(param_name, new_default_params[param_name])
      self.default_params = new_default_params

##  ==========自定义槽函数===============================


##  ============窗体测试程序 ============================
if __name__ == "__main__":  # 用于当前窗体测试
   app = QApplication(sys.argv)  # 创建GUI应用程序
   form = QmyDialogSetParams()  # 创建窗体
   form.show()
   sys.exit(app.exec_())
