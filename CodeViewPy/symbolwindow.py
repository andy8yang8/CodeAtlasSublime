# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore,uic
import sys

qtCreatorFile = './ui/Symbol.ui' # Enter file here.

Ui_SymbolWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ForbiddenItem(QtGui.QListWidgetItem):
	def __init__(self, uname, name, parent = None):
		super(ForbiddenItem, self).__init__(name, parent)
		self.uniqueName = uname

	def getUniqueName(self):
		return self.uniqueName

class SymbolWindow(QtGui.QScrollArea, Ui_SymbolWindow):
	def __init__(self, parent = None):
		QtGui.QScrollArea.__init__(self)
		Ui_SymbolWindow.__init__(self)
		self.setupUi(self)
		self.addForbidden.clicked.connect(self.onAddForbidden)
		self.deleteForbidden.clicked.connect(self.onDeleteForbidden)

	def onAddForbidden(self):
		from UIManager import UIManager
		scene = UIManager.instance().getScene()
		scene.addForbiddenSymbol()
		self.updateForbiddenSymbol()

	def updateForbiddenSymbol(self):
		from UIManager import UIManager
		scene = UIManager.instance().getScene()
		forbidden = scene.getForbiddenSymbol()

		self.forbiddenList.clear()
		#print('update forbidden', forbidden)
		for uname, name in forbidden.items():
			self.forbiddenList.addItem(ForbiddenItem(uname, name))


	def onDeleteForbidden(self):
		print('delete forbidden')
		item = self.forbiddenList.currentItem()

		from UIManager import UIManager
		scene = UIManager.instance().getScene()
		print('item', item)
		if not item or not scene:
			return

		scene.acquireLock()
		scene.deleteForbiddenSymbol(item.getUniqueName())
		self.updateForbiddenSymbol()

		item = self.forbiddenList.item(0)
		if item:
			self.forbiddenList.setCurrentItem(item)

		scene.releaseLock()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	window = SymbolWindow()
	window.show()
	sys.exit(app.exec_())