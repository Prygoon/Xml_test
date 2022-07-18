from PyQt5.QtCore import pyqtSlot, QFile, QIODevice
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QMenu, QTreeView, QMainWindow, QFileDialog
from PyQt5.QtXml import QDomDocument

from Models.dom_model import DomModel


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.model = DomModel(QDomDocument(), self)
        self.file_menu = QMenu()
        self.xml_path = ''
        self.view = QTreeView(self)

        file_menu = self.menuBar().addMenu('File')
        file_menu.addAction('&Open...', MainWindow.open_file, QKeySequence.Open)
        file_menu.addAction('E&xit', QWidget.close, QKeySequence.Quit)

        self.view.setModel(self.model)

    @pyqtSlot()
    def open_file(self):
        file_path: str = QFileDialog.getOpenFileName(self, 'Open File',
                                                     self.xml_path, 'XML files (*.xml);;HTML files (*.html);;'
                                                                    'SVG files (*.svg);;User Interface files (*.ui)')

        if file_path != '':
            file: QFile = QFile(file_path)
            if file.open(QIODevice.ReadOnly):
                document: QDomDocument = QDomDocument()
                if document.setContent(file):
                    new_model: DomModel = DomModel(document, self)
                    self.view.setModel(new_model)
                    del self.model
                    self.xml_path = file_path

            file.close()
