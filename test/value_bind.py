import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import *

from QSugar.component import RowCol
from QSugar.proxy import Batch, Bind
from QSugar.type import Ref

import logging

logging.basicConfig(level=logging.INFO)

Batch(Bind)(
    QScrollBar,
    QSpinBox,
    QDoubleSpinBox,
    QProgressBar,
    QSlider
)

uniValueProp = Ref(0)


def resetUniValueProp():
    uniValueProp << 0


app = QApplication(sys.argv)

bar = Ref(None)

widget = QWidget(
    child=RowCol(
        alignment=Qt.AlignmentFlag.AlignCenter,
        children=[
            QScrollBar(Qt.Horizontal,value=uniValueProp),
            QSpinBox(value=uniValueProp),
            QDoubleSpinBox(value=uniValueProp),
            QProgressBar(value=uniValueProp),
            QSlider(Qt.Horizontal, value=uniValueProp),
            QPushButton(
                text='Reset',
                clicked=resetUniValueProp
            ),
        ]
    )
)

widget.show()

app.exec()
