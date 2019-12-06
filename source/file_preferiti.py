# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 06/12/2019
 Descrizione...: Programma per la gestione di un elenco di file preferiti.
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file file_preferiti_ui.py è ricavato partendo da file_preferiti_ui.ui 
"""

#Librerie sistema
import os
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from file_preferiti_ui import Ui_file_preferiti_window
#Librerie interne 
from preferenze import preferenze
from utilita import message_error, message_info
       
class file_preferiti_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self):
        super(file_preferiti_class, self).__init__()
        self.ui = Ui_file_preferiti_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        
        
        # creo un oggetto modello che va ad agganciarsi all'oggetto grafico lista
        self.lista_risultati = QtGui.QStandardItemModel()        
        self.ui.o_lst1.setModel(self.lista_risultati)            
        
        # carica la lista dei preferiti
        self.carica_files_preferiti()
        
    def carica_files_preferiti(self):
        """
            Carica quanto presente nel file dei preferiti
        """
        self.lista_risultati.clear()
        try:
            v_file = open(self.o_preferenze.favorites_file, 'r')
            v_stringa = v_file.readline()
            while v_stringa != '':
                # elimino dalla stringa il carattere di ritorno a capo                
                v_stringa = v_stringa.rstrip('\n')                
                self.lista_risultati.appendRow(QtGui.QStandardItem(v_stringa))                                
                v_stringa = v_file.readline()
            v_file.close()
        except:
            pass    
        
    def slot_refresh(self):
        """
           Ricarica la lista dei preferiti
        """
        self.carica_files_preferiti()
        
    def slot_insert_line(self):
        pass
        
    def slot_sposta_su(self):
        pass
        
    def slot_sposta_giu(self):
        pass
        
    def slot_delete_line(self):
        pass
        
    def slot_clear(self):
        pass
        
    def slot_save(self):
        pass
        
    def slot_open_folder(self):
        pass
        
    def slot_backup_line(self):
        pass
        
    def slot_pubblica_smile(self):
        pass
        
    def slot_pubblica_icom(self):
        pass
        
    def slot_compile_icom_backup1(self):
        pass
        
    def slot_compile_icom_backup2(self):
        pass
        
    def slot_compile_smile_backup1(self):
        pass
        
    def slot_compile_smile_backup2(self):            
        pass
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = file_preferiti_class()
    application.show()
    sys.exit(app.exec())        