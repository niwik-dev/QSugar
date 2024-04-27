import ast
import inspect
from functools import wraps
from typing import Callable

from qtpy.QtCore import QObject, Signal

from QSugar.type import Ref


class RefVisitor(ast.NodeVisitor):
    def __init__(self, _globals):
        self.globals = _globals
        self.locals = set()
        self.refValues = list()

    def walk(self, node):
        if isinstance(node, ast.Tuple):
            for each in node.dims:
                self.walk(each)
        else:
            self.locals.add(node.id)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Tuple):
                self.walk(target)

    def visit_Name(self, node):
        if node.id in self.locals:
            return
        if self.globals:
            var = self.globals[node.id]
            if isinstance(var, Ref):
                self.refValues.append(var)


class Computed(QObject):
    valueChanged = Signal(object)
    value: object

    BindComputedProperty = '__bind_computed_property__'

    def watch(self, func: Callable):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            src = inspect.getsource(func)
            tree = ast.parse(src)
            visitor = RefVisitor(self._globals)
            visitor.visit(tree)

            for refValue in visitor.refValues:
                if hasattr(refValue, self.BindComputedProperty):
                    if getattr(refValue, self.BindComputedProperty) == self:
                        continue
                refValue.valueChanged.connect(
                    lambda: self.valueChanged.emit(self.value)
                )
                setattr(refValue, self.BindComputedProperty, self)
            ret = func(*args, **kwargs)
            return ret

        return func_wrapper

    def __init__(self, _globals=None):
        super().__init__()
        self._globals = _globals
        self._getter: Callable = None
        self._setter: Callable = None

    def __call__(self, func: Callable):
        self._getter = self.watch(func)
        self._getter()
        return self._getter

    def get(self, func: Callable):
        self._getter = self.watch(func)
        self._getter()
        return self._getter

    def callGet(self):
        return self._getter()

    def set(self, func: Callable):
        self._setter = func
        return self._setter

    def callSet(self, *args, **kwargs):
        return self._setter(*args, **kwargs)

    def __getattr__(self, item):
        if item == 'value':
            return self.callGet()
        else:
            return super().__getattr__(item)

    def __setattr__(self, key, value):
        if key == 'value':
            self.callSet(value)
        else:
            super().__setattr__(key, value)

    def getValue(self):
        return self.value

    def setValue(self, value):
        if value != self.value:
            self.value = value
