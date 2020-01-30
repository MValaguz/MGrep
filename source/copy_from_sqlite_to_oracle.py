# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 24/01/2020
 Descrizione...: Scopo del programma è prendere una tabella SQLite ed esportarla dentro un DB Oracle. 
"""
#Librerie di data base
import cx_Oracle
import sqlite3 
#Librerie di sistema
import os
import sys
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
#Moduli di progetto
from utilita_database import estrae_struttura_tabella_sqlite        
from utilita import message_error, message_info, message_question_yes_no

class copy_from_sqlite_to_oracle(QtWidgets.QWidget):
    """
        Esegue la copia di una tabella SQLite dentro una tabella Oracle che NON deve esistere
        Va indicato attraverso l'instanziazione della classe:
            p_table_name     = Nome della tabella SQLite da copiare                        
            p_sqlite_db_name = Nome del DB SQLite, se non esiste verrà creato automaticamente
            p_blob_pathname  = Pathname dove verranno pescate le cartelle contenenti i blob della tabella copiata
            p_user_db        = Nome utente del DB Oracle
            p_password_db    = Password utente del DB Oracle
            p_dsn_db         = Indirizzo IP del DB Oracle o dsn
            p_oracle_table   = Nome della tabella Oracle di destinazione (NON deve esistere)             
    """
    def __init__(self,                  
                 p_table_name,                 
                 p_sqlite_db_name,
                 p_blob_pathname,
                 p_user_db,
                 p_password_db,
                 p_dsn_db,
                 p_oracle_table,
                 p_modalita_test):
                
        # rendo la mia classe una superclasse
        super(copy_from_sqlite_to_oracle, self).__init__()                
                
        #Completo la pathname 
        p_blob_pathname = p_blob_pathname + '\\'        
                
                # creazione della wait window
        self.v_progress_step = 0
        self.progress = QtWidgets.QProgressDialog(self)        
        self.progress.setMinimumDuration(0)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Copy...")                
        
        # icona di riferimento
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)        
        self.progress.setWindowIcon(icon)
        
        # imposto valore minimo e massimo a 0 in modo venga considerata una progress a tempo indefinito
        # Attenzione! dentro nel ciclo deve essere usata la funzione setvalue altrimenti non visualizza e non avanza nulla!
        self.progress.setMinimum(0)
        self.progress.setMaximum(100) 
        # creo un campo label che viene impostato con 100 caratteri in modo venga data una dimensione di base standard
        self.progress_label = QtWidgets.QLabel()            
        self.progress_label.setText('.'*100)
        # collego la label già presente nell'oggetto progress bar con la mia label 
        self.progress.setLabel(self.progress_label)                           
        # creo una scritta iniziale...
        self.avanza_progress('Collecting data...')
        
        #Avvio la copia della tabella        
        if self.copia_tabella(p_table_name, p_sqlite_db_name, p_blob_pathname, p_user_db, p_password_db, p_dsn_db, p_oracle_table) == 'ok':
            #Messaggio finale            
            message_info('Table copy completed!')
        
        return None                

    def copia_tabella(self,
                      v_table_name,                      
                      v_sqlite_db_name,
                      v_blob_pathname,
                      v_user_db,
                      v_password_db,
                      v_dsn_db,
                      v_oracle_table): 
                        
        #Controllo se esiste una directory con il nome della tabella e al cui interno sia presente il file di definizione dei blob    
        #Eventualmente preparo una lista con le posizioni dei campi di blob che userò solo dopo aver fatto le insert
        v_posizioni_blob = []
        if os.path.isfile(v_blob_pathname + v_table_name + '\\blob_fields_position.ini'):            
            v_file_blob = open(v_blob_pathname + v_table_name + '\\blob_fields_position.ini')            
            v_linea = v_file_blob.readline()
            v_linea = v_linea.replace(' ','')
            v_linea = v_linea.replace('[','')
            v_linea = v_linea.replace(']','')
            v_posizioni_blob = v_linea.split(',')            
            v_file_blob.close()                
                      
        #Collegamento a Oracle
        try:
            v_oracle_db = cx_Oracle.connect(user=v_user_db, password=v_password_db, dsn=v_dsn_db)        
        except:
            message_error("Connecting problems to Oracle DB!")            
            #esco
            return 'ko'            
        v_oracle_cursor = v_oracle_db.cursor()    
        #Apre il DB sqlite    
        v_sqlite_conn = sqlite3.connect(database=v_sqlite_db_name)
        #Indico al db di funzionare in modalità stringa
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()
        
        #Conto i record della tabella Oracle (se non esiste --> errore)
        try:
            v_oracle_cursor.execute("SELECT COUNT(*) FROM ALL_TABLES WHERE TABLE_NAME='" + v_oracle_table + "'")                        
        except:
            message_error("Table in Oracle DB not exists!")           
            #esco
            return 'ko'
        #Se la tabella esiste errore ed esco
        if v_oracle_cursor.fetchone()[0] > 0:
            message_error("Table in Oracle DB already exist!")           
            #esco
            return 'ko'
            
        #Conto i record della tabella di partenza        
        query = 'SELECT COUNT(*) FROM ' + v_table_name                
        #Aggiungo la where (solo se caricata)        
        try:    
            v_sqlite_cur.execute(query)
        except:
            message_error("SQLite table do not exists!")           
            #esco
            return 'ko'
                
        v_total_rows = 0
        for row in v_sqlite_cur:                  
            v_total_rows = row[0]
        #Calcolo il 10% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100
    
        #Chiedo a db SQLite di restituirmi la struttura della tabella di partenza
        query = estrae_struttura_tabella_sqlite('c', v_sqlite_cur, v_table_name)                             
        #Sostituisco il nome della tabella SQLite con la tabella di arrivo che deve essere creata in Oracle
        query = query.replace(v_table_name,v_oracle_table)        
        #Eseguo la creazione della tabella in DB Oracle
        v_oracle_cursor.execute(query)
        
        ##
        #Inizio copia dei dati
        ##
        
        #Estraggo da db SQLite una struttura "select ..." dalla tabella di partenza
        query = estrae_struttura_tabella_sqlite('s', v_sqlite_cur, v_table_name)                         
        #Estraggo da db SQLite una struttura "insert into nome_tabella(campo1, campo2...) values(:1,:2,....)" dalla tabella di partenza
        v_insert_base = estrae_struttura_tabella_sqlite('h', v_sqlite_cur, v_table_name) 
                
        #Nell'istruzione insert appena ricavata, sostituisco il nome della tabella di partenza con la tabella di arrivo
        v_insert_base = v_insert_base.replace(v_table_name,v_oracle_table)        
        
        #Eseguo la query
        v_sqlite_cur.execute(query)        
        v_progress = 0                
        #Leggo tutte le righe
        for row in v_sqlite_cur:                              
            #Azzero lista che conterrà tutti campi della riga
            v_insert_row = []            
            #Leggo tutte le colonne-campi di una singola riga
            for v_i in range(0,len(row)):                                
                v_blob_caricato = False
                #Se la colonna appartiene a un blob, carico il file corrispondente all'indice
                if len(v_posizioni_blob) > 0:                
                    for v_j in range(0,len(v_posizioni_blob)):
                        if int(v_posizioni_blob[v_j]) == (v_i+1):                            
                            #apro il file
                            v_file_blob = open(v_blob_pathname + v_table_name + '\\' + str(row[v_i]) + '.zzz', 'rb')                                                                                            
                            #leggo il file indicando che deve finire in un blob formato oracle
                            v_blob_value = v_oracle_cursor.var(cx_Oracle.BLOB)                            
                            v_blob_value.setvalue(0,v_file_blob.read())                            
                            #aggiungo il file alla lista delle colonne
                            v_insert_row.append(v_blob_value)                            
                            #elimino il blob come var e chiudo il file
                            del v_blob_value                            
                            v_file_blob.close()                
                            v_blob_caricato = True
                #Carico la colonna normale (tutti i tipi di campi diversi da blob)
                if not v_blob_caricato:
                    v_insert_row.append(row[v_i])                
            
            #Apro di nuovo il cursore (si sono verificati problemi di memoria)
            v_oracle_cursor = v_oracle_db.cursor()    
            #Eseguo la insert dove v_insert_base contiene la parte di testo INSERT INTO ...., mentre v_insert_row contiene i dati dei campi
            v_oracle_cursor.execute(v_insert_base,v_insert_row)                                    
            #Committo
            v_oracle_db.commit()                                
            #Chiudo il cursore 
            v_oracle_cursor.close()    

            #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
            if v_total_rows > 100:
                v_progress += 1
                if v_progress % v_rif_percent == 0:                
                    self.avanza_progress('Total records to copy: ' + str(v_total_rows))                    
                
        #chiusura dei db
        v_sqlite_conn.close()                    
        v_oracle_db.close()        
        return 'ok'
    
    def avanza_progress(self, p_msg):
        """
           Visualizza prossimo avanzamento sulla progress bar
        """
        self.v_progress_step += 1
        if self.v_progress_step <= 100:
            self.progress.setValue(self.v_progress_step);                                        
            self.progress_label.setText(p_msg)        
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    copy_from_sqlite_to_oracle("OC_ORTES",  
                               "C:/MGrep/MGrepTransfer.db",                               
                               "C:\MGrep",
                               "SMILE",
                               "SMILE",
                               "BACKUP_815",
                               "CANCELLAMI_103",
                               True)      
