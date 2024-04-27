import sys

from qtpy.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout

from QSugar.proxy import Batch, DSL
from QSugar.type import DeepRef

Batch(DSL)(
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)


class Model:
    def __init__(self):
        self.text = 'Click Me'
        self.styleSheet = 'color:red'


model = DeepRef(Model())

app = QApplication(sys.argv)

widget = QWidget(
    title='Prop DSL Test',
    size=(300, 300),
    child=QHBoxLayout(
        children=[
            QPushButton(
                text='Hello,World',
                styleSheet=model.styleSheet,
                clicked=lambda: model.text << 'Hi,World'
            ),
            QPushButton(
                text=model.text,
                clicked=lambda: model.styleSheet << 'color:blue'
            )
        ]
    )
)

widget.show()
app.exec()
