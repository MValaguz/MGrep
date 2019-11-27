# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 25/08/2019
 Descrizione...: Programma per visualizzare le info di MGrep
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file program_info_ui.py è ricavato partendo da program_info_ui.ui 
"""

#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from program_info_ui import Ui_Program_info
       
class program_info_class(QtWidgets.QDialog):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self, p_mdi_area):
        super(program_info_class, self).__init__()
        self.ui = Ui_Program_info()
        self.ui.setupUi(self)
        self.mdi_area = p_mdi_area
            
    def slot_Program_info_close(self):
        """
            Chiude la window (attenzione! durante l'inizializzazione viene passato il riferimento al widget mdi)
        """
        self.mdi_area.closeActiveSubWindow()
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = program_info_class(None)
    application.show()
    sys.exit(app.exec())        