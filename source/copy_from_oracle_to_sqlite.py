# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 23/01/2020
 Descrizione...: Scopo del programma è prendere una tabella di Oracle ed esportarla dentro un 
                 DB SQLite. Se in questa tabella sono presenti dei campi BLOB, il contenuto non viene copiato
                 nel rispettivo campo del DB SQLite (anche perché al massimo può contenere blob di 1mb) ma 
                 direttamente sul PC dell'esecutore del programma. Al posto del contenuto del blob nel DB SQLite
                 ci finirà il nome del file che è stato salvato sul PC per un successivo recupero.
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
from utilita_database import estrae_struttura_tabella_oracle
from utilita_database import estrae_struttura_tabella_sqlite        
from utilita import message_error, message_info, message_question_yes_no

class copy_from_oracle_to_sqlite(QtWidgets.QWidget):
    """
        Esegue la copia di una tabella Oracle dentro medesima tabella di SQLite  
        Va indicato attraverso l'instanziazione della classe:
            p_user_db        = Nome utente del DB Oracle
            p_password_db    = Password utente del DB Oracle
            p_dsn_db         = Indirizzo IP del DB Oracle o dsn
            p_table_name     = Nome della tabella Oracle da copiare
            p_table_where    = Eventuale where da applicare a v_table_name
            p_sqlite_db_name = Nome del DB SQLite, se non esiste verrà creato automaticamente
            p_blob_pathname  = Pathname dove verranno create le cartelle contenenti i blob della tabella copiata
        La tabella create nel db risultante, sarà identica per struttura a quella di partenza anche
        se priva di foreign key, indici, check. Sarà anche priva del contenuto campi blob. In questi
        casi (ed è lo scopo da cui sono partito a creare questa procedura) al posto del contenuto del
        blob ci sarà il nome del file che verrà creato nel file system del PC
    """    
    def __init__(self, 
                 p_user_db,
                 p_password_db,
                 p_dsn_db,
                 p_table_name,
                 p_table_where,
                 p_sqlite_db_name,
                 p_blob_pathname,
                 p_modalita_test):
        
        # rendo la mia classe una superclasse
        super(copy_from_oracle_to_sqlite, self).__init__()                
        
        # completo la pathname 
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
        
        # copia tabella 
        if self.copia_tabella(p_user_db, p_password_db, p_dsn_db, p_table_name, p_table_where, p_sqlite_db_name, p_blob_pathname) == 'ok':
            message_info('Table copy completed!')
                
        self.progress.close()
        self.close()
    
    def copia_tabella(self,
                      v_user_db,
                      v_password_db,
                      v_dsn_db,
                      v_table_name,
                      v_table_where,
                      v_sqlite_db_name,
                      v_blob_pathname): 
                                      
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
        #Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = bytes
        v_sqlite_cur = v_sqlite_conn.cursor()
        
        #Controllo se tabella SQLite esiste già
        v_sqlite_cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE name='" + v_table_name + "'")                                
        #Se la tabella esiste chiedo se posso sovrascrivere
        if v_sqlite_cur.fetchone()[0] > 0:
            if message_question_yes_no("Table in SQLite DB already exist! Do you want overwrite it?") == 'Yes':                            
                #Cancello la tabella se già presente nel db sqlite
                query ='DROP TABLE ' + v_table_name
                v_sqlite_cur.execute(query)    
            else:
                #esco
                return 'ko'
            
        #Conta dei record nella tabella sorgente Oracle
        #Aggiungo la where (solo se caricata)        
        query = 'SELECT COUNT(*) FROM ' + v_table_name        
        if len(v_table_where.split()) > 0:
            query += ' WHERE ' + v_table_where
        try:    
            v_oracle_cursor.execute(query)
        except:
            message_error("Oracle table do not exists or errors in 'where' condition!")
            #esco
            return 'ko'
        
        v_total_rows = 0
        for row in v_oracle_cursor:                  
            v_total_rows = row[0]
        #Calcolo 1% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100

        #Creo la tabella in ambiente di backup (ottengo lo script di create table)
        query = estrae_struttura_tabella_oracle('c', v_oracle_cursor, v_user_db, v_table_name)
        v_sqlite_cur.execute(query)

        #Creo una lista con le posizioni dei campi dove si trovano i blob 
        #In pratica un array dove sono segnati le posizioni dei campi
        #Esempio:
        #CREATE TABLE ta_files (
        #  files_nu NUMBER(8,0)   NOT NULL,
        #  modul_do VARCHAR2(1)   NOT NULL,
        #  files_do VARCHAR2(1)   NOT NULL,
        #  filen_co VARCHAR2(200) NOT NULL,
        #  exten_co VARCHAR2(20)  NULL,
        #  files_fi BLOB          NULL,
        #  ....
        #)
        #La lista conterrà un solo elemento con valore 6 indicante la posizione del campo files_fi
        v_posizioni_blob = estrae_struttura_tabella_oracle('b', v_oracle_cursor, v_user_db, v_table_name)
        v_estensione_blob = estrae_struttura_tabella_oracle('e', v_oracle_cursor, v_user_db, v_table_name)

        #Se nella tabella sono presenti dei blob, creo una cartella nel file system dove ci finiranno i blob
        if v_posizioni_blob:     
            message_info('Table contains blob data! It will be copied in ' + v_blob_pathname + v_table_name)                                
            try: 
                os.mkdir(v_blob_pathname + v_table_name)                
            except:
                message_error('The table contains blob fields! The copy must create the directory ' + v_table_name + ' but this already exists!')                        
                exit()    
            #In questa cartella inserisco un file di testo che riporta le posizioni dei blob. Tale file verrà poi utilizzo nel caso
            #si voglia ricopiare la tabella dentro Oracle
            v_file_allegato = open(v_blob_pathname + v_table_name + '\\blob_fields_position.ini','w')
            v_file_allegato.write(str(v_posizioni_blob))
            v_file_allegato.close()                            
                    
        #Copia dei dati
        query = estrae_struttura_tabella_oracle('s', v_oracle_cursor, v_user_db, v_table_name) 
        #if v_table_where is not None:
        if len(v_table_where.split()) > 0:
            query += ' WHERE ' + v_table_where

        v_insert_base = estrae_struttura_tabella_oracle('i', v_oracle_cursor, v_user_db, v_table_name)         
        v_oracle_cursor.execute(query)        
        v_progress = 0
        v_puntatore_blob = 0
        v_valore_colonna = str()
        for row in v_oracle_cursor:                  
            v_1a_volta = True
            v_insert = v_insert_base            
            for count, column in enumerate(row):                
                if column is None:
                    v_valore_colonna = ''
                else:                
                    v_valore_colonna = column
                    #se la colonna è un blob --> sostituisco il contenuto con quello del puntatore 
                    #e scrivo il contenuto della colonna come file separato in directory a parte
                    if v_posizioni_blob:                
                        if count+1 in v_posizioni_blob:                    
                            v_puntatore_blob += 1                                                
                            v_file_allegato = open(v_blob_pathname + v_table_name + '\\' + str(v_puntatore_blob) + '.zzz','wb')
                            v_file_allegato.write(column.read())
                            v_file_allegato.close()                            
                            v_valore_colonna = str(v_puntatore_blob)                    
                    
                #compongo la insert con il contenuto della colonna (da notare il replace del carattere " con apice singolo!)
                v_valore_colonna = str(v_valore_colonna)                    
                if v_1a_volta:                
                    v_insert += '"' + v_valore_colonna.replace('"',"'") + '"'
                else:
                    v_insert += ',"' + v_valore_colonna.replace('"',"'") + '"'
                    
                v_1a_volta = False
            v_insert += ')'        
            v_sqlite_cur.execute(v_insert)    

            #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
            if v_total_rows > 100:
                v_progress += 1
                if v_progress % v_rif_percent == 0:                                    
                    self.avanza_progress('Total records to copy: ' + str(v_total_rows))
                    #print('Avanzamento scrittura...' + str((v_progress*100//v_total_rows)+1) + '%')                    
        #commit
        v_sqlite_conn.commit()                        
        #chiusura dei cursori
        v_sqlite_conn.close()                    
        v_oracle_cursor.close()   
        
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
    copy_from_oracle_to_sqlite("SMILE",
                               "SMILE",
                               "BACKUP_815",
                               "TA_FILES",
                               "FILEN_CO LIKE '%à%'", 
                               "C:\MGrep\MGrepTransfer.db",
                               "C:\MGrep",
                               True)      