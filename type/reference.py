from qtpy.QtCore import QObject, Signal, Property


class Ref(QObject):

    def __init__(self, value: object):
        super().__init__()
        self.__value = value
        self.__packed__ = False

    def getValue(self) -> object:
        return self.__value

    def setValue(self, value: object):
        if value != self.__value:
            self.__value = value
            self.valueChanged.emit(value)

    valueChanged = Signal(object)
    value = Property(object, fget=getValue, fset=setValue, notify=valueChanged)

    def __iter__(self):
        return self

    def __next__(self):
        if not self.__packed__:
            self.__packed__ = True
            return self.value
        else:
            self.__packed__ = False
            raise StopIteration

    def __getattr__(self, item):
        return getattr(self.value, item)

    def __setattr__(self, key, value):
        if key == 'value':
            self.setValue(value)
        else:
            super().__setattr__(key, value)

    def __lshift__(self, value: object):
        self.setValue(value)
        return self

    def __getitem__(self, item):
        return self.value.__getitem__(item)


class DeepRef(Ref):
    def __init__(self, value: object):
        super().__init__(value)
        self.walk(value)

    def init(self) -> object:
        return self

    @classmethod
    def isPrivate(cls, name: str):
        if name.startswith('__') or name.startswith('_'):
            return True
        else:
            return False

    def walk(self, obj: object):
        if not hasattr(obj, '__dict__'):
            return

        attrs = vars(obj)
        for name, attr in attrs.items():
            if not self.isPrivate(name):
                setattr(self, name, DeepRef(attr))
