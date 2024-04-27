"""
Attention! It is not currently recommended for use and the scheme may require major changes.
"""

import logging
from qtpy.QtCore import *
from qtpy.QtWidgets import *
from lxml import etree
from lxml.etree import Element
from QSugar.util.reflect import ReflectUtil

KeepAlive = []
"""
I have to admit that the `KeepAlive` variable is a pretty lame design,
Cause putting objects in a global singleton pool to protect objects from being released prematurely is really insecure and weird.
What if you have a better idea? Please contact me!
"""


class QTMLLoader(object):
    def __init__(self):
        self._content: bytes = b''

    def parse_head(self, head: Element):
        """Parse the contents of the head tag"""
        # TODO
        pass

    def parse_qml(self, view: Element, parent: QObject):
        """Parse and embed QML components """
        # TODO
        pass

    def parse_widget(self, view: Element, parent: QObject) -> tuple[QObject, QObject]:
        """
        Parse the QtWidgets component
        """
        clazz_str = view.tag

        item = ReflectUtil.instance(clazz_str)
        KeepAlive.append(item)

        for nodeProp in view.items():
            propKey, propValue = nodeProp
            if propKey.endswith('ed'):
                ReflectUtil.connect(item, propKey, propValue)
                continue
            ReflectUtil.setRealProp(item, propKey, propValue)

        if not parent:
            item.show()
        else:
            parent, item = ReflectUtil.contain(parent, item)

        return item, parent

    def parse_prop(self, view: Element, parent: QObject):
        """
        Parse the properties of the widgets
        """
        content = view.text
        if content:
            content = content.strip()
        nodeTag = view.tag

        if parent is None:
            return
        if content:
            ReflectUtil.setProp(parent, nodeTag, content)
        resValue = self.parse_body(view, parent)
        if len(resValue) > 1:
            logging.warning(f'Notice!There are {len(resValue)} properties set on `{nodeTag}`.')

        if resValue:
            ReflectUtil.setRealProp(parent, nodeTag, resValue[-1])

    def parse_body(self, view: Element, parent: QObject = None) -> list[QWidget]:
        """
        Parse the contents of the body tag
        """
        result = []
        for node in view:
            nodeTag = node.tag
            if not isinstance(nodeTag, str):
                continue

            if nodeTag[0].isupper():
                if nodeTag == 'QML':
                    self.parse_qml(node, parent)
                else:
                    item, parent = self.parse_widget(node, parent)
                    self.parse_body(node, item)

            if nodeTag[0].islower():
                self.parse_prop(node, parent)

        return result

    def parse(self):
        """
        Parse the contents of the QTML file
        :return:The list of parsed Qt widgets
        """
        root = etree.fromstring(self._content)

        for block in root:
            if block.tag == 'head':
                self.parse_head(block)
            if block.tag == 'body':
                body = self.parse_body(block)

        return body

    def load(self, filepath: str):
        """
        Load the QTML file from path
        :param filepath: local filepath, which can be the Qt resource file path
        """
        file = QFile(filepath)
        if not file.exists():
            raise FileNotFoundError(f'File {filepath} not found')

        okay = file.open(QFile.ReadOnly)
        if not okay or not file.isReadable():
            raise IOError(f'Cannot read file {filepath}')
        stream = file.readAll()
        file.close()

        try:
            self._content = stream.data()
        except UnicodeEncodeError:
            raise UnicodeEncodeError(f'Cannot decode file {filepath} as UTF-8')
