from typing import Any

from PyQt5.QtCore import QAbstractItemModel, QObject, QModelIndex, Qt, QVariant
from PyQt5.QtXml import QDomDocument, QDomNode, QDomNamedNodeMap

from Models.dom_item import DomItem


class DomModel(QAbstractItemModel):

    def __init__(self, document: QDomDocument, parent: QObject = None):
        super().__init__(parent)

        self.__dom_document: QDomDocument = document
        self.__root_item: DomItem = DomItem(self.__dom_document, 0)

    def data(self, index: QModelIndex, role: int = ...) -> Any:
        if not index.isValid():
            return QVariant()

        if role != Qt.DisplayRole:
            return QVariant()

        item: DomItem = index.internalPointer()

        node: QDomNode = item.node

        if index.column() == 0:
            return node.nodeName()
        elif index.column() == 1:
            attribute_map: QDomNamedNodeMap = node.attributes()
            attributes: list[str] = []
            for i in range(attribute_map.count()):
                attribute: QDomNode = attribute_map.item(i)
                attributes.append(f'{attribute.nodeName()}=\"{attribute.nodeValue()}\"')

            return ' '.join(attributes)
        elif index.column() == 2:
            return ' '.join(node.nodeValue().split('\n'))
        else:
            return QVariant()

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        return super().flags(index)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...) -> Any:
        header_data = {0: 'Name', 1: 'Attributes', 2: 'Value'}

        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return header_data[section]

        return QVariant()

    def index(self, row: int, column: int, parent: QModelIndex = ...) -> QModelIndex:
        return super().index(row, column, parent)

    def parent(self, child: QModelIndex) -> QModelIndex:
        return super().parent(child)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return super().rowCount(parent)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return super().columnCount(parent)
