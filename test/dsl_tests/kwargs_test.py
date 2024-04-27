import sys

from qtpy.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout

from QSugar.proxy import Batch, DSL, Bind
from QSugar.type import Ref, DeepRef

Batch(Bind)(
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)

Batch(DSL)(
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)

app = QApplication(sys.argv)

textProp = Ref('Text')

btn = DeepRef(None)

widget = QWidget(
    title='Prop DSL Test',
    size=(300, 300),
    child=QHBoxLayout(
        children=[
            QPushButton(
                text=textProp
            ),
            QVBoxLayout(
                children=[
                    QPushButton(
                        text=textProp
                    ),
                    QPushButton(
                        text=textProp
                    )
                ]
            ),
            QPushButton(
                text='Button A',
                clicked=lambda : textProp << ''
            ),
            QPushButton(
                text='Button B',
                clicked=lambda: textProp << 'Text'
            )
        ]
    )
)

widget.show()
app.exec()
