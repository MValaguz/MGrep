# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 17/12/2019
 Descrizione...: Programma per la gestione di un elenco di directory preferite.
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file directory_preferite_ui.py è ricavato partendo da directory_preferite_ui.ui 
"""

#Librerie sistema
import os
import sys
#Libreria per gestione date
import datetime
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from directory_preferite_ui import Ui_directory_preferite_window
#Librerie interne 
from preferenze import preferenze
from utilita import message_error, message_info, message_question_yes_no
       
class directory_preferite_class(QtWidgets.QMainWindow):
    """
        Programma per la gestione delle directory preferite
    """                
    def __init__(self):
        super(directory_preferite_class, self).__init__()
        self.ui = Ui_directory_preferite_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        
        
        # creo un oggetto modello che va ad agganciarsi all'oggetto grafico lista
        self.lista_risultati = QtGui.QStandardItemModel()        
        self.ui.o_lst1.setModel(self.lista_risultati)            
        
        # carica la lista dei preferiti
        self.carica_directory_preferite()
        
        # attivo il drag and drop (da notare come questa attivazione di fatto sembra valere per tutti gli elementi)
        self.setAcceptDrops(True)                
            
    def dragEnterEvent(self, event):
        """
           Attivo evento di drag sovrascrivendolo alla classe sottostante 
        """
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()    

    def dropEvent(self, event):        
        """
           Attivo evento di drop. Attenzione! Senza evento di drag di cui sopra, il drop non funzionerebbe!
        """        
        if event.mimeData().hasText():
            mime = event.mimeData()
            elementi = mime.text().split("file:///")            
            # prendo tutti gli elementi e li aggiungo alla lista                        
            for elemento in elementi:                                
                if elemento != '':
                    # normalizza il path name del file
                    elemento_normalizzato = os.path.normpath(elemento).replace(chr(10),'')                    
                    # estraggo solo la directory
                    nome_dir = os.path.dirname(elemento_normalizzato)
                    self.lista_risultati.appendRow(QtGui.QStandardItem(nome_dir))        
            
    def carica_directory_preferite(self):
        """
            Carica quanto presente nel file dei preferiti
        """
        self.lista_risultati.clear()
        try:
            v_file = open(self.o_preferenze.favorites_dirs, 'r')
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
        """
            Inserisce una riga vuota all'interno della lista
        """        
        try:
            v_index = self.ui.o_lst1.selectedIndexes()[0]        
            v_row = v_index.row()
        except:
            v_row = 0
         
        self.lista_risultati.insertRow(v_row, QtGui.QStandardItem('-'*100))                                
        
    def slot_sposta_su(self):
        """
            Sposta verso l'alto la riga selezionata
        """
        try:
            v_index = self.ui.o_lst1.selectedIndexes()[0]        
            v_row = v_index.row()
        except:
            return        
        if v_row > 0:
            v_item = self.lista_risultati.itemFromIndex(v_index)
            v_seltext = v_item.text()                                     
            self.lista_risultati.removeRow( v_index.row() )
            self.lista_risultati.insertRow( v_row - 1 , QtGui.QStandardItem(v_seltext) )            
            v_new_index = self.ui.o_lst1.model().index(v_row - 1 , 0)            
            self.ui.o_lst1.setCurrentIndex(v_new_index)        
        
    def slot_sposta_giu(self):
        """
            Sposta verso il basso la riga selezionata
        """
        try:
            v_index = self.ui.o_lst1.selectedIndexes()[0]        
            v_tot = self.lista_risultati.rowCount()
            v_row = v_index.row()
        except:
            return                
        if v_row < v_tot-1:
            v_item = self.lista_risultati.itemFromIndex(v_index)
            v_seltext = v_item.text()                                     
            self.lista_risultati.removeRow( v_index.row() )
            self.lista_risultati.insertRow( v_row + 1 , QtGui.QStandardItem(v_seltext) )            
            v_new_index = self.ui.o_lst1.model().index(v_row + 1 , 0)            
            self.ui.o_lst1.setCurrentIndex(v_new_index)        
        
    def slot_delete_line(self):
        """
            Cancella la riga selezionata
        """
        try:
            v_index = self.ui.o_lst1.selectedIndexes()[0]                                
        except:
            return                
        
        self.lista_risultati.removeRow( v_index.row() )        
        
    def slot_clear(self):
        """
           Cancella l'intera lista
        """
        if message_question_yes_no('Do you want to clear result list?') == 'Yes':
            self.lista_risultati.clear()
        
    def slot_save(self):
        """
           Salva elenco lista file preferiti
        """
        f_output = open(self.o_preferenze.favorites_dirs, 'w')
        for v_index in range( self.lista_risultati.rowCount() ):
            v_item = self.lista_risultati.item(v_index)
            f_output.write( v_item.text() + '\n')

        # chiudo il file dei risultati
        f_output.close()
            
    def slot_doppio_click_lista(self, p_index):
        """
            Doppio click su listbox
        """
        v_selindex = self.lista_risultati.itemFromIndex(p_index)
        v_seltext = v_selindex.text() 
        if v_seltext != '':
            try:
                os.startfile(v_seltext)
            except:
                message_error('File not found or problem during open application!')
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = directory_preferite_class()
    application.show()
    sys.exit(app.exec())        