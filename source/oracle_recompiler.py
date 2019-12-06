# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 05/12/2019
 Descrizione...: Programma per la ricompilazione oggetti invalidi su DB oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_recompiler_ui.py è ricavato partendo da oracle_recompiler_ui.ui 
"""

#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_recompiler_ui import Ui_oracle_recompiler_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
       
class oracle_recompiler_class(QtWidgets.QMainWindow):
    """
        Oracle recompiler 
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_recompiler_class, self).__init__()
        self.ui = Ui_oracle_recompiler_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
            
    def carica_oggetti_invalidi_db(self):
        """
            carica elenco degli oggetti invalidi
        """
        # connessione al DB come amministratore        
        try:
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)                        
        except:
            message_error('Connection to oracle rejected. Please control login information.')            
            # esco dalla funzione senza nulla
            return [] 
            
        # apro cursori
        v_cursor = v_connection.cursor()
        # select per la ricerca degli oggetti invalidi
        v_cursor.execute("SELECT OWNER, OBJECT_NAME, OBJECT_TYPE  FROM ALL_OBJECTS WHERE STATUS='INVALID' AND OWNER NOT IN ('SYS','APEX_040200') AND OBJECT_NAME NOT LIKE 'OLAP_OLEDB%' ORDER BY OBJECT_TYPE")
        
        # carico tutte le righe in una lista
        v_row = v_cursor.fetchall()            

        v_cursor.close()
        v_connection.close()                       
        
        # restituisco la matrice
        return v_row
                                                
    def slot_b_search_all(self):
        """
            ricerca tutti gli oggetti invalidi
        """
        matrice_dati = self.carica_oggetti_invalidi_db()
        
        # lista contenente le intestazioni
        intestazioni = ['Owner','Object name','Object type']                        
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
                self.lista_risultati.setItem(y, x, QtGui.QStandardItem(field) )
                x += 1
            y += 1
        # carico il modello nel widget        
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()
                                               
    def slot_b_compile_all(self):
        """
            compila tutti gli oggetti invalidi
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)
            v_error = False
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            v_error = True

        if not v_error:
            # apro cursori
            v_cursor = v_connection.cursor()

            # esecuzione dello script che ricompila tutti gli oggetti invalidi
            v_cursor.execute("BEGIN UTL_RECOMP.RECOMP_SERIAL(); END;")
            v_cursor.close()
            v_connection.close()

            # select per la ricerca degli oggetti invalidi
            self.slot_b_search_all()
            
            message_info('Invalid objects recompiled!')
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_recompiler_class() 
    application.show()
    sys.exit(app.exec())        