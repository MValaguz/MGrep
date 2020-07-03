# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 25/06/2020
 Descrizione...: Mini programma che simula in parte il funzionamento di sql tools
                  
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_my_sql_ui.py è ricavato partendo da oracle_my_sql_ui.ui 
"""

#Librerie sistema
import sys
import os
import datetime
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_my_sql_ui import Ui_oracle_my_sql_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
from utilita_database import nomi_colonne_istruzione_sql

# classe principale       
class oracle_my_sql_class(QtWidgets.QMainWindow):
    """
        Oracle My Sql
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_my_sql_class, self).__init__()
        self.ui = Ui_oracle_my_sql_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze 
        # Attenzione! Verrà richiamato in automatico l'evento di connessione a oracle
        self.v_connesso = False
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
            
        # sql di prova
        #self.ui.e_sql.setText("SELECT * FROM CP_DIPEN WHERE AZIEN_CO='TEC'")
        self.ui.e_sql.setText("SELECT * FROM TA_AZIEN")
        
        self.ui.o_table.itemChanged.connect(self.log_change)
        
    def log_change(self, item):
        print(item)
                                        
    def slot_connect(self):
        """
           Esegue connessione a Oracle
        """
        try:
            # chiudo eventuale connessione già aperta 
            if self.v_connesso:
                self.v_cursor.close()
            # connessione al DB come smile
            self.v_connection = cx_Oracle.connect(user='SMILE', password='SMILE', dsn=self.ui.e_server_name.currentText())            
            # apro cursore
            self.v_cursor = self.v_connection.cursor()                
            # imposto var che indica la connesione a oracle
            self.v_connesso = True
        except:
            message_error('Error to oracle connection!')                                             
        
    def slot_load(self):
        """
           Carica un file sql
        """
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a sql file", "", "Sql (*.sql)")                  
        if fileName[0] != "":
            try:             
                v_file = open(fileName[0],'r')
                self.ui.e_sql.clear()
                self.ui.e_sql.setText( v_file.read() )            
            except:
                message_error('Error to opened the file')
        
    def slot_save(self):
        """
           Salva un file sql
        """
        
    def slot_execute(self):
        """
           Esegue statement sql
        """
        if self.v_connesso:
            self.ui.o_table.clear()
            # sostituisce la freccia del mouse con icona "clessidra"
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
            
            # esecuzione dell'sql contenuto nel campo a video
            self.v_cursor.execute( self.ui.e_sql.toPlainText() )            
            # lista contenente le intestazioni (tramite apposita funzione si ricavano i nomi delle colonne dall'sql che si intende eseguire)
            intestazioni = nomi_colonne_istruzione_sql(self.v_cursor)                        
            # carico i dati in una matrice e identifico il numero di righe e di colonne della tabella
            matrice_dati = self.v_cursor.fetchall()
            self.ui.o_table.setColumnCount(len(intestazioni))            
            self.ui.o_table.setRowCount(len(matrice_dati))                        
            # setto le intestazioni....va fatta dopo che sono state indicate le righe e colonne altrimenti non funziona
            self.ui.o_table.setHorizontalHeaderLabels(intestazioni)
            y =0
            # carico i dati presi dal db dentro il modello
            for row in matrice_dati:            
                x = 0                            
                for field in row:                                        
                    # campo numerico (se non funziona provare con i cx_Oracle type
                    if isinstance(field, float) or isinstance(field, int):                           
                        self.ui.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( '{:10.0f}'.format(field) ) )
                    # campo nullo
                    elif field == None:                                                
                        self.ui.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( "" ) )                
                    # se il contenuto è un clob...utilizzo il metodo read sul campo field, poi lo inserisco in una immagine
                    # che poi carico una label e finisce dentro la cella a video
                    elif self.v_cursor.description[x][1] == cx_Oracle.BLOB:                                                                            
                        qimg = QtGui.QImage.fromData(field.read())
                        pixmap = QtGui.QPixmap.fromImage(qimg)   
                        label = QtWidgets.QLabel()
                        label.setPixmap(pixmap)                        
                        self.ui.o_table.setCellWidget(y, x, label )                
                    # campo data
                    elif self.v_cursor.description[x][1] == cx_Oracle.DATETIME:                                                                            
                        self.ui.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( str(field) ) )       
                    # campo stringa
                    else:                                                 
                        self.ui.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( field ) )                
                    x += 1
                y += 1
            # indico di calcolare automaticamente la larghezza delle colonne
            self.ui.o_table.resizeColumnsToContents()
            
            QtWidgets.QApplication.restoreOverrideCursor()                        
        
    def slot_commit(self):
        """
           Salva eventuali modifiche di tabella
        """

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_my_sql_class() 
    application.show()
    sys.exit(app.exec())   