from functools import wraps
from typing import Iterable, Union, Callable

from qtpy.QtCore import QSize, QMargins, QObject
from qtpy.QtWidgets import QWidget

from QSugar.type.reference import Ref
from QSugar.util import ReflectUtil


def Batch(func):
    def wrapper(*args):
        for arg in args:
            func(arg)

    return wrapper


class BaseClazzProxy:
    INIT_PROXY_CLASS_SET = set()
    """
    This set is used to ensure that the __init__ method of each class is not repeated
    """

    @staticmethod
    def prop_size_handler(item: QWidget, size: Union[tuple, QSize]) -> None:
        """
        Body of the method that handles the `size` property
        :param item: QWidget object
        :param size: the size of widget, in the form of `QSize(600,800)` or `(600,800)`
        """
        if isinstance(size, tuple):
            item.setFixedSize(QSize(*size))
        else:
            item.setFixedSize(size)

    @staticmethod
    def prop_margins_handler(item: QWidget, margins: Union[tuple, QMargins]) -> None:
        """
        Body of the method that handles the `margins` property
        :param item: QWidget object
        :param margins: the margins of widget, in the form of `QMargins(16,8,8,16)` or `(16,8,8,1+)`
        """
        if isinstance(margins, tuple):
            item.setContentsMargins(QMargins(*margins))
        else:
            item.setContentsMargins(margins)

    @staticmethod
    def prop_self_handler(item: QObject, self: Ref):
        """
        Body of the method that handles the `self` property
        :param item: QObject object
        :param self: reference object
        """
        self.value = item

    prop_handlers = {
        'size': prop_size_handler,
        'margins': prop_margins_handler,
        'self': prop_self_handler,
    }

    prop_mappers = {
        'width': 'fixedWidth',
        'height': 'fixedHeight',
        'max_size': 'maximumSize',
        'max_width': 'maximumWidth',
        'max_height': 'maximumHeight',
        'min_size': 'minimumSize',
        'min_width': 'minimumWidth',
        'min_height': 'minimumHeight',
        'title': 'windowTitle'
    }

    @classmethod
    def def_prop_handler(cls, prop: str, handler: Callable):
        """
        Define property names that need to be handled additionally.
        """
        cls.prop_handlers[prop] = handler

    @classmethod
    def def_prop_mapper(cls, prop: str, mapper: str):
        """
        Define the property names that need to be mapped.
        """
        cls.prop_mappers[prop] = mapper

    @classmethod
    def kwargs_intercept(cls, target: dict, sep: Iterable, repl: Iterable) -> tuple[dict, dict]:
        """
        Intercept key valueRef pairs of the `target`.
        If the key is in `sep`, it will be separated;
        and if the key is in `repl`, replace it directly.
        """

        sep_kwargs = dict()

        for key in target.copy():
            if key in sep:
                sep_kwargs[key] = target[key]
                target.pop(key)
            if key in repl:
                repl_kw = cls.prop_mappers[key]
                target[repl_kw] = target[key]
                del target[key]

        return sep_kwargs, target

    @classmethod
    def proxy_clazz_init_method(cls, init_method):
        """
        Decorator of modified class.
        In order to proxy `__init__` method of modified class.
        """

        @wraps(init_method)
        def init_proxy(*args, **kwargs):
            seq_keywords = cls.prop_handlers.keys()
            repl_keywords = cls.prop_mappers.keys()

            sep_kwargs, kwargs = cls.kwargs_intercept(
                kwargs, seq_keywords, repl_keywords
            )
            init_method(*args, **kwargs)
            self = args[0]
            for key, value in sep_kwargs.items():
                handler = cls.prop_handlers[key]
                handler(self, value)

        return init_proxy

    @classmethod
    def base_proxy_clazz_setter(cls, setter: Callable):
        """
        Setter method proxy, which implements the Fluent API.
        """

        @wraps(setter)
        def setter_proxy(*args, **kwargs):
            self = args[0]
            setter(*args, **kwargs)
            return self

        return setter_proxy

    def __call__(self, clazz):
        mro_clazz_list = self.__class__.mro()
        mro_clazz_list.append(clazz)

        if clazz not in self.INIT_PROXY_CLASS_SET:
            clazz.__init__ = self.proxy_clazz_init_method(clazz.__init__)
            self.INIT_PROXY_CLASS_SET.add(clazz)

        for mro_clazz in mro_clazz_list:
            if mro_clazz == object:
                continue
            for setter_name in ReflectUtil.scanFluentProps(mro_clazz):
                clazz_setter = getattr(mro_clazz, setter_name)
                setattr(mro_clazz, setter_name, self.base_proxy_clazz_setter(clazz_setter))
        return clazz


Def = BaseClazzProxy()
