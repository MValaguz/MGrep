from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import (QWidget, QApplication, QBoxLayout, QPushButton,
                             QProgressBar)
from PyQt5.QtCore import Qt
import sys
import time


class CustomProgressBar(QProgressBar):
    def __init__(self, minimum, maximum):
        super(CustomProgressBar, self).__init__()
        self.setRange(minimum, maximum)
        self.setAlignment(Qt.AlignCenter)
        self._text = "0/0 (0%) Click start..."
        self.setFormat("%v/%m (%p%)")

    def set_text(self, text):
        self._text = text

    def text(self):
        return self._text

    def update(self, step):
        maximum = self.maximum()
        rate = step * 100 / maximum
        string = "{}/{} ({}%)".format(step, maximum, rate)
        time.sleep(1)
        self.set_text(string)
        self.setValue(step)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("QProgressBar Example")
        self.central_widget = FormWidget(self) 
        self.setCentralWidget(self.central_widget)
        self.resize(250, 100)


class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(layout)
        self.progressbar = CustomProgressBar(0, 3)
        btn_start = QPushButton("START")
        layout.addWidget(self.progressbar, 0)
        layout.addWidget(btn_start, 0)
        btn_start.clicked.connect(self.on_start)

    def on_start(self):
        max = self.progressbar.maximum()        
        for n in range(max + 1):
            self.progressbar.update(n)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())