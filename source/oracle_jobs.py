# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 18/12/2019
 Descrizione...: Programma per interrogare i job di sistema Oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_jobs_ui.py è ricavato partendo da oracle_jobs_ui.ui 
"""

#Librerie sistema
import sys
import os
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_jobs_ui import Ui_oracle_jobs_window
from oracle_jobs_history_ui import Ui_oracle_jobs_history_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info

# classe della storia dei job
class oracle_jobs_history_class(QtWidgets.QMainWindow):
    """
        Oracle job's history. Visualizza lo storico di un job
    """       
    def __init__(self, 
                 p_job_name, 
                 p_oracle_user_sys, 
                 p_oracle_password_sys, 
                 p_server_name):
        
        # incapsulo la classe grafica da qtdesigner
        super(oracle_jobs_history_class, self).__init__()
        self.ui = Ui_oracle_jobs_history_window()
        self.ui.setupUi(self)
        
        # carico i dati
        matrice_dati = self.get_jobs_history(p_job_name, p_oracle_user_sys, p_oracle_password_sys, p_server_name)                        
        
        # lista contenente le intestazioni
        # se si sposta il campo status, ricordarsi di rivedere l'istruzione che cambia il colore
        intestazioni = ['Start date','Run duration','End date','Status','Additional info']                        
        # creo un oggetto modello-matrice che va ad agganciarsi all'oggetto grafico lista        
        self.lista_risultati = QtGui.QStandardItemModel()
        # carico nel modello la lista delle intestazioni
        self.lista_risultati.setHorizontalHeaderLabels(intestazioni)        
        # creo le colonne per contenere i dati
        self.lista_risultati.setColumnCount(len(intestazioni))        
        # creo le righe per contenere i dati
        self.lista_risultati.setRowCount(len(matrice_dati))        
        y =0
        # carico i dati presi dal db dentro il modello
        for row in matrice_dati:            
            x = 0                            
            for field in row:
                q_item = QtGui.QStandardItem()
                q_item.setText( str(field) )
                if x == 3 and field == 'FAILED':                    
                    q_item.setBackground( QtGui.QColor('red') )                    
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        # carico il modello nel widget        
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()
                
    def get_jobs_history(self, p_job_name, p_oracle_user_sys, p_oracle_password_sys, p_server_name):
        """
            Restituisce in una tupla con la storia del job
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=p_oracle_user_sys,
                                             password=p_oracle_password_sys,
                                             dsn=p_server_name,
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []

        # apro cursori
        v_cursor = v_connection.cursor()
            
        # select per la ricerca degli oggetti invalidi
        v_select = """SELECT TO_CHAR(REQ_START_DATE,'DD/MM/YYYY HH24:MI:SS') REQ_START_DATE,
                             TO_CHAR(EXTRACT(HOUR FROM RUN_DURATION), 'FM00') || ':' || TO_CHAR(EXTRACT(MINUTE FROM RUN_DURATION), 'FM00') || ':' || TO_CHAR(EXTRACT(SECOND FROM RUN_DURATION), 'FM00') RUN_DURATION, 
                             LOG_DATE,
                             STATUS,
                             ERRORS
                      FROM   ALL_SCHEDULER_JOB_RUN_DETAILS 
                      WHERE  JOB_NAME='""" + p_job_name + """' 
                      ORDER BY LOG_DATE DESC"""        
                
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]) ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row

