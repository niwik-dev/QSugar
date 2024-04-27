from qtpy.QtCore import QObject

from QSugar.proxy.base import BaseClazzProxy
from QSugar.util.reflect import ReflectUtil


class DSLClazzProxy(BaseClazzProxy):
    @staticmethod
    def prop_children_handler(item: QObject, children: list[QObject]) -> None:
        """
        Body of the method that handles the `size` property
        :param item: QObject object
        :param children: children of the widget/layout
        """
        for child in children:
            ReflectUtil.contain(item, child)

    @staticmethod
    def prop_child_handler(item: QObject, child: QObject):
        """
        Body of the method that handles the `size` property
        :param item: QObject object
        :param child: child of the widget/layout
        """
        ReflectUtil.contain(item, child)

    BaseClazzProxy.prop_handlers.update({
        'children': prop_children_handler,
        'child': prop_child_handler
    })

    def __call__(self, clazz):
        return super().__call__(clazz)


DSL = DSLClazzProxy()
