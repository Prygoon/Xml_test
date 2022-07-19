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
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_item: DomItem = self.__root_item
        else:
            parent_item: DomItem = parent.internalPointer()

        child_item: DomItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)

        return QModelIndex()

    def parent(self, child: QModelIndex) -> QModelIndex:
        if not child.isValid():
            return QModelIndex()

        child_item: DomItem = child.internalPointer()
        parent_item: DomItem = child_item.parent

        if not parent_item or parent_item == self.__root_item:
            return QModelIndex()

        return self.createIndex(parent_item.row, 0, parent_item)

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item: DomItem = self.__root_item
        else:
            parent_item: DomItem = parent.internalPointer()

        return parent_item.node.childNodes().count()

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 3
