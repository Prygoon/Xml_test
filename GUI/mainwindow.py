from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QMenu, QTreeView, QMainWindow
from PyQt5.QtXml import QDomDocument


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.model = DomModel(QDomDocument(), self)
        self.file_menu = QMenu()
        self.xml_path = ''
        self.view = QTreeView(self)

        file_menu = menuBar.addMenu()

    @pyqtSlot()
    def open_file(self):
        pass
