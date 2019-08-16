# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria qt5
 Data..........: 05/07/2017
 Descrizione...: Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms ecc.
 
 Note..........: Per far funzionare la ricerca di Apex è necessario che sotto Oracle sia installata la funzione EXPORT_APEX_APPLICATION (che è presente nella directory di questo sorgente)
"""

#Librerie sistema
import os
import sys
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from ricerca_stringhe_ui import Ui_MainWindow
#Librerie interne SmiGrep
from preferenze import preferenze
from test_app import Test_App
from utilita import pathname_icons

class ricerca_stringhe_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """            
    def b_pathname_slot(self):
        print('ciao')
        
    def b_excludepath_slot(self):
        print('richiama dialog')
        
    def b_save_slot(self):
        print('salva ricerca')
    
    def b_search_slot(self):
        print('avvia ricerca')
        
    def b_add_line_slot(self):
        print('aggiunge ai preferiti')
        
    def o_lst1_slot(self):
        print('doppio click sulla lista')    

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = ricerca_stringhe_class()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())