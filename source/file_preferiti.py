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
#Libreria per gestione zip
import zipfile
#Libreria per gestione date
import datetime
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from file_preferiti_ui import Ui_file_preferiti_window
#Librerie interne 
from preferenze import preferenze
from utilita import message_error, message_info, message_question_yes_no
       
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
        self.setAcceptDrops(True)        
        
    def dragMoveEvent(self, e):
        print('Marco! era così semplice!!!')
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()        
        
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
        f_output = open(self.o_preferenze.favorites_file, 'w')
        for v_index in range( self.lista_risultati.rowCount() ):
            v_item = self.lista_risultati.item(v_index)
            f_output.write( v_item.text() + '\n')

        # chiudo il file dei risultati
        f_output.close()
        
    def slot_open_folder(self):
        """
            Apre la cartella dove si trova il file selezionato
        """
        try:
            # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
            v_index = self.ui.o_lst1.selectedIndexes()[0]                    
            v_item = self.lista_risultati.itemFromIndex(v_index)
            v_seltext = v_item.text()                                                     
            if v_seltext != '':
                try:
                    os.startfile(v_seltext[0:v_seltext.rfind('\\')])
                except:
                    message_error('Problem during open object folder!')
        except:
            message_error('Problem during open object folder!')
        
    def slot_backup_line(self):
        """
            Copia il file indicato all'interno di un file zip di nome Old, presente nella medesima
            cartella del file di partenza. Se il file zip non esiste, viene creato. Se esiste il file
            indicato viene accodato
        """
        if message_question_yes_no("Do you want to backup file into old.zip?") == 'Yes':
            # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
            try:
                v_index = self.ui.o_lst1.selectedIndexes()[0]                    
            except:
                return
            v_item = self.lista_risultati.itemFromIndex(v_index)
            v_seltext = v_item.text()                                                     
            #scompongo l'intera pathname in tutte le sue componenti (directory, nome file, suffisso)
            v_directory = os.path.split(v_seltext)[0]
            v_solo_nome_file = os.path.split(v_seltext)[1]
            v_solo_nome_file_senza_suffisso = os.path.splitext(v_solo_nome_file)[0]
            v_suffisso_nome_file = os.path.splitext(v_solo_nome_file)[1]
            #prendo la data di sistema che servirà per dare un suffisso al nome del file che viene zippato
            v_system_date = datetime.datetime.now()
            v_str_data  = '_' + str(v_system_date.year) + '_' + str(v_system_date.month) + '_' + str(v_system_date.day)
            if v_directory != '':
                try:
                    #apro il file zip (se non esiste lo creo)
                    v_zip = zipfile.ZipFile(v_directory + '\\old.zip','a')
                    #accodo il file indicato allo zip (il nome di arrivo è il nome del file più suffisso data)
                    v_zip.write(v_seltext, v_solo_nome_file_senza_suffisso + v_str_data + '.' + v_suffisso_nome_file)
                    #chiudo lo zip e emetto messaggio che procedura terminata
                    v_zip.close()
                    message_info('The file ' + v_solo_nome_file + ' is been copied into Old.zip')
                except:
                    message_error('Error to copy the file into Old zip!')        
                    
    def pubblica(self, p_tipo_server):
        """
            Pubblica il file Oracle Form o Oracle Report nei server indicati
            se p_tipo_server = 1 compila in SMILE, altrimenti in ICOM
        """
        # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
        try:
            v_index = self.ui.o_lst1.selectedIndexes()[0]                    
        except:
            return        
        v_item = self.lista_risultati.itemFromIndex(v_index)
        v_file = v_item.text()                                
        
        # tipo server
        if p_tipo_server == '1':
            v_nome = 'SMILE'
        else:
            v_nome = 'ICOM'
        # se è stato selezionato qualcosa
        if v_file != '' and message_question_yes_no("Do you want to compile the file " + chr(10) + v_file + chr(10) + "and post it in " + v_nome + " system?") == 'Yes':
            #sono ammessi solo file con suffissi specifici
            if '.fmb' not in v_file and '.rdf' not in v_file:
                message_error('File is not in format "Oracle Form" or "Oracle Report"!')
            else:
                # apro una nuova finestra figlia della principale
                canvas = pubblica_form_report(v_file, 
                                              self.o_preferenze.work_dir, 
                                              p_tipo_server)
        
    def slot_pubblica_smile(self):
        """
            Pubblica in SMILE
        """
        self.pubblica('1')        
        
    def slot_pubblica_icom(self):
        """
            Pubblica in ICOM
        """
        self.pubblica('2')        
    
    def compila(self, p_nome_programma, p_server):
        """
            Compila il p_nome_programma
        """        
        if p_nome_programma != '':
            try:                
                os.system('c:\ITCCONF\compilaauto.bat "' + p_nome_programma + '" ' + p_server)
            except:
                message_error('Problem during object compile!')
        
    def slot_compile_icom_backup1(self):
        """
            Compila l'oggetto selezionato icom backup1
        """
        # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
        v_index = self.ui.o_lst1.selectedIndexes()[0]                    
        v_item = self.lista_risultati.itemFromIndex(v_index)
        v_seltext = v_item.text()                                                     
        
        # compila
        self.compila(v_seltext, "smi/smi@backup_815")
                
    def slot_compile_icom_backup2(self):
        """
            Compila l'oggetto selezionato icom backup2
        """
        # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
        v_index = self.ui.o_lst1.selectedIndexes()[0]                    
        v_item = self.lista_risultati.itemFromIndex(v_index)
        v_seltext = v_item.text()                                                     
        
        # compila
        self.compila(v_seltext, "smi/smi@backup_2_815")        
        
    def slot_compile_smile_backup1(self):
        """
            Compila l'oggetto selezionato smile backup1
        """
        # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
        v_index = self.ui.o_lst1.selectedIndexes()[0]                    
        v_item = self.lista_risultati.itemFromIndex(v_index)
        v_seltext = v_item.text()                                                     
        
        # compila
        self.compila(v_seltext, "smile/smile@backup_815")
                
    def slot_compile_smile_backup2(self):            
        """
            Compila l'oggetto selezionato smile backup2
        """
        # ricerco la posizione dell'indice selezionato e ne ricavo il contenuto 
        v_index = self.ui.o_lst1.selectedIndexes()[0]                    
        v_item = self.lista_risultati.itemFromIndex(v_index)
        v_seltext = v_item.text()                                                     
        
        # compila
        self.compila(v_seltext, "smile/smile@backup_2_815")
    
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
    application = file_preferiti_class()
    application.show()
    sys.exit(app.exec())        