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
from test_app import Test_App
from utilita import pathname_icons, message_error
       
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
                wx.MessageBox(text='Connection to oracle rejected. Please control login information.', caption = 'Error', style = wx.OK | wx.ICON_ERROR)
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
                wx.MessageBox(text='Connection to oracle rejected. Please control login information.', caption = 'Error', style = wx.OK | wx.ICON_ERROR)
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
                wx.MessageBox(text='File not found or problem during open application!', caption = 'Error', style = wx.OK | wx.ICON_ERROR)

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

        # lista dei files contenuti nella directory (os.walk restituisce le tuple di tutte le directory partendo dal punto di root)
        for root, dirs, files in os.walk(v_root_node):
            # fermo il loop se richiesto da utente
            if not self.continua:
                break
            # elimino dall'albero delle dir quelle che vanno escluse!
            # Se la stessa dir fosse presente anche ai livelli successivi, viene eliminata anche da li
            for i in range(0, len(v_exclude_ricerca)):
                if v_exclude_ricerca[i] in dirs:
                    dirs.remove(v_exclude_ricerca[i])
            # scorro le tuple dei nomi dentro tupla dei files
            for name in files:
                # fermo il loop se richiesto da utente
                if not self.continua:
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
                        # output a video del file in elaborazione                        
                        (self.continua, keep) = self.wait_win.Pulse(v_file_name[0:50]+chr(13)+v_file_name[51:100])
                        # Lettura di tutto il file  
                        try:
                            f_contenuto = f_input.read().upper()
                        except MemoryError:
                            wx.MessageBox( message='File ' + v_file_name + ' is too big! It was skipped!', caption='Warning', style=wx.OK|wx.ICON_INFORMATION )
                            
                        # utente ha richiesto di ricercare due stringhe in modalita AND
                        if len(v_string1) > 0 and len(v_string2) > 0:
                            if f_contenuto.find(bytes(v_string1.upper(), encoding='latin-1')) >= 0 and f_contenuto.find(
                                    bytes(v_string2.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.o_lst1.Append(v_file_name)
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # utente ha richiesto di ricercare solo una stringa, la prima
                        elif len(v_string1) > 0:
                            if f_contenuto.find(bytes(v_string1.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.o_lst1.Append(v_file_name)
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # utente ha richiesto di ricercare solo una stringa, la seconda
                        elif len(v_string2) > 0:
                            if f_contenuto.find(bytes(v_string2.upper(), encoding='latin-1')) >= 0:
                                # visualizzo output nell'area di testo e scrivo il risultato nel file csv
                                self.o_lst1.Append(v_file_name)
                                f_output.write(v_dir + ';' + v_only_file_name + ';' + v_only_file_extension + '\n')
                        # chiudo il file
                        f_input.close()
        f_output.close()

    def ricerca_stringa_in_db(self,
                              v_db,
                              v_string1,
                              v_string2,
                              v_output):
        """
            ricerca stringa in dbase
        """
        try:
            v_connection = cx_Oracle.connect(v_db)
            v_error = False
        except:
            wx.MessageBox(message='Connection to oracle rejected. Search will skipped!', caption='Warning', style=wx.OK | wx.ICON_ERROR)            
            v_error = True

        if not v_error:
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
                if not self.continua:
                    break
                v_c_name = result[0]
                v_c_type = result[1]
                # output a video del file in elaborazione
                v_msg = v_c_type + ' --> ' + v_c_name
                (self.continua, keep) = self.wait_win.Pulse(v_msg[0:50]+chr(13)+v_msg[51:100])
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
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:
                        # print('Stringa1 trovata in %s' % v_file_name)
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:
                        # print('Stringa2 trovata in %s' % v_file_name)
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                i += 1
                # if i > 10:
                #	break

            ####################################################
            # ricerca all'interno della definizione delle tabelle
            ####################################################
            v_owner = v_db[0:v_db.find('/')]
            v_cursor.execute(
                "SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER = " + "'" + v_owner + "'" + " ORDER BY TABLE_NAME")
            i = 0
            for result in v_cursor:
                if not self.continua:
                    break
                # nome della tabella
                v_c_name = result[0]
                v_c_type = 'TABLE'
                # output a video del file in elaborazione
                v_msg = v_c_type + ' --> ' + v_c_name
                (self.continua, keep) = self.wait_win.Pulse(v_msg[0:50]+chr(13)+v_msg[51:100])
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
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')

                i += 1
                # if i >= 1:
                #	break

            ##################################################
            # ricerca all'interno della definizione delle viste
            ##################################################
            v_owner = v_db[0:v_db.find('/')]
            v_cursor.execute("SELECT VIEW_NAME FROM ALL_VIEWS WHERE OWNER = " + "'" + v_owner + "'" + " ORDER BY VIEW_NAME")
            for result in v_cursor:
                if not self.continua:
                    break
                # nome della tabella
                v_c_name = result[0]
                v_c_type = 'VIEW'
                # output a video del file in elaborazione
                v_msg = v_c_type + ' --> ' + v_c_name
                (self.continua, keep) = self.wait_win.Pulse(v_msg[0:50]+chr(13)+v_msg[51:100])
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
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
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
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_c_type + ' --> ' + v_c_name)
                        f_output.write(v_c_type + ';' + v_c_name + ';' + v_db + '\n')

            ###########################################################################################
            # ricerca dentro la UT_LOV (tabella delle liste di valori)...ma solo se connessi al DB SMILE
            ###########################################################################################
            if v_db.upper().find('SMILE') >= 0:
                try:
                    # output a video del file in elaborazione
                    (self.continua, keep) = self.wait_win.Pulse('UT_LOV')
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
                            self.o_lst1.Append(' UT_LOV --> ' + v_c_lov_name)
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
                            self.o_lst1.Append('UT_LOV --> ' + v_c_lov_name)
                            f_output.write('UT_LOV;' + v_c_lov_name + '\n')
                except:
                    pass
                
                ###########################################################################################
                # ricerca dentro la ALL_SCHEDULER_JOBS (tabella dei job schedulati)
                ###########################################################################################
                if v_db.upper().find('SMILE') >= 0:
                    try:
                        # output a video del file in elaborazione
                        (self.continua, keep) = self.wait_win.Pulse('ALL_SCHEDULER_JOBS')
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
                                self.o_lst1.Append('ALL_SCHEDULER_JOBS --> ' + v_c_lov_name)
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
                                self.o_lst1.Append('ALL_SCHEDULER_JOBS --> ' + v_c_lov_name)
                                f_output.write('ALL_SCHEDULER_JOBS;' + v_c_lov_name + '\n')
                    except:
                        pass                

            # chiusura cursori e connessione DB
            v_cursor_det.close()
            v_cursor.close()
            v_connection.close()
            f_output.close()

    def ricerca_stringa_in_icom(self,
                                v_string1,
                                v_string2,
                                v_output):
        """
            ricerca stringa in sorgenti ICOM-UNIFACE
        """
        try:
            v_connection = cx_Oracle.connect('icom_ng_source/icom_ng_source@uniface')
            v_error = False
        except:
            wx.MessageBox(message='Connection rejected! Search in ICOM-UNIFACE will skipped!', caption='Warning', style = wx.OK | wx.ICON_INFORMATION)
            v_error = True

        if not v_error:
            # apro il file di output che conterra' i risultati della ricerca
            f_output = open(v_output, 'a')

            # apro cursori
            v_cursor = v_connection.cursor()
            v_cursor_det = v_connection.cursor()

            # emetto messaggio inizio ricerca icom
            (self.continua, keep) = self.wait_win.Pulse('ICOM-UNIFACE')

            # eseguo la ricerca con apposita funzione
            v_cursor.execute('SELECT rep_search_function(:string1,:string2) FROM dual',{'string1' : v_string1 , 'string2' : v_string2})
            for result in v_cursor:
                if result[0] is not None:
                    v_lista  = result[0].split(',')
                    for i in v_lista:
                        # output a video delle ricorrenze trovate
                        self.o_lst1.Append('ICOM source --> ' + i)
                        f_output.write('ICOM source' + ';' + i + ';\n')

            # chiusura cursori e connessione DB
            v_cursor.close()
            v_connection.close()
            f_output.close()
            
    def ricerca_stringa_in_apex(self,
                                v_db,
                                v_string1,
                                v_string2,
                                v_output):
        """
            ricerca stringa nei sorgenti di Apex. E' importante che sul server Oracle sia stata compilata la funzione EXPORT_APEX_APPLICATION.
			Siccome ci sono stati problemi di conversione caratteri UTF8, si è deciso che quanto restituito dalla funzione EXPORT_APEX_APPLICATION 
			sia tutto in formato ASCII
        """        
        v_connection = cx_Oracle.connect(v_db)
        try:            
            v_connection = cx_Oracle.connect(v_db)
            v_error = False
        except:
            wx.MessageBox(message='Connection to oracle rejected. Search will skipped!', caption='Warning', style=wx.OK | wx.ICON_ERROR)            
            v_error = True

        if not v_error:
            # apro il file di output che conterra' i risultati della ricerca
            f_output = open(v_output, 'a')

            # apro cursori
            v_cursor = v_connection.cursor()
            v_cursor_det = v_connection.cursor()

            ##############################################################
            # ricerca all'interno delle applicazioni Apex
            ##############################################################
            v_cursor.execute("SELECT WORKSPACE_ID, APPLICATION_ID, APPLICATION_NAME FROM APEX_APPLICATIONS WHERE WORKSPACE = 'SMILE' /*AND APPLICATION_ID=167*/ ORDER BY APPLICATION_NAME")
            i = 0
            for result in v_cursor:
                if not self.continua:
                    break
                v_c_type = 'APEX'
                v_workspace_id = result[0]
                v_application_id = result[1]
                v_application_name = result[2]
                # output a video del file in elaborazione
                v_msg = v_c_type + ' --> (' + str(v_application_id) + ') ' + v_application_name
                (self.continua, keep) = self.wait_win.Pulse(v_msg[0:50]+chr(13)+v_msg[51:100])                
                # lettura del sorgente (ci sono stati problemi con il tipo di mappatura dei caratteri e per questo motivo nella funzione di SMILE è stata forzata la conversione da UTF8 a US7ASCII
                v_cursor_det.prepare("SELECT EXPORT_APEX_APPLICATION(:application_id) FROM dual")
                v_cursor_det.execute(None, {'application_id': v_application_id})
                # leggo la prima colonna della lista che viene restituita dal cursore di oracle e che contiene il clob con l'export in formato testuale dell'applicazione Apex                
                v_result = v_cursor_det.var(cx_Oracle.CLOB)   
                v_result = v_cursor_det.fetchone()[0]                                
                # trasformo il clob in una stringa e porto tutti i caratteri a maiuscolo e inoltre elimino tutti i "ritorni a capo" in quanto sembra che Apex vada a capo senza troppi criteri
                v_sorgente = v_result.read()                   
                v_sorgente = v_sorgente.upper()
                v_sorgente = v_sorgente.replace(chr(10),'')
                # utente ha richiesto di ricercare due stringhe in modalita AND
                if len(v_string1) > 0 and len(v_string2) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0 and v_sorgente.find(v_string2.upper()) >= 0:                        
                        # visualizzo output nell'area di testo
                        self.o_lst1.Append(v_msg)
                        f_output.write(v_c_type + ';' + str(v_application_id) + ';' + v_application_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la prima
                elif len(v_string1) > 0:
                    if v_sorgente.find(v_string1.upper()) >= 0:                        
                        self.o_lst1.Append(v_msg)
                        f_output.write(v_c_type + ';' + str(v_application_id) + ';' + v_application_name + ';' + v_db + '\n')
                # utente ha richiesto di ricercare solo una stringa, la seconda
                elif len(v_string2) > 0:
                    if v_sorgente.find(v_string2.upper()) >= 0:                        
                        self.o_lst1.Append(v_msg)
                        f_output.write(v_c_type + ';' + str(v_application_id) + ';' + v_application_name + ';' + v_db + '\n')
                        
            # chiusura cursori e connessione DB
            v_cursor_det.close()
            v_cursor.close()
            v_connection.close()
            f_output.close()            

    def b_search_slot(self):
        """
            esegue la ricerca delle stringhe
        """
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
            # avanzamento progressbar
            self.continua = True
            self.wait_win = wx.ProgressDialog(title='Searching', message='Please wait', maximum=1000, parent=None, style=wx.PD_AUTO_HIDE|wx.PD_CAN_ABORT|wx.PD_ELAPSED_TIME)
            self.wait_win.Show()

            # pulizia dell'item dei risultati
            self.o_lst1.Clear()

            # se presente, pulisco il file di output, oppure lo creo. Perché tutte le fasi di ricerca vanno in accodamento
            f_output = open(self.e_outputfile.GetValue(), 'w')
            f_output.close()

            # richiama la ricerca nel file system se presente file system
            if self.c_flsearch.GetValue():
                self.ricerca_stringa_in_file(self.e_pathname.GetValue(),
                                             self.e_stringa1.GetValue(),
                                             self.e_stringa2.GetValue(),
                                             self.e_outputfile.GetValue(),
                                             self.e_filter.GetValue(),
                                             self.e_excludepath.GetValue())

            # se presente ricerco nei sorgenti DB della connessione1
            if self.c_dbsearch.GetValue() and self.e_dboracle1.GetValue() != '' and self.continua:
                self.ricerca_stringa_in_db(self.e_dboracle1.GetValue(),
                                           self.e_stringa1.GetValue(),
                                           self.e_stringa2.GetValue(),
                                           self.e_outputfile.GetValue())

            # se presente ricerco nei sorgenti DB della connessione2
            if self.c_dbsearch.GetValue() and self.e_dboracle2.GetValue() != '' and self.continua:
                self.ricerca_stringa_in_db(self.e_dboracle2.GetValue(),
                                           self.e_stringa1.GetValue(),
                                           self.e_stringa2.GetValue(),
                                           self.e_outputfile.GetValue())

            # eseguo la ricerca nei sorgenti di UNIFACE-ICOM (utente e password di collegamento sono fisse in procedura!)
            if self.c_dbsearch.GetValue() and self.continua:
                self.ricerca_stringa_in_icom(self.e_stringa1.GetValue(),
                                             self.e_stringa2.GetValue(),
                                             self.e_outputfile.GetValue())
            
            # se presente ricerco nei sorgenti Apex
            if self.c_apexsearch.GetValue() and self.e_dbapex.GetValue() != '' and self.continua:
                self.ricerca_stringa_in_apex(self.e_dbapex.GetValue(),
                                             self.e_stringa1.GetValue(),
                                             self.e_stringa2.GetValue(),
                                             self.e_outputfile.GetValue())
            
            # fermo la progressbar
            self.wait_win.Destroy()
    

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    application = ricerca_stringhe_class()
    application.show()
    sys.exit(app.exec())        