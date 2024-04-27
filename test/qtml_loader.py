import sys

from qtpy.QtWidgets import QApplication

from QSugar import QTMLLoader

app = QApplication(sys.argv)

loader = QTMLLoader()
loader.load('./index.qtml')
loader.parse()

app.exec()