# classe principale       
class oracle_jobs_class(QtWidgets.QMainWindow):
    """
        Oracle jobs
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_jobs_class, self).__init__()
        self.ui = Ui_oracle_jobs_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
                                                                
    def get_elenco_jobs(self):
        """
            Restituisce in una tupla elenco dei jobs di sistema
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []

        # apro cursori
        v_cursor = v_connection.cursor()
        
        # eventuale stringa di ricerca per nome o commento del job
        v_where = ''
        if self.ui.e_search1.displayText() != '':
            v_where = " AND (JOB_NAME LIKE '%" + self.ui.e_search1.displayText() + "%' OR COMMENTS LIKE '%" + self.ui.e_search1.displayText() + "')" 
            
        # select per la ricerca degli oggetti invalidi
        v_select = """SELECT JOB_NAME, 
                             COMMENTS,                                
                             JOB_ACTION, 
                             STATE,
                             TO_CHAR(LAST_START_DATE,'DD/MM/YYYY HH24:MI:SS') LAST_START_DATE,
                             TO_CHAR(LAST_START_DATE+LAST_RUN_DURATION,'DD/MM/YYYY HH24:MI:SS') LAST_END_DATE,                                                      
                             to_char(extract(HOUR FROM LAST_RUN_DURATION), 'fm00') || ':' || to_char(extract(MINUTE FROM LAST_RUN_DURATION), 'fm00') || ':' || to_char(extract(SECOND FROM LAST_RUN_DURATION), 'fm00') LAST_RUN_DURATION,      
                             (SELECT STATUS
                              FROM   ALL_SCHEDULER_JOB_RUN_DETAILS 
                              WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME
                                 AND ALL_SCHEDULER_JOB_RUN_DETAILS.LOG_DATE=(SELECT Max(LOG_DATE)
                                                                             FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                                                                             WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME)
                             ) LAST_STATUS,
                             (SELECT ADDITIONAL_INFO
                              FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                              WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME
                                 AND ALL_SCHEDULER_JOB_RUN_DETAILS.LOG_DATE=(SELECT Max(LOG_DATE)
                                                                             FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                                                                             WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME)
                             ) ADDITIONAL_INFO,
                             TO_CHAR(NEXT_RUN_DATE,'DD/MM/YYYY HH24:MI:SS') NEXT_RUN_DATE
                      FROM   ALL_SCHEDULER_JOBS 
                      WHERE  ENABLED='TRUE' """ + v_where.upper() + """
                      ORDER BY JOB_NAME"""        
                
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8]), str(result[9]) ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
                               
    def slot_startSearch(self):            
        """
            Ricerca le sessioni 
        """       
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        matrice_dati = self.get_elenco_jobs()                        
        QtWidgets.QApplication.restoreOverrideCursor()
        
        # lista contenente le intestazioni
        # se si sposta il campo status, ricordarsi di rivedere l'istruzione che cambia il colore
        intestazioni = ['Job name','Comments','Job action','State','Last start date','Last end date','Last run duration','Last status','Additional info','Next run date']                        
        # creo un oggetto modello-matrice che va ad agganciarsi all'oggetto grafico lista        
        self.lista_risultati = QtGui.QStandardItemModel()
        # carico nel modello la lista delle intestazioni
        self.lista_risultati.setHorizontalHeaderLabels(intestazioni)        
        # creo le colonne per contenere i dati
        self.lista_risultati.setColumnCount(len(intestazioni))        
        # creo le righe per contenere i dati
        self.lista_risultati.setRowCount(len(matrice_dati))        
        y =0
        # carico i dati presi dal db dentro il modello
        for row in matrice_dati:            
            x = 0                            
            for field in row:
                q_item = QtGui.QStandardItem()
                q_item.setText( str(field) )
                if x ==3 and field == 'RUNNING':
                    q_item.setBackground( QtGui.QColor('green') ) 
                elif x == 7 and field == 'FAILED':                    
                    q_item.setBackground( QtGui.QColor('red') )                    
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        # carico il modello nel widget        
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()
        
    def slot_jobsHistory(self):
        """
            visualizza la storia del job selezionato
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.ui.o_lst1.currentIndex()                
        # non devo prendere la cella selezionata ma la cella 0 della riga selezionata (quella che contiene il nome del job)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        if v_item_0 != None:            
            v_job_name = v_item_0.text()
            # apro la finestra con lo storico del job
            self.jobs_history = oracle_jobs_history_class( v_job_name, 
                                                           self.o_preferenze.v_oracle_user_sys, 
                                                           self.o_preferenze.v_oracle_password_sys, 
                                                           self.ui.e_server_name.currentText() ) 
            self.jobs_history.show()
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_jobs_class() 
    application.show()
    sys.exit(app.exec())        