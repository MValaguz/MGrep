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
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
import resource_rc

class my_wait_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setWindowModality(QtCore.Qt.ApplicationModal)
        #Form.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        #Form.setWindowFlag(QtCore.Qt.CustomizeWindowHint)
        Form.resize(246, 77)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "..."))
        self.label.setText(_translate("Form", "......wait a moment please......"))
       
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
            
    def wait_window(self, p_stato):
        """
           Apre una finestra di wait
        """       
        if p_stato:
            self.primo = QtWidgets.QWidget()
            self.secondo = my_wait_window()
            self.secondo.setupUi(self.primo)
            self.primo.show()        
        else:
            self.primo.close()
        """
        if p_stato:
            # creazione della wait window
            self.v_progress_step = 0
            self.progress = QtWidgets.QProgressDialog(self)        
            self.progress.setMinimumDuration(0)
            self.progress.setWindowModality(QtCore.Qt.WindowModal)
            self.progress.setWindowTitle("Wait window")                
            self.progress.setCancelButton(None)
            
            # imposto valore minimo e massimo a 0 in modo venga considerata una progress a tempo indefinito
            # Attenzione! dentro nel ciclo deve essere usata la funzione setvalue altrimenti non visualizza e non avanza nulla!
            self.progress.setMinimum(0)
            self.progress.setMaximum(101)             
            # creo un campo label che viene impostato con 100 caratteri in modo venga data una dimensione di base standard
            self.progress_label = QtWidgets.QLabel()            
            self.progress_label.setText('.....wait a moment please......')
            # collego la label già presente nell'oggetto progress bar con la mia label 
            self.progress.setLabel(self.progress_label)
            # imposto %100
            self.v_progress_step = 1
            self.progress.setValue(self.v_progress_step);                                                    
            self.v_progress_step = 100
            self.progress.setValue(self.v_progress_step);                                                                
        else:
            self.progress.close()
        """
                                                    
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

        # select per la ricerca degli oggetti invalidi
        v_select = """SELECT JOB_NAME, 
                             COMMENTS,                                
                             JOB_ACTION, 
                             TO_CHAR(LAST_START_DATE,'DD/MM/YYYY HH24:MI:SS') LAST_START_DATE,
                             TO_CHAR(NEXT_RUN_DATE,'DD/MM/YYYY HH24:MI:SS') NEXT_RUN_DATE, 
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
                             ) ADDITIONAL_INFO
                      FROM   ALL_SCHEDULER_JOBS 
                      WHERE  ENABLED='TRUE'
                      ORDER BY JOB_NAME"""        
                
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]) ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
                               
    def slot_startSearch(self):            
        """
            Ricerca le sessioni 
        """        
        self.wait_window(True)
        matrice_dati = self.get_elenco_jobs()                        
        #self.wait_window(False)
        
        # lista contenente le intestazioni
        intestazioni = ['Job name','Comments','Job action','Last start date','Next run date','Last status','Additional info']                        
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
                self.lista_risultati.setItem(y, x, QtGui.QStandardItem(str(field)) )
                x += 1
            y += 1
        # carico il modello nel widget        
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_jobs_class() 
    application.show()
    sys.exit(app.exec())        