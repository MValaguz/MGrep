# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 25/08/2019
 Descrizione...: Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms ecc.
 
 Note..........: Per far funzionare la ricerca di Apex è necessario che sotto Oracle sia installata la funzione EXPORT_APEX_APPLICATION (che è presente nella directory di questo sorgente)
                 Il layout è stato creato utilizzando qtdesigner e il file ricerca_stringhe_ui.py è ricavato partendo da ricerca_stringhe_ui.ui 
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
from utilita import message_error
       
class ricerca_stringhe_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self):
        super(ricerca_stringhe_class, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        

        # imposto i valori ricevuti come preferiti        
        self.ui.e_stringa1.setText( self.o_preferenze.stringa1 )
        self.ui.e_stringa2.setText( self.o_preferenze.stringa2 )
        self.ui.e_pathname.setText( self.o_preferenze.pathname )
        self.ui.e_excludepath.setText( self.o_preferenze.excludepath )
        self.ui.e_outputfile.setText( self.o_preferenze.outputfile )
        self.ui.e_filter.setText( self.o_preferenze.filter )
        self.ui.c_flsearch.setChecked( self.o_preferenze.flsearch  )
        self.ui.e_dboracle1.setText( self.o_preferenze.dboracle1 )
        self.ui.e_dboracle2.setText( self.o_preferenze.dboracle2 )
        self.ui.c_dbsearch.setChecked( self.o_preferenze.dbsearch )
        self.ui.c_apexsearch.setChecked( self.o_preferenze.flapexsearch )
        self.ui.e_dbapex.setText( self.o_preferenze.dbapexsearch )                               
    
    def b_pathname_slot(self):
        """
          selezione in tab string search apre la finestra di dialogo per selezionare una directory
        """        
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose a directory")                  
        if dirName != "":
            self.ui.e_pathname.setText( dirName )        
        
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
        
    def b_save_slot(self):
        print('salva ricerca')
    
    def b_add_line_slot(self):
        print('aggiunge ai preferiti')
        
    def o_lst1_slot(self):
        print('doppio click sulla lista')  
        
    def apre_source_db(self,
                       p_obj_type,
                       p_obj_name):
        """
            apre oggetto di db
        """
        def creazione_del_file_da_db(p_db):
            try:
                # connessione a oracle (1)
                v_connection = cx_Oracle.connect(p_db)
                v_error = False
            except:
                message_error('Connection to oracle rejected. Please control login information.')
                v_error = True

            if not v_error:
                # apro il file di output che conterra' i risultati della ricerca
                f_output = open(os.path.join(self.o_preferenze.work_dir, 'temp_source_db.sql'), 'w')

                # apro cursore
                v_cursor = v_connection.cursor()
                v_cursor_det = v_connection.cursor()
                v_count_line = 0

                # lettura del sorgente
                if p_obj_type == 'PACKAGE':
                    v_cursor_det.prepare("SELECT TEXT, LINE FROM USER_SOURCE WHERE NAME=:p_name ORDER BY TYPE, LINE")
                    v_cursor_det.execute(None, {'p_name': p_obj_name})
                elif p_obj_type in ('PROCEDURE', 'FUNCTION', 'TRIGGER'):
                    v_cursor_det.prepare("SELECT TEXT FROM USER_SOURCE WHERE NAME=:p_name ORDER BY TYPE, LINE")
                    v_cursor_det.execute(None, {'p_name': p_obj_name})
                elif p_obj_type == 'TABLE' or p_obj_type == 'VIEW':
                    v_cursor_det.prepare(
                        "SELECT A.COLUMN_NAME || ' = ' || B.COMMENTS FROM ALL_TAB_COLUMNS A, ALL_COL_COMMENTS B WHERE A.OWNER=:p_owner AND A.TABLE_NAME = :p_name AND A.OWNER=B.OWNER AND A.TABLE_NAME=B.TABLE_NAME AND A.COLUMN_NAME=B.COLUMN_NAME")
                    v_cursor_det.execute(None, {'p_owner': 'SMILE', 'p_name': p_obj_name})

                # scrivo il sorgente nel file
                v_1a_riga = True
                for result in v_cursor_det:
                    v_count_line = v_count_line + 1
                    # sorgente di package
                    if p_obj_type == 'PACKAGE':
                        if result[1] == 1:
                            if v_1a_riga:
                                f_output.write('CREATE OR REPLACE ' + result[0])
                            else:
                                f_output.write('\n' + '/' + '\n')
                                f_output.write('CREATE OR REPLACE ' + result[0])
                        else:
                            f_output.write(result[0])
                            # sorgente di procedura, funzione, trigger
                    elif p_obj_type in ('PROCEDURE', 'FUNCTION', 'TRIGGER'):
                        if v_1a_riga:
                            f_output.write('CREATE OR REPLACE ' + result[0])
                        else:
                            f_output.write(result[0])
                            # sorgente di tabella
                    else:
                        f_output.write(result[0] + '\n')
                    v_1a_riga = False

                # chiusura cursori e connessione DB e file di lavoro
                v_cursor.close()
                v_connection.close()
                f_output.close()

                # restituisco il numero di righe processate
                return v_count_line

        # creo il file sorgente presupponendo sia stato trovato sul db indicato dalla connessione1
        if self.e_dboracle1.GetValue() != '':
            v_count_line = creazione_del_file_da_db(self.e_dboracle1.GetValue())
            # se il file creato è vuoto allora richiamo la stessa procedura ma con la connessione2
            if v_count_line == 0 and self.e_dboracle2.GetValue() != '':
                v_count_line = creazione_del_file_da_db(self.e_dboracle2.GetValue())

        # apre il file appena creato
        os.startfile(os.path.join(self.o_preferenze.work_dir, 'temp_source_db.sql'))

    def apre_source_apex(self,                         
                         p_obj_name):
        """
            apre source di Apex
        """        
        if self.e_dbapex.GetValue() != '':        
            try:
                # connessione a oracle apex
                v_connection = cx_Oracle.connect(self.e_dbapex.GetValue())
                v_error = False
            except:
                message_error('Connection to oracle rejected. Please control login information.')
                v_error = True

            if not v_error:
                wait_win = PBI.PyBusyInfo(message="Please wait a moment...", parent=None, title="Recompiling")
                # apro il file di output che conterra' i risultati della ricerca
                f_output = open(os.path.join(self.o_preferenze.work_dir, 'temp_source_apex.sql'), 'w')
                # apro cursore
                v_cursor = v_connection.cursor()
                v_cursor_det = v_connection.cursor()
                # richiamo la procedura che esporta il sorgente di Apex
                v_cursor_det.prepare("SELECT EXPORT_APEX_APPLICATION(:application_id) FROM dual")
                v_cursor_det.execute(None, {'application_id': p_obj_name})
                # leggo la prima colonna della lista che viene restituita dal cursore di oracle e che contiene il clob con l'export in formato testuale dell'applicazione Apex                
                v_result = v_cursor_det.var(cx_Oracle.CLOB)   
                v_result = v_cursor_det.fetchone()[0]                                
                # scrivo il clob in un file 
                f_output.write(v_result.read())                
                # chiusura cursori e connessione DB e file di lavoro
                v_cursor.close()
                v_connection.close()
                f_output.close()                
                # apre il file appena creato
                os.startfile(os.path.join(self.o_preferenze.work_dir, 'temp_source_apex.sql') )
                # chiudo la window di attesa
                del wait_win
    
    def doppio_click(self,event):
        """
            doppio click su listbox di ricerca stringa apre il file indicato
        """
        v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        # apro il source scelto a video in base alla tipologia di appartenenza
        if v_seltext[0:11] == 'PACKAGE -->':
            self.apre_source_db('PACKAGE', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:11] == 'TRIGGER -->':
            self.apre_source_db('TRIGGER', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:13] == 'PROCEDURE -->':
            self.apre_source_db('PROCEDURE', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:12] == 'FUNCTION -->':
            self.apre_source_db('FUNCTION', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:9] == 'TABLE -->':
            self.apre_source_db('TABLE', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:8] == 'VIEW -->':
            self.apre_source_db('VIEW', v_seltext[v_seltext.find('>') + 2:len(v_seltext)])
        elif v_seltext[0:8] == 'APEX -->':
            v_pos_inizio = v_seltext.find('(')
            v_pos_fine   = v_seltext.find(')')            
            self.apre_source_apex(v_seltext[v_pos_inizio + 1 : v_pos_fine])        
        # documento windows (es. form o report, doc, xls, ecc.)
        elif v_seltext != '':
            try:
                os.startfile(v_seltext)
            except:
                message_error('File not found or problem during open application!')

    def aggiunge_riga_preferiti(self, event):
        """
            aggiunge la riga nei preferiti
        """
        f_output = open(self.o_preferenze.favorites_file, 'a')
        f_output.write(self.o_lst1.GetString(self.o_lst1.GetSelection()) + '\n')
        f_output.close()

    def salva_preferenze(self, event):
        self.o_preferenze.stringa1 = self.e_stringa1.GetValue()
        self.o_preferenze.stringa2 = self.e_stringa2.GetValue()
        self.o_preferenze.pathname = self.e_pathname.GetValue()
        self.o_preferenze.excludepath = self.e_excludepath.GetValue()
        self.o_preferenze.outputfile = self.e_outputfile.GetValue()
        self.o_preferenze.filter = self.e_filter.GetValue()
        self.o_preferenze.flsearch = self.c_flsearch.GetValue()
        self.o_preferenze.dboracle1 = self.e_dboracle1.GetValue()
        self.o_preferenze.dboracle2 = self.e_dboracle2.GetValue()
        self.o_preferenze.dbsearch = self.c_dbsearch.GetValue()
        self.o_preferenze.flapexsearch = self.c_apexsearch.GetValue()
        self.o_preferenze.dbapexsearch = self.e_dbapex.GetValue()                
        self.o_preferenze.salva()

    def ricerca_stringa_in_file(self,
                                v_root_node,
                                v_string1,
                                v_string2,
                                v_output,
                                v_filter,
                                v_exclude):
        """
            ricerca stringa in file
        """
        # ricavo una tupla contenente i filtri di ricerca separati
        v_filtri_ricerca = v_filter.split(',')

        # ricavo una tupla contenente le directory da escludere
        v_exclude_ricerca = v_exclude.split(',')

        # apro il file di output che conterra' i risultati della ricerca
        f_output = open(v_output, 'a')
        
        v_progress_step = 0        
        # lista dei files contenuti nella directory (os.walk restituisce le tuple di tutte le directory partendo dal punto di root)        
        for root, dirs, files in os.walk(v_root_node):
            # fermo il loop se richiesto da utente
            if self.progress.wasCanceled():
                break
            # elimino dall'albero delle dir quelle che vanno escluse!
            # Se la stessa dir fosse presente anche ai livelli successivi, viene eliminata anche da li
            for i in range(0, len(v_exclude_ricerca)):
                if v_exclude_ricerca[i] in dirs:
                    dirs.remove(v_exclude_ricerca[i])
            # scorro le tuple dei nomi dentro tupla dei files            
            for name in files:
                # fermo il loop se richiesto da utente
                if self.progress.wasCanceled():
                    break
                # partendo dalla directory e dal nome file, uso la funzione join per avere il nome del file completo
                v_file_name = os.path.join(root, name)
                # stesso discorso istruzione precedente per quanto riguarda la directory (viene poi salvata nel file risultato)
                v_dir = os.path.join(root)
                v_dir_is_valid = True
                # if v_exclude != '':
                #    for i in range(0,len(v_exclude_ricerca)):
                #        if string.find(os.path.normpath(v_dir),os.path.normpath(v_exclude_ricerca[i]))<>-1:
                #            v_dir_is_valid = False
                #            break
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
                # se nome del file è valido
                if v_dir_is_valid and v_file_is_valid:
                    # apertura del file (in modo binario! la documentazione dice che la modalita rb vale solo per sistema MS-WIN)
                    # viene tentata l'apertura tramite una try perché tra il momento di creazione della lista dei file da
                    # elaborare e l'effettiva lettura, il file potrebbe essere stato eliminato
                    try:
                        f_input = open(v_file_name,'rb')  # Con il passaggio a python3.6 non funzionava più correttamente
                        v_file_is_open = True
                    except:
                        print('File ' + v_file_name + ' non trovato!')
                        v_file_is_open = False
                    if v_file_is_open:
                        # estraggo dal nome file l'estensione e il nome (servono per scrivere il csv)
                        v_only_file_name, v_only_file_extension = os.path.splitext(v_file)
                        # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                        v_progress_step += 1
                        self.progress.setValue(v_progress_step);                        
                        self.progress_label.setText(v_file_name)
                        self.progress.setLabel(self.progress_label)                                                
                        # Lettura di tutto il file  
                        try:
                            f_contenuto = f_input.read().upper()
                        except MemoryError:
                            message_error('File ' + v_file_name + ' is too big! It was skipped!')
                            
                        # utente ha richiesto di ricercare due stringhe in modalita AND
                        if len(v_string1) > 0 and len(v_string2) > 0:
                            if f_contenuto.find(bytes(v_string1.upper(), encoding='latin-1')) >= 0 and f_contenuto.find(
                                    bytes(v_string2.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.lista_risultati.appendRow(QtGui.QStandardItem(v_file_name))                                
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # utente ha richiesto di ricercare solo una stringa, la prima
                        elif len(v_string1) > 0:
                            if f_contenuto.find(bytes(v_string1.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.lista_risultati.appendRow(QtGui.QStandardItem(v_file_name))                                
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # utente ha richiesto di ricercare solo una stringa, la seconda
                        elif len(v_string2) > 0:
                            if f_contenuto.find(bytes(v_string2.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.lista_risultati.appendRow(QtGui.QStandardItem(v_file_name))                                
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # chiudo il file
                        f_input.close()
        f_output.close()

    def b_search_slot(self):
        """
            esegue la ricerca delle stringhe
        """
        # creo un job che si mette in attesa di una risposta così da lasciare libera l'applicazione da questo lavoro
        # viene passato al thread l'oggetto chat
        #-self.thread_wait_window = class_wait_window()
        # collego il thread con la relativa funzione
        #self.thread_in_attesa.signal.connect(self.ricevo_il_messaggio)
        #-self.thread_wait_window.start()
        
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
        if self.ui.e_stringa1.displayText() == '' and self.ui.e_stringa2.displayText() == '':
            message_error('Please enter string1 or string2 value')
            v_ok = False
        if not self.ui.c_flsearch.isChecked() and not self.ui.c_dbsearch.isChecked() and not self.ui.c_apexsearch.isChecked():
            message_error('Select execute search in Folder or DB or Apex')
            v_ok = False
        if self.ui.c_flsearch.isChecked() and self.ui.e_pathname.displayText() == '':
            message_error('Please enter a pathname')
            v_ok = False
        if self.ui.c_dbsearch.isChecked() and self.ui.e_dboracle1.displayText() == '' and self.ui.e_dboracle2.displayText() == '':
            message_error('Please enter a DB name')
            v_ok = False
        if self.ui.c_apexsearch.isChecked() and self.ui.e_dbapex.displayText() == '':
            message_error('Please enter a Apex DB name')
            v_ok = False            
        if self.ui.e_outputfile.displayText() == '':
            message_error('Please enter an output file')
            v_ok = False
        # i controlli sono stati superati --> avvio la ricerca
        if v_ok:
            # pulizia dell'item dei risultati
            self.lista_risultati = QtGui.QStandardItemModel()
            self.lista_risultati.clear()
            self.ui.o_lst1.setModel(self.lista_risultati)

            # se presente, pulisco il file di output, oppure lo creo. Perché tutte le fasi di ricerca vanno in accodamento
            f_output = open(self.ui.e_outputfile.displayText(), 'w')
            f_output.close()

            # richiama la ricerca nel file system se presente file system
            if self.ui.c_flsearch.isChecked():
                self.ricerca_stringa_in_file(self.ui.e_pathname.displayText(),
                                             self.ui.e_stringa1.displayText(),
                                             self.ui.e_stringa2.displayText(),
                                             self.ui.e_outputfile.displayText(),
                                             self.ui.e_filter.displayText(),
                                             self.ui.e_excludepath.displayText())

            # visualizzo il risultato (carico il modello dentro la lista)
            self.ui.o_lst1.setModel(self.lista_risultati)                  
            self.progress.close()
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    application = ricerca_stringhe_class()
    application.show()
    sys.exit(app.exec())        