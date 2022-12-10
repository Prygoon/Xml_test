from PyQt5.QtCore import pyqtSlot, QFile, QIODevice
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QWidget, QMenu, QTreeView, QMainWindow, QFileDialog, QAction, QHeaderView
from PyQt5.QtXml import QDomDocument

from Models.dom_model import DomModel


class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.__model = DomModel(QDomDocument(), self)
        self.__file_menu = QMenu()
        self.__xml_path = ''
        self.__view = QTreeView(self)

        open_action: QAction = QAction('&Open...', self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self.open_file)

        exit_action: QAction = QAction('&Exit', self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)

        self.__file_menu = self.menuBar().addMenu('File')
        self.__file_menu.addAction(open_action)
        self.__file_menu.addAction(exit_action)

        self.__view.setModel(self.__model)

        self.__view.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.setCentralWidget(self.__view)
        self.setWindowTitle('Simple DOM Model')

    @pyqtSlot()
    def open_file(self):
        file_path: str = QFileDialog.getOpenFileName(self, 'Open File',
                                                     self.__xml_path, 'XML files (*.xml);;HTML files (*.html);;'
                                                                      'SVG files (*.svg);;User Interface files (*.ui)')

        if file_path != '':
            xml_file: QFile = QFile(file_path[0])
            if xml_file.open(QIODevice.ReadOnly):
                document: QDomDocument = QDomDocument()
                if document.setContent(xml_file):
                    new_model: DomModel = DomModel(document, self)
                    self.__view.setModel(new_model)
                    del self.__model
                    self.__xml_path = file_path[0]

            xml_file.close()
