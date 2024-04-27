import sys

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QPushButton, QTextEdit, QLabel, QApplication, QWidget

from QSugar.component import RowCol
from QSugar.proxy import Batch, DSL
from QSugar.type import Ref

Batch(DSL)(
    QWidget,
    QPushButton,
    QTextEdit,
    QLabel
)

isVisible = Ref(True)

app = QApplication(sys.argv)

widget = QWidget(
    child=RowCol(
        alignment=Qt.AlignmentFlag.AlignCenter,
        children=
        [
            QLabel(
                visible=isVisible,
                text=f'<{tag}>{index + 1}. {name}</{tag}>'
            )
            for index, (name, tag) in enumerate(
            [
                ('John', 'h1'), ('Tom', 'h2'), ('Alice', 'h3')
            ]
        )
        ]
        +
        [
            QPushButton(
                text='Click Me',
                clicked=lambda: isVisible << (not isVisible.value)
            )
        ]
        +
        [
            [
                QPushButton(text=str(row * 3 + col + 1))
                for col in range(3)
            ]
            for row in range(3)
        ]
    )
)

widget.show()

app.exec()
