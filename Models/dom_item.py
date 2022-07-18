from PyQt5.QtXml import QDomNode


class DomItem:
    def __init__(self, node: QDomNode, row: int, parent=None):
        # private
        self.__dom_node: QDomNode = node
        self.__child_items: dict[int, DomItem] = {}
        self.__parent_item: DomItem = parent
        self.__row_number: int = row

    @property
    def node(self):
        return self.__dom_node

    @property
    def parent(self):
        return self.__parent_item

    @property
    def row(self) -> int:
        return self.__row_number

    def child(self, i: int):
        child_item: DomItem = self.__child_items.get(i)

        if child_item:
            return child_item

        # if child does not yet exist, create it
        if 0 <= i < self.__dom_node.childNodes().count():
            child_node: QDomNode = self.__dom_node.childNodes().item(i)
            child_item = DomItem(child_node, i, self)
            self.__child_items[i] = child_item

        return child_item
