import sys
from PyQt5.QtWidgets import (QApplication, QProgressDialog)
from PyQt5.QtCore import Qt
import time
 
 
def show_progress(max=100):
    progress = QProgressDialog("Doing stuff...[0/0]", "Abort", 0, max, None)
    progress.setWindowModality(Qt.WindowModal)
    progress.setModal(True)
    progress.show()
    for i in range(max + 1):
        progress.setValue(i)
        progress.setLabelText("Doing stuff...[{}/{}]".format(
            i, progress.maximum()))
        if progress.wasCanceled():
            break
        time.sleep(0.05)
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    show_progress(max=210)