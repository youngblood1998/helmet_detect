from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox

from PyQt5.QtCore import Qt


## ==============基于QComboBox的代理组件====================
class QmyComboBoxDelegate(QStyledItemDelegate):
   def __init__(self, parent=None):
      super().__init__(parent)
      self.__itemList = []
      self.__isEditable = False

   def setItems(self, itemList, isEditable=False):
      self.__itemList = itemList
      self.__isEditable = isEditable

   ## 自定义代理组件必须继承以下4个函数
   def createEditor(self, parent, option, index):
      editor = QComboBox(parent)
      editor.setFrame(False)
      editor.setEditable(self.__isEditable)
      editor.addItems(self.__itemList)
      return editor

   def setEditorData(self, editor, index):
      model = index.model()
      text = model.data(index, Qt.EditRole)
      ##      text = str(index.model().data(index, Qt.EditRole))
      editor.setCurrentText(text)

   def setModelData(self, editor, model, index):
      text = editor.currentText()
      model.setData(index, text, Qt.EditRole)

   def updateEditorGeometry(self, editor, option, index):
      editor.setGeometry(option.rect)