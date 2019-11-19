# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 18/11/2019
 Descrizione...: Main del programma MGrep
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file MGrep_ui.py è ricavato partendo da MGrep_ui.ui 
"""

#Librerie sistema
import os
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from MGrep_ui import Ui_MainWindow
#Librerie interne SmiGrep
from preferenze import preferenze
from utilita import message_error, message_info
       
class MGrep_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self):
        super(MGrep_class, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
            
    def slot_actionSearch_string(self):
        """
          Richiamo form di ricerca stringa
        """        
        from ricerca_stringhe import ricerca_stringhe_class
        app1 = ricerca_stringhe_class()        
        app1.show()
                    
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = MGrep_class()
    application.show()
    sys.exit(app.exec())        