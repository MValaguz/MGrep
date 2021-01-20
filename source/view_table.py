# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 28/01/2020
 Descrizione...: Scopo del programma è visualizzare il contenuto di una tabella SQLite
"""
#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from view_table_ui import Ui_table_view_window
#Librerie di data base
import sqlite3 
#Import dei moduli interni
from utilita_database import estrae_struttura_tabella_sqlite
from utilita import message_error

class view_table_class(QtWidgets.QMainWindow, Ui_table_view_window):
    """
        Visualizza il contenuto di una tabella SQLite
        Va indicato attraverso l'instanziazione della classe:
            p_table_name     = Nome della tabella SQLite da visualizzare
            p_sqlite_db_name = Nome del DB SQLite            
    """
    def __init__(self,                 
                 p_table_name,
                 p_sqlite_db_name):
        
        # incapsulo la classe grafica da qtdesigner
        super(view_table_class, self).__init__()        
        self.setupUi(self)  
        
        # controllo presenza dei dati in ingresso
        if p_table_name == '' or p_sqlite_db_name == '':
            message_error('Please set table name e SQLite db')
            return None
        
        # indico tramite il cursore del mouse che è in corso un'elaborazione
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))       
        
        ####
        #Apro il DB sqlite    
        ####
        v_sqlite_conn = sqlite3.connect(database=p_sqlite_db_name)
        #Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        #v_sqlite_conn.text_factory = bytes
        v_sqlite_cur = v_sqlite_conn.cursor()                
        #Carico struttura della tabella
        elenco_colonne = estrae_struttura_tabella_sqlite('1', v_sqlite_cur, p_table_name)                         
                                        
        ####
        #Carico la tabella                
        ####
        #Lettura del contenuto della tabella    
        query = estrae_struttura_tabella_sqlite('s', v_sqlite_cur, p_table_name)         
        v_sqlite_cur.execute(query)
        rows = v_sqlite_cur.fetchall()    
        v_sqlite_conn.close()                             
                    
        ###
        # Visualizzo la tabella
        ###
        # creo un oggetto modello-matrice che va ad agganciarsi all'oggetto grafico lista        
        self.lista_risultati = QtGui.QStandardItemModel()
        # carico nel modello la lista delle intestazioni
        self.lista_risultati.setHorizontalHeaderLabels(elenco_colonne)        
        # creo le colonne per contenere i dati
        self.lista_risultati.setColumnCount(len(elenco_colonne))        
        # creo le righe per contenere i dati
        self.lista_risultati.setRowCount(len(rows))        
        y = 0
        # carico i dati presi dal db dentro il modello
        for row in rows:            
            x = 0                            
            for field in row:
                q_item = QtGui.QStandardItem()
                q_item.setText( str(field) )                
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        
        # carico il modello nel widget        
        self.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.o_lst1.resizeColumnsToContents()
        
        # riporto a "normale" l'icona del mouse
        QtWidgets.QApplication.restoreOverrideCursor()        

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = view_table_class('OC_ORTES', 'C:/MGrep/MGrepTransfer.db') 
    application.show()
    sys.exit(app.exec())      