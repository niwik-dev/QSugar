import sys

from qtpy.QtWidgets import QWidget, QApplication, QHBoxLayout, QPushButton, QVBoxLayout

from QSugar.proxy import Batch, Bind
from QSugar.type import Ref

Batch(Bind)(
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
)

textProp = Ref('Text')

app = QApplication(sys.argv)

widget = \
    (
        QWidget()
        .setWindowTitle('Fluent DSL Test')
        .setFixedSize(300, 300)
        .setLayout(
            QHBoxLayout()
            .addWidget(
                btn := QPushButton()
                .setText(textProp)
            )
            .addLayout(
                QVBoxLayout()
                .addWidget(
                    QPushButton()
                    .setText(textProp)
                )
                .addWidget(
                    QPushButton()
                    .setText(textProp)
                )
            )
            .addWidget(
                btnA := QPushButton()
                .setText('Button A')
            )
            .addWidget(
                btnB := QPushButton()
                .setText('Button B')
            )
        )
    )

btnA.clicked.connect(
    lambda: textProp << ''
)

btnB.clicked.connect(
    lambda: textProp << 'Text'
)

widget.show()
app.exec()
