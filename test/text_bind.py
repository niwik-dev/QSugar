import sys

from qtpy.QtGui import Qt
from qtpy.QtWidgets import *

from QSugar import *

import logging

logging.basicConfig(level=logging.INFO)

Batch(Bind)(
    QPushButton,
    QLineEdit,
    QTextEdit,
    QPlainTextEdit,
    QLabel,
    QTextBrowser
)

uniTextProp = Ref('Lorem Ipsum')


def resetUniTextProp():
    uniTextProp << 'Lorem Ipsum'


app = QApplication(sys.argv)

widget = QWidget(
    child=RowCol(
        alignment=Qt.AlignmentFlag.AlignCenter,
        children=[
            QPushButton(text=uniTextProp),
            QLabel(text=uniTextProp),
            QTextEdit(text=uniTextProp),
            QPlainTextEdit(text=uniTextProp),
            QPushButton(
                text='Reset',
                clicked=resetUniTextProp
            ),
        ]
    )
)

widget.show()

app.exec()
