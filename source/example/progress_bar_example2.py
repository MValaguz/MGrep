# -*- coding: utf-8 -*-
import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtWidgets

class wait_thread(QThread):
    """
       Questa classe serve per creare un thread separato che si metta in ascolto di eventuali messaggi
       al parametro p_tool_chat dovrà essere passata la classe tools_chat (di fatto l'oggetto principale di questo programma
    """
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)        
        MainWindow = QtWidgets.QWidget()
        MainWindow .setWindowTitle('Progress Bar')
        self.progress = QtWidgets.QProgressDialog("Please Wait!", "Cancel", 0, 0, MainWindow) 
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(0)
        self.button = QtWidgets.QPushButton('Start')
        self.button.move(0, 30)
        MainWindow.show()

        self.button.clicked.connect(self.onButtonClick)        

    def run(self):
        # ciclo di scambio messaggi fino a quando con si chiude la connessione
        errore = False
        while not errore:
           pass    
        self.signal.emit(message)
        
    def onButtonClick(self):
        print('click')
        


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = wait_thread()
    sys.exit(app.exec_())