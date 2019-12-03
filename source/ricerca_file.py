# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 03/12/2019
 Descrizione...: Programma per la ricerca dei file all'interno del file system
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file ricerca_file_ui.py è ricavato partendo da ricerca_file_ui.ui 
"""

#Librerie sistema
import os
import sys
#Librerie di data base
import sqlite3
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from ricerca_file_ui import Ui_Ricerca_file_window
#Librerie interne 
from preferenze import preferenze
from utilita import message_error, message_info
       
class ricerca_file_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca dei file all'interno del file system
    """                
    def __init__(self):
        super(ricerca_file_class, self).__init__()
        self.ui = Ui_Ricerca_file_window()
        self.ui.setupUi(self)
        
        # creo un oggetto modello che va ad agganciarsi all'oggetto grafico lista
        self.lista_risultati = QtGui.QStandardItemModel()        
        self.ui.o_lst1.setModel(self.lista_risultati)
        
        # variabili per controllo caricamento della cache
        self.v_t2_pathname = ''
        self.v_t2_filter = ''
        self.v_t2_excludepath = ''        
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        

        # imposto i valori ricevuti come preferiti                
        self.ui.e_filesearch.setText( self.o_preferenze.filesearch )
        self.ui.e_pathname.setText( self.o_preferenze.pathname2 )
        self.ui.e_excludepath.setText( self.o_preferenze.excludepath2 )
        self.ui.e_filter.setText( self.o_preferenze.filter2 )
        
    def b_excludepath_slot(self):
        """
            button esclusioni in tab string search apre la finestra di dialogo per selezionare una directory
        """
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose a directory")                  
        if dirName != "":
            # Prenderò solo la parte della directory, di solito la seconda posizione
            directory_scelta = os.path.split( dirName )[1]
            if directory_scelta != '':
                if self.ui.e_excludepath.displayText() != '':
                    self.ui.e_excludepath.setText(self.ui.e_excludepath.displayText() + ',' + directory_scelta)
                else:
                    self.ui.e_excludepath.setText(directory_scelta)     
    
    def b_pathname_slot(self):
        """
          apre la finestra di dialogo per selezionare una directory
        """        
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose a directory")                  
        if dirName != "":
            self.ui.e_pathname.setText( dirName )        
                
    def b_save_slot(self):
        """
           Salva i parametri di ricerca
	"""               
        self.o_preferenze.filesearch = self.ui.e_filesearch.displayText()
        self.o_preferenze.pathname2 = self.ui.e_pathname.displayText()
        self.o_preferenze.excludepath2 = self.ui.e_excludepath.displayText()
        self.o_preferenze.filter2 = self.ui.e_filter.displayText()
        self.o_preferenze.salva()        
        
        message_info('Search options saved!')
    
    def b_add_line_slot(self):                
        """
            aggiunge la riga nei preferiti (selezione corrente sulla lista)
        """        
        v_selindex = self.lista_risultati.itemFromIndex( self.ui.o_lst1.currentIndex() )
        if v_selindex != None:
            v_seltext = v_selindex.text()
            if v_seltext != '':
                f_output = open(self.o_preferenze.favorites_file, 'a')
                f_output.write(v_seltext + '\n')
                f_output.close()
                           
    def o_lst1_slot(self, p_index):
        """
            doppio click su listbox di ricerca stringa apre il file indicato
        """    
        v_selindex = self.lista_risultati.itemFromIndex(p_index)
        v_seltext = v_selindex.text()
                
        if v_seltext != '':
            try:
                os.startfile(v_seltext)
            except:
                message_error('File not found or problem during open application!')             

    def copy_file_system_in_db(self,
                               v_sqlite_db_name,
                               v_root_node,
                               v_filter,
                               v_exclude):
        """
            Copia nella tabella FILE_SYSTEM del db p_sqlite_db_name
            tutto l'albero dei files, partendo dalla radice p_path_name

            Nota Bene: Passando p_sqlite_db_name = ':MEMORY' verrà creato in RAM e non su disco
        """
        # Apre il DB sqlite
        v_sqlite_conn = sqlite3.connect(database=v_sqlite_db_name)
        # Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()

        # Cancello la tabella se già presente nel db sqlite
        try:
            v_sqlite_cur.execute('DROP TABLE FILE_SYSTEM')
        except:
            pass

        # Creo la tabella
        v_sqlite_cur.execute('CREATE TABLE FILE_SYSTEM (DIR_NAME VARCHAR2(1000), FILE_NAME VARCHAR2(1000))')

        # ricavo una tupla contenente i filtri di ricerca separati
        v_filtri_ricerca = v_filter.split(',')

        # ricavo una tupla contenente le directory da escludere
        v_exclude_ricerca = v_exclude.split(',')

        # lista dei files contenuti nella directory (os.walk restituisce le tuple di tutte le directory partendo dal punto di root)
        v_progress_step = 0
        for root, dirs, files in os.walk(v_root_node):
            # emetto messaggio sulla progress bar
            self.progress.setValue(v_progress_step);     
            self.progress_label.setText('Load file system cache...please wait...')
            self.progress.setLabel(self.progress_label)  
            v_progress_step += 10
            self.progress.setValue(v_progress_step);                 
            # elimino dall'albero delle dir quelle che vanno escluse!
            # Se la stessa dir fosse presente anche ai livelli successivi, viene eliminata anche da li
            for i in range(0, len(v_exclude_ricerca)):
                if v_exclude_ricerca[i] in dirs:
                    dirs.remove(v_exclude_ricerca[i])
            # scorro le tuple dei nomi dentro tupla dei files
            for name in files:
                # stesso discorso istruzione precedente per quanto riguarda la directory (viene poi salvata nel file risultato)
                v_dir = os.path.join(root)
                # stesso discorso istruzione precedente per quanto riguarda il file (viene poi salvata nel file risultato)
                v_file = os.path.join(name)
                # se presenti i filtri di ricerca --> controllo che il file corrisponda alla lista indicata
                v_file_is_valid = False
                if v_filter != '':
                    for i in range(0, len(v_filtri_ricerca)):
                        if v_file.find(v_filtri_ricerca[i]) > 0:
                            v_file_is_valid = True
                            break
                else:
                    v_file_is_valid = True
                # se file è valido --> lo scrivo nel db
                if v_file_is_valid:
                    # scrittura del risultato della ricerca
                    v_sql = "INSERT INTO FILE_SYSTEM(DIR_NAME, FILE_NAME) VALUES(:v_dir,:v_file)"
                    v_sqlite_cur.execute(v_sql, {'v_dir': v_dir, 'v_file': v_file})
                    # refresh della window (per avanzamento della progress bar)
                    #self.wait_win.Pulse()
        # commit
        v_sqlite_conn.commit()
        # chiusura dei cursori
        v_sqlite_conn.close()    
        
    def ricerca_file(self,
                     v_root_node,
                     v_filesearch,
                     v_filter,
                     v_exclude):
        """
            ricerca file
        """        
        # Se richiesto dal flag della cache...
        if self.ui.c_cache_file_system.isChecked():
            # copio il file system dentro la cache di un db sqlite (questo per velorizzare le ricerche successive)
            self.copy_file_system_in_db(self.o_preferenze.name_file_for_db_cache,
                                        v_root_node,
                                        v_filter,
                                        v_exclude)
            # la cache è caricata e non è necessario ricaricarla successivamente
            self.ui.c_cache_file_system.setChecked(False)

        # Apre il DB sqlite
        v_sqlite_conn = sqlite3.connect(database=self.o_preferenze.name_file_for_db_cache)
        # Indico al db di funzionare in modalità str altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()
        v_sqlite_cur.execute("SELECT DIR_NAME, FILE_NAME FROM FILE_SYSTEM WHERE UPPER(FILE_NAME) LIKE :filesearch",
                             {'filesearch': '%' + v_filesearch + '%'})
        for row in v_sqlite_cur:
            # visualizzo output nell'area di testo (normalizzo la pathname del file con i separatori corretti)
            v_nome_completo_file = os.path.normpath(row[0] + "/" + row[1])
            self.lista_risultati.appendRow(QtGui.QStandardItem(v_nome_completo_file))                                            
        
        # Chiudo connessione
        v_sqlite_conn.close()
                
    def b_search_slot(self):
        """
            esegue la ricerca del file
        """
        # creazione della wait window
        self.progress = QtWidgets.QProgressDialog(self)        
        self.progress.setMinimumDuration(0)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Please wait...")        
        # imposto valore minimo e massimo a 0 in modo venga considerata una progress a tempo indefinito
        # Attenzione! dentro nel ciclo deve essere usata la funzione setvalue altrimenti non visualizza e non avanza nulla!
        self.progress.setMinimum(0)
        self.progress.setMaximum(0) 
        # creo un campo label che viene impostato con 100 caratteri in modo venga data una dimensione di base standard
        self.progress_label = QtWidgets.QLabel()            
        self.progress_label.setText('.'*100)
        # collego la label già presente nell'oggetto progress bar con la mia label 
        self.progress.setLabel(self.progress_label)                                                
        
        v_ok = True
        # controllo che ci siano i dati obbligatori
        if self.ui.e_filesearch.displayText() == '':
            message_error('Please enter a file name')
            v_ok = False
        if self.ui.e_pathname.displayText() == '':
            message_error('Please enter a pathname')
            v_ok = False

        # i controlli sono stati superati --> avvio la ricerca
        if v_ok:
            # Se la cache non è attiva, controllo se sono cambiati i valori di ricerca (es. path) perché allora vuol dire che la cache va ripristinata
            if not self.ui.c_cache_file_system.isChecked():
                if self.v_t2_pathname != self.ui.e_pathname.displayText() or self.v_t2_filter != self.ui.e_filter.displayText() or self.v_t2_excludepath != self.ui.e_excludepath.displayText():
                    # I valori sono cambiati e la cache va ricaricata
                    self.ui.c_cache_file_system.setChecked()

            # Carico le var globali che permetteranno il confronto ai giri successivi. In pratica la cache va ricaricata automaticamente se sono cambiati dei parametri di ricerca
            self.v_t2_pathname = self.ui.e_pathname.displayText()
            self.v_t2_filter = self.ui.e_filter.displayText()
            self.v_t2_excludepath = self.ui.e_excludepath.displayText()

            # pulizia dell'item dei risultati            
            self.lista_risultati.clear()            

            # richiama la ricerca nel file system se presente file system
            self.ricerca_file(self.ui.e_pathname.displayText(),
                              self.ui.e_filesearch.displayText(),
                              self.ui.e_filter.displayText(),
                              self.ui.e_excludepath.displayText())

            # chiudo la wait window
            self.progress.close()                                           
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = ricerca_file_class()
    application.show()
    sys.exit(app.exec())        