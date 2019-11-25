# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 25/08/2019
 Descrizione...: Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms ecc.
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file ricerca_stringhe_ui.py è ricavato partendo da ricerca_stringhe_ui.ui 
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
from ricerca_stringhe_ui import Ui_MyPrefFileWindow
#Librerie interne SmiGrep
from preferenze import preferenze
from utilita import message_error, message_info
       
class ricerca_stringhe_class(QtWidgets.QMainWindow):
    """
        Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self):
        super(ricerca_stringhe_class, self).__init__()
        self.ui = Ui_MyPrefFileWindow()
        self.ui.setupUi(self)
        
        # creo un oggetto modello che va ad agganciarsi all'oggetto grafico lista
        self.lista_risultati = QtGui.QStandardItemModel()        
        self.ui.o_lst1.setModel(self.lista_risultati)
        
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
        """
           Salva i parametri di ricerca
	"""
        self.o_preferenze.stringa1 = self.ui.e_stringa1.displayText()
        self.o_preferenze.stringa2 = self.ui.e_stringa2.displayText()
        self.o_preferenze.pathname = self.ui.e_pathname.displayText()
        self.o_preferenze.excludepath = self.ui.e_excludepath.displayText()
        self.o_preferenze.outputfile = self.ui.e_outputfile.displayText()
        self.o_preferenze.filter = self.ui.e_filter.displayText()
        if self.ui.c_flsearch.isChecked():
            self.o_preferenze.flsearch = True
        else:
            self.o_preferenze.flsearch = False
        self.o_preferenze.dboracle1 = self.ui.e_dboracle1.displayText()
        self.o_preferenze.dboracle2 = self.ui.e_dboracle2.displayText()
        if self.ui.c_dbsearch.isChecked():
            self.o_preferenze.dbsearch = True
        else:
            self.o_preferenze.dbsearch = False
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
        if self.ui.e_dboracle1.displayText() != '':
            v_count_line = creazione_del_file_da_db(self.ui.e_dboracle1.displayText())
            # se il file creato è vuoto allora richiamo la stessa procedura ma con la connessione2
            if v_count_line == 0 and self.ui.e_dboracle2.displayText() != '':
                v_count_line = creazione_del_file_da_db(self.ui.e_dboracle2.displayText())

        # apre il file appena creato
        os.startfile(os.path.join(self.o_preferenze.work_dir, 'temp_source_db.sql'))
    
    def o_lst1_slot(self, p_index):
        """
            doppio click su listbox di ricerca stringa apre il file indicato
        """    
        v_selindex = self.lista_risultati.itemFromIndex(p_index)
        v_seltext = v_selindex.text()
                
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
        v_abort = False
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
                v_abort = True
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
                    v_abort = True
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
        
        return v_abort

    def ricerca_stringa_in_db(self,
                              v_db,
                              v_string1,
                              v_string2,
                              v_output):
        """
            ricerca stringa in dbase
        """
        v_abort = False
        try:
            v_connection = cx_Oracle.connect(v_db)
            v_error = False
        except:
            message_error('Connection to oracle rejected. Search will skipped!')            
            v_error = True

        if not v_error:
            v_progress_step = 0
            
            # apro il file di output che conterra' i risultati della ricerca
            f_output = open(v_output, 'a')

            # apro cursori
            v_cursor = v_connection.cursor()
            v_cursor_det = v_connection.cursor()

            ##############################################################
            # ricerca all'interno di procedure, funzioni, package e trigger
            ##############################################################
            v_cursor.execute(
                "SELECT DISTINCT NAME,TYPE FROM USER_SOURCE WHERE TYPE IN ('PROCEDURE','PACKAGE','TRIGGER','FUNCTION') ORDER BY TYPE, NAME")
            i = 0
            for result in v_cursor:
                if self.progress.wasCanceled():
                    v_abort = True
                    break
                v_c_name = result[0]
                v_c_type = result[1]
                # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                v_progress_step += 1
                self.progress.setValue(v_progress_step);                        
                v_msg = v_c_type + ' --> ' + v_c_name
                self.progress_label.setText(v_msg)
                self.progress.setLabel(self.progress_label)                                               
                # lettura del sorgente (di fatto una lettura di dettaglio di quanto presente nel cursore di partenza                
                # in data 20/12/2018 si è dovuta aggiungere la conversione in ASCII in quanto nel pkg CG_FATTURA_ELETTRONICA risultano annegati caratteri che python non riesce a leggere
                v_cursor_det.prepare("SELECT Convert(TEXT,'US7ASCII') FROM USER_SOURCE WHERE NAME=:p_name ORDER BY LINE")
                v_cursor_det.execute(None, {'p_name': v_c_name})
                # il sorgente finisce dentro la stringa v_sorgente
                v_sorgente = ''
                for result in v_cursor_det:
                    v_sorgente = v_sorgente + v_sorgente.join(result)

                v_sorgente = v_sorgente.upper()
                # utente ha richiesto di ricercare due stringhe in modalita AND
                if len(v_string1) > 0 and len(v_string2) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0 and v_sorgente.find(v_string2.upper()) >= 0:
                        # print('Stringhe trovate in %s' % v_file_name)
                        # visualizzo output nell'area di testo
                        self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:
                        # print('Stringa1 trovata in %s' % v_file_name)
                        self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:
                        # print('Stringa2 trovata in %s' % v_file_name)
                        self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                i += 1
                # if i > 10:
                #	break

            ####################################################
            # ricerca all'interno della definizione delle tabelle
            ####################################################
            if not v_abort:
                v_owner = v_db[0:v_db.find('/')]
                v_cursor.execute(
                    "SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = " + "'" + v_owner + "'" + " ORDER BY TABLE_NAME")
                i = 0
                for result in v_cursor:
                    if self.progress.wasCanceled():
                        v_abort = True
                        break
                    # nome della tabella
                    v_c_name = result[0]
                    v_c_type = 'TABLE'
                    # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                    v_progress_step += 1
                    self.progress.setValue(v_progress_step);                        
                    v_msg = v_c_type + ' --> ' + v_c_name
                    self.progress_label.setText(v_msg)
                    self.progress.setLabel(self.progress_label)                                                               
                    # preparazione select per la lettura delle colonne e relativi commenti di tabella. Gli spazi sono stati inseriti in quanto il sorgente estratto risultava come unica riga e la ricerca successiva non teneva conto di eventuali separatori
                    v_cursor_det.prepare(
                        "SELECT :p_name FROM DUAL UNION SELECT ' ' || A.COLUMN_NAME || ' ' || B.COMMENTS FROM ALL_TAB_COLUMNS A, ALL_COL_COMMENTS B WHERE A.OWNER=:p_owner AND A.TABLE_NAME = :p_name AND A.OWNER=B.OWNER AND A.TABLE_NAME=B.TABLE_NAME AND A.COLUMN_NAME=B.COLUMN_NAME")
                    v_cursor_det.execute(None, {'p_owner': v_owner, 'p_name': v_c_name})
                    # il sorgente finisce dentro la stringa v_sorgente
                    v_sorgente = ''
                    for result in v_cursor_det:
                        v_sorgente = v_sorgente + v_sorgente.join(result)
    
                    v_sorgente = v_sorgente.upper()
    
                    # utente ha richiesto di ricercare due stringhe in modalita AND
                    if len(v_string1) > 0 and len(v_string2) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0 and v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la prima
                    elif len(v_string1) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la seconda
                    elif len(v_string2) > 0:
                        if v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
    
                    i += 1
                    # if i >= 1:
                    #	break

            ##################################################
            # ricerca all'interno della definizione delle viste
            ##################################################
            if not v_abort:
                v_owner = v_db[0:v_db.find('/')]
                v_cursor.execute("SELECT VIEW_NAME FROM ALL_VIEWS WHERE OWNER = " + "'" + v_owner + "'" + " ORDER BY VIEW_NAME")
                for result in v_cursor:
                    if self.progress.wasCanceled():
                        v_abort = True
                        break
                    # nome della tabella
                    v_c_name = result[0]
                    v_c_type = 'VIEW'
                    # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                    v_progress_step += 1
                    self.progress.setValue(v_progress_step);                        
                    v_msg = v_c_type + ' --> ' + v_c_name
                    self.progress_label.setText(v_msg)
                    self.progress.setLabel(self.progress_label)                                                               
                    # preparazione select per la lettura delle colonne e relativi commenti di tabella
                    v_cursor_det.prepare(
                        "SELECT :p_name FROM DUAL UNION SELECT ' ' || A.COLUMN_NAME || ' ' || B.COMMENTS FROM ALL_TAB_COLUMNS A, ALL_COL_COMMENTS B WHERE A.OWNER=:p_owner AND A.TABLE_NAME = :p_name AND A.OWNER=B.OWNER AND A.TABLE_NAME=B.TABLE_NAME AND A.COLUMN_NAME=B.COLUMN_NAME")
                    v_cursor_det.execute(None, {'p_owner': v_owner, 'p_name': v_c_name})
                    # il sorgente finisce dentro la stringa v_sorgente
                    v_sorgente = ''
                    for result in v_cursor_det:
                        v_sorgente = v_sorgente + v_sorgente.join(result)
    
                    v_sorgente = v_sorgente.upper()
                    # utente ha richiesto di ricercare due stringhe in modalita AND
                    if len(v_string1) > 0 and len(v_string2) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0 and v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la prima
                    elif len(v_string1) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la seconda
                    elif len(v_string2) > 0:
                        if v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
    
                    # preparazione select per la lettura del sorgente della vista
                    v_cursor_det.prepare("SELECT TEXT FROM ALL_VIEWS WHERE VIEW_NAME=:p_name")
                    v_cursor_det.execute(None, {'p_name': v_c_name})
                    # il sorgente finisce dentro la stringa v_sorgente
                    v_sorgente = ''
                    for result in v_cursor_det:
                        v_sorgente = v_sorgente + v_sorgente.join(result)
    
                    v_sorgente = v_sorgente.upper()
                    # utente ha richiesto di ricercare due stringhe in modalita AND
                    if len(v_string1) > 0 and len(v_string2) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0 and v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la prima
                    elif len(v_string1) > 0:
                        if v_sorgente.find(v_string1.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                    # utente ha richiesto di ricercare solo una stringa, la seconda
                    elif len(v_string2) > 0:
                        if v_sorgente.find(v_string2.upper()) >= 0:
                            # visualizzo output nell'area di testo
                            self.lista_risultati.appendRow(QtGui.QStandardItem(v_c_type + ' --> ' + v_c_name))
                            f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')

            ###########################################################################################
            # ricerca dentro la UT_LOV (tabella delle liste di valori)...ma solo se connessi al DB SMILE
            ###########################################################################################
            if not v_abort:
                if v_db.upper().find('SMILE') >= 0:
                    try:                    
                        # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                        v_progress_step += 1                    
                        self.progress_label.setText('UT_LOV')
                        self.progress.setLabel(self.progress_label)                                                                   
                        if len(v_string1) > 0 and len(v_string2) > 0:
                            # lettura di UT_LOV
                            v_cursor_det.prepare("""SELECT NAME_CO
                                                    FROM   UT_LOV
                                                    WHERE  (SEL01_CO || SEL02_CO || SEL03_CO || SEL04_CO || SEL05_CO ||
                                                            SEL06_CO || SEL07_CO || SEL08_CO || SEL09_CO || SEL10_CO ||
                                                            FROM_CO  || WHERE_CO || ORDER_CO)
                                                            LIKE '%' || UPPER(:p_string1) || '%' AND
                                                           (SEL01_CO || SEL02_CO || SEL03_CO || SEL04_CO || SEL05_CO ||
                                                            SEL06_CO || SEL07_CO || SEL08_CO || SEL09_CO || SEL10_CO ||
                                                            FROM_CO  || WHERE_CO || ORDER_CO)
                                                            LIKE '%' || UPPER(:p_string2) || '%'
                                                """)
                            v_cursor_det.execute(None, {'p_string1': v_string1, 'p_string2': v_string2})
                            for result in v_cursor_det:
                                v_c_lov_name = result[0]
                                self.lista_risultati.appendRow(QtGui.QStandardItem(' UT_LOV --> ' + v_c_lov_name))
                                f_output.write('UT_LOV;' + v_c_lov_name + '\n')
                        elif len(v_string1) > 0:
                            # lettura di UT_LOV
                            v_cursor_det.prepare("""SELECT NAME_CO
                                                    FROM   UT_LOV
                                                    WHERE  (SEL01_CO || SEL02_CO || SEL03_CO || SEL04_CO || SEL05_CO ||
                                                            SEL06_CO || SEL07_CO || SEL08_CO || SEL09_CO || SEL10_CO ||
                                                            FROM_CO  || WHERE_CO || ORDER_CO)
                                                            LIKE '%' || UPPER(:p_string1) || '%'
                                                """)
                            v_cursor_det.execute(None, {'p_string1': v_string1})
                            for result in v_cursor_det:
                                v_c_lov_name = result[0]
                                self.lista_risultati.appendRow(QtGui.QStandardItem('UT_LOV --> ' + v_c_lov_name))
                                f_output.write('UT_LOV;' + v_c_lov_name + '\n')
                    except:
                        pass
                    
                    ###########################################################################################
                    # ricerca dentro la ALL_SCHEDULER_JOBS (tabella dei job schedulati)
                    ###########################################################################################
                    if v_db.upper().find('SMILE') >= 0:
                        try:
                            # output a video del file in elaborazione (notare incremento del value e impostazione della label)
                            v_progress_step += 1
                            self.progress.setValue(v_progress_step);                                                
                            self.progress_label.setText('ALL_SCHEDULER_JOBS')
                            self.progress.setLabel(self.progress_label)                                                                       
                            if len(v_string1) > 0 and len(v_string2) > 0:
                                # lettura di UT_LOV
                                v_cursor_det.prepare("""SELECT JOB_NAME
                                                        FROM   ALL_SCHEDULER_JOBS
                                                        WHERE  UPPER(JOB_ACTION) LIKE '%' || UPPER(:p_string1) || '%' 
                                                          AND  UPPER(JOB_ACTION) LIKE '%' || UPPER(:p_string2) || '%'
                                                    """)
                                v_cursor_det.execute(None, {'p_string1': v_string1, 'p_string2': v_string2})
                                for result in v_cursor_det:
                                    v_c_lov_name = result[0]
                                    self.lista_risultati.appendRow(QtGui.QStandardItem('ALL_SCHEDULER_JOBS --> ' + v_c_lov_name))
                                    f_output.write('ALL_SCHEDULER_JOBS;' + v_c_lov_name + '\n')
                            elif len(v_string1) > 0:
                                # lettura di UT_LOV                            
                                v_cursor_det.prepare("""SELECT JOB_NAME
                                                        FROM   ALL_SCHEDULER_JOBS
                                                        WHERE  UPPER(JOB_ACTION) LIKE '%' || UPPER(:p_string1) || '%'
                                                    """)
                                v_cursor_det.execute(None, {'p_string1': v_string1})
                                for result in v_cursor_det:
                                    v_c_lov_name = result[0]
                                    self.lista_risultati.appendRow(QtGui.QStandardItem('ALL_SCHEDULER_JOBS --> ' + v_c_lov_name))
                                    f_output.write('ALL_SCHEDULER_JOBS;' + v_c_lov_name + '\n')
                        except:
                            pass                

            # chiusura cursori e connessione DB
            v_cursor_det.close()
            v_cursor.close()
            v_connection.close()
            f_output.close()
            
            return v_abort

    def ricerca_stringa_in_icom(self,
                                v_string1,
                                v_string2,
                                v_output):
        """
            ricerca stringa in sorgenti ICOM-UNIFACE
        """
        v_abort = False
        try:
            v_connection = cx_Oracle.connect('icom_ng_source/icom_ng_source@uniface')
            v_error = False
        except:
            message_error('Connection rejected! Search in ICOM-UNIFACE will skipped!')
            v_error = True

        v_progress_step = 0
        if not v_error:
            # apro il file di output che conterra' i risultati della ricerca
            f_output = open(v_output, 'a')

            # apro cursori
            v_cursor = v_connection.cursor()
            v_cursor_det = v_connection.cursor()
            
            # output a video del file in elaborazione (notare incremento del value e impostazione della label)
            v_progress_step += 1
            self.progress.setValue(v_progress_step);                                        
            self.progress_label.setText('ICOM-UNIFACE')
            self.progress.setLabel(self.progress_label)                                                                       

            # eseguo la ricerca con apposita funzione
            v_cursor.execute('SELECT rep_search_function(:string1,:string2) FROM dual',{'string1' : v_string1 , 'string2' : v_string2})
            for result in v_cursor:
                if result[0] is not None:
                    v_lista  = result[0].split(',')
                    for i in v_lista:
                        # output a video delle ricorrenze trovate
                        self.lista_risultati.appendRow(QtGui.QStandardItem('ICOM source --> ' + i))
                        f_output.write('ICOM source' + ';' + i + ';\n')

            # chiusura cursori e connessione DB
            v_cursor.close()
            v_connection.close()
            f_output.close()
        
        return v_abort
            
    def b_search_slot(self):
        """
            esegue la ricerca delle stringhe
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
        if self.ui.e_stringa1.displayText() == '' and self.ui.e_stringa2.displayText() == '':
            message_error('Please enter string1 or string2 value')
            v_ok = False
        if not self.ui.c_flsearch.isChecked() and not self.ui.c_dbsearch.isChecked():
            message_error('Select execute search in Folder or DB')
            v_ok = False
        if self.ui.c_flsearch.isChecked() and self.ui.e_pathname.displayText() == '':
            message_error('Please enter a pathname')
            v_ok = False
        if self.ui.c_dbsearch.isChecked() and self.ui.e_dboracle1.displayText() == '' and self.ui.e_dboracle2.displayText() == '':
            message_error('Please enter a DB name')
            v_ok = False
        if self.ui.e_outputfile.displayText() == '':
            message_error('Please enter an output file')
            v_ok = False
        # i controlli sono stati superati --> avvio la ricerca
        if v_ok:
            # pulizia dell'item dei risultati            
            self.lista_risultati.clear()            

            # se presente, pulisco il file di output, oppure lo creo. Perché tutte le fasi di ricerca vanno in accodamento
            f_output = open(self.ui.e_outputfile.displayText(), 'w')
            f_output.close()
            
            '''
            questo è stato usato per test        
            self.lista_risultati.appendRow(QtGui.QStandardItem('ciao!'))
            self.lista_risultati.appendRow(QtGui.QStandardItem('come'))
            self.lista_risultati.appendRow(QtGui.QStandardItem('stai?'))            
            self.lista_risultati.index
            '''
            
            # richiama la ricerca nel file system se presente file system            
            if self.ui.c_flsearch.isChecked():
                v_ko = self.ricerca_stringa_in_file(self.ui.e_pathname.displayText(),
                                                    self.ui.e_stringa1.displayText(),
                                                    self.ui.e_stringa2.displayText(),
                                                    self.ui.e_outputfile.displayText(),
                                                    self.ui.e_filter.displayText(),
                                                    self.ui.e_excludepath.displayText())

            # se presente ricerco nei sorgenti DB della connessione1
            if self.ui.c_dbsearch.isChecked() and self.ui.e_dboracle1.displayText() != '' and not v_ko:
                v_ko = self.ricerca_stringa_in_db(self.ui.e_dboracle1.displayText(),
                                                  self.ui.e_stringa1.displayText(),
                                                  self.ui.e_stringa2.displayText(),
                                                  self.ui.e_outputfile.displayText())

            # se presente ricerco nei sorgenti DB della connessione2
            if self.ui.c_dbsearch.isChecked() and self.ui.e_dboracle2.displayText() != '' and not v_ko:
                v_ko = self.ricerca_stringa_in_db(self.ui.e_dboracle2.displayText(),
                                                  self.ui.e_stringa1.displayText(),
                                                  self.ui.e_stringa2.displayText(),
                                                  self.ui.e_outputfile.displayText())

            # eseguo la ricerca nei sorgenti di UNIFACE-ICOM (utente e password di collegamento sono fisse in procedura!)
            if self.ui.c_dbsearch.isChecked() and not v_ko:
                v_ko = self.ricerca_stringa_in_icom(self.ui.e_stringa1.displayText(),
                                                    self.ui.e_stringa2.displayText(),
                                                    self.ui.e_outputfile.displayText())
            
            # chiudo la wait window
            self.progress.close()                    
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = ricerca_stringhe_class()
    application.show()
    sys.exit(app.exec())        