# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 24/01/2020
 Descrizione...: Scopo del programma è prendere una tabella di SQLite ed esportala in un file Excel
"""
#Librerie di data base
import sqlite3 
#Librerie di sistema
import os
import sys
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
#Libreria per export in excel
from    xlsxwriter.workbook import Workbook
#Import dei moduli interni
from utilita_database import estrae_struttura_tabella_sqlite
from utilita import message_error, message_info, message_question_yes_no

class export_from_sqlite_to_excel(QtWidgets.QWidget):
    """
        Esporta una tabella SQLite in un file Excel
        Va indicato attraverso l'instanziazione della classe:
            p_table_name     = Nome della tabella SQLite da esportare            
            p_sqlite_db_name = Nome del DB SQLite
            p_excel_file     = Nome del file di Excel (il nome deve essere comprensivo di pathname)
    """
    def __init__(self, 
                 p_table_name,                 
                 p_sqlite_db_name,
                 p_excel_file,
                 p_modalita_test):
        
        # rendo la mia classe una superclasse
        super(export_from_sqlite_to_excel, self).__init__()                
                
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
        self.avanza_progress('Record count...', False)
        self.avanza_progress('Record count...', False)
        
        ###############################
        #Avvio la copia della tabella  
        ###############################      
        
        #Apre il DB sqlite (lo apro in modalità classica....non dovrei avere problemi con utf-8)
        v_sqlite_conn = sqlite3.connect(database=p_sqlite_db_name)
        v_sqlite_cur = v_sqlite_conn.cursor()        
                
        #Conta dei record della tabella (serve unicamente per visualizzare la progress bar)
        query = 'SELECT COUNT(*) FROM ' + p_table_name
        try:
            v_sqlite_cur.execute(query)
        except:
            message_error("Table in SQLite DB not exists!")           
            #esco
            return None
        
        v_total_rows = 0
        for row in v_sqlite_cur:                  
            v_total_rows = row[0]
        #Calcolo l' 1% che rappresenta lo spostamento della progress bar        
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100        
                
        #Creazione del file excel
        workbook = Workbook(p_excel_file)
        worksheet = workbook.add_worksheet()
        
        #Estraggo elenco dei campi
        v_struttura = estrae_struttura_tabella_sqlite('1',v_sqlite_cur,p_table_name)
        
        #Carico elenco dei campi nella prima riga del foglio        
        pos = 0
        for i in v_struttura:
            worksheet.write(0, pos, i)
            pos += 1

        #Carico tutte le altre righe della tabella                
        v_progress = 0        
        query = 'SELECT * FROM ' + p_table_name        
        v_sqlite_cur.execute(query)
        for i, row in enumerate(v_sqlite_cur):            
            for j, value in enumerate(row):
                worksheet.write(i+1, j, row[j])        
            #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
            if v_total_rows > 100:
                v_progress += 1
                if v_progress % v_rif_percent == 0:                                    
                    self.avanza_progress( 'Total records to copy: ' + str(v_total_rows), False )                    
                
        #Chiusura del file e del db
        self.avanza_progress('Finalizing process...',True)
        self.avanza_progress('Finalizing process...',True)
        
        workbook.close()
        v_sqlite_conn.close()                    
        #Messaggio finale        
        message_info('Table export completed!')
                
        return None             
    
    def avanza_progress(self, p_msg, p_final):
        """
           Visualizza prossimo avanzamento sulla progress bar
        """        
        if p_final:
            self.v_progress_step += 1
        else:
            if self.v_progress_step < 97:
                self.v_progress_step += 1
                
        self.progress.setValue(self.v_progress_step);                                        
        self.progress_label.setText(p_msg)                
    
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    export_from_sqlite_to_excel("OC_ORTES",                                      
                                "C:\MGrep\MGrepTransfer.db",
                                "C:\MGrep\exportdb.xls",
                                True)      
