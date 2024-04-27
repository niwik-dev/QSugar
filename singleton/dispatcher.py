from typing import Union

from qtpy.QtCore import QObject, Signal

from QSugar.type.computed import Computed
from QSugar.type.reference import Ref
from QSugar.util.decorator import singleton

import logging


@singleton
class NotifySignalDispatcher(QObject):
    """
    Notify signals from the widget will be dispatched by this class.
    And the request format is class object, property name, new property value.
    """
    requestReceived = Signal(QObject, str, object)

    def __init__(self):
        super().__init__(parent=None)
        self.dispatchRule = dict()
        self.requestReceived.connect(self.handle_request)

    def handle_request(self, sender: QObject, prop_name: str, value: object) -> None:
        logging.info(f'Route:{sender.__class__.__name__}/{prop_name} Body:{value}')
        if (sender, prop_name) in self.dispatchRule:
            valueRef = self.dispatchRule[(sender, prop_name)]
            valueRef.setValue(value)

    def describe(self, sender: QObject, prop_name: str, valueRef: Union[Ref,Computed]) -> None:
        self.dispatchRule[(sender, prop_name)] = valueRef

        setter_name = 'set' + prop_name[0].upper() + prop_name[1:]
        setter = getattr(sender, setter_name)

        valueRef.valueChanged.connect(setter)
        valueRef.valueChanged.emit(valueRef.getValue())
