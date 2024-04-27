from qtpy.QtCore import *
from qtpy.QtWidgets import *


class ReflectUtil:
    @classmethod
    def contain(cls, parent: object, child: object):
        if isinstance(parent, QLayout):
            if isinstance(child, QLayout):
                parent.addLayout(child)
            elif isinstance(child, QWidget):
                parent.addWidget(child)
        elif isinstance(parent, QWidget):
            if isinstance(child, QLayout):
                parent.setLayout(child)
            elif isinstance(child, QWidget):
                layout = QHBoxLayout()
                parent.setLayout(layout)
                layout.addWidget(child)
                parent = layout
        return parent, child

    @classmethod
    def connect(cls, item: QWidget, signal: str, slot: str):
        signal = getattr(item, signal)
        slot = eval(f'lambda: {slot}')
        signal.connect(slot)

    @classmethod
    def setProp(cls, item: QObject, prop: str, value: str):
        clazz = item.__class__
        prop = prop[0].upper() + prop[1:]
        clazz_prop_setter = getattr(clazz, f'set{prop}')
        evalValue = eval(value)
        if isinstance(evalValue, tuple):
            clazz_prop_setter(item, *evalValue)
        else:
            clazz_prop_setter(item, evalValue)

    @classmethod
    def setRealProp(cls, item: QObject, prop: str, value: object):
        clazz = item.__class__
        prop = prop[0].upper() + prop[1:]
        clazz_prop_setter = getattr(clazz, f'set{prop}')
        clazz_prop_setter(item, value)

    @classmethod
    def scanFluentProps(cls, clazzOrObj: object):
        attrs = dir(clazzOrObj)
        for attr in attrs:
            if attr.startswith('_') or attr.startswith('__'):
                continue
            if attr.endswith('_') or attr.endswith('__'):
                continue
            if attr.startswith('set') or attr.startswith('add'):
                fluent_method_name = attr
                yield fluent_method_name

    @classmethod
    def scanSymmetricProps(cls, clazzOrObj: object):
        attrs = dir(clazzOrObj)
        for attr in attrs:
            result = []
            if attr.startswith('_') or attr.startswith('__'):
                continue
            if attr.endswith('_') or attr.endswith('__'):
                continue
            if attr.startswith('set'):
                setter_name = attr
                prop_name = attr.removeprefix('set')
                bool_getter_name = f'is{prop_name}'
                getter_name = prop_name[0].lower() + prop_name[1:]
                notify_signal_name = f'{prop_name}Changed'

                if setter_name in attrs or notify_signal_name in attrs:
                    result.append(setter_name)

                if getter_name in attrs:
                    result.append(getter_name)
                elif bool_getter_name in attrs:
                    result.append(bool_getter_name)
                else:
                    result.append(None)

                yield result

    @classmethod
    def instance(cls, clazz: str):
        return eval(clazz)()


if __name__ == '__main__':
    print(ReflectUtil.scanSymmetricProps(QWidget))
