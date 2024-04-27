import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout

from QSugar import Batch, DSL, Ref, Computed, Bind

Batch(DSL)(
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton
)

Batch(Bind)(
    QLabel
)

base, rate = Ref(1), Ref(1)
tip = Computed(globals())


@tip.get
def getTip():
    return f'The number is {base.value * rate.value}.'


def increase():
    base << base.value + 1


def decrease():
    base << base.value - 1


def double():
    rate << rate.value * 2


def half():
    rate << rate.value / 2


app = QApplication(sys.argv)

widget = QWidget(
    child=QVBoxLayout(
        children=[
            QLabel(
                alignment=Qt.AlignCenter,
                text=tip
            ),
            QHBoxLayout(
                children=[
                    QPushButton(
                        text='count +1',
                        clicked=increase
                    ),
                    QPushButton(
                        text='count -1',
                        clicked=decrease
                    )
                ]
            ),
            QHBoxLayout(
                children=[
                    QPushButton(
                        text='rate *2',
                        clicked=double
                    ),
                    QPushButton(
                        text='rate /2',
                        clicked=half
                    )
                ]
            )
        ]
    )
)
widget.show()

app.exec()
