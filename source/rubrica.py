# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 04/12/2019
 Descrizione...: Programma per la ricerca nella rubrica aziendale
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file rubrica_ui.py è ricavato partendo da rubrica_ui.ui 
"""

#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from rubrica_ui import Ui_rubrica_window
#Librerie interne MGrep
from utilita import message_error, message_info
       
class rubrica_class(QtWidgets.QMainWindow):
    """
        Apre una finestra visualizzando la rubrica aziendale
        Va indicato attraverso l'instanziazione della classe:
           tipo_rubrica  = T=Telefonica, E=Email
    """       
    def __init__(self, p_tipo_rubrica):
        # creo variabile interna corrispondente al tipo rubrica
        self.tipo_rubrica = p_tipo_rubrica
        
        # incapsulo la classe grafica da qtdesigner
        super(rubrica_class, self).__init__()
        self.ui = Ui_rubrica_window()
        self.ui.setupUi(self)
        
        # carico e visualizzo il contenuto della tabella                 
        self.slot_b_ricerca()                   
                                            
    def load_rubrica(self):
        """
            restituisce una lista con i risultati della ricerca
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user='SMILE', password='SMILE', dsn='ICOM_815')
        except:
            message_error('Connection to oracle rejected!')
            return 'Error'

        # apro cursori
        v_cursor = v_connection.cursor()

        # select per la ricerca degli oggetti invalidi
        if self.ui.e_ricerca.displayText() != '':
            v_where_ricerca = "AND UPPER(AZIDP_DE || DIPEN_DE || CONTT_CO || REP_DE || EMAIL_DE || MANSIO_DE) LIKE UPPER('%" + self.ui.e_ricerca.displayText().replace(' ','%') + "%')"
        else:
            v_where_ricerca = ''

        # definizione della select (per rubrica telefonica)
        if self.tipo_rubrica == 'T':
            v_cursor.execute("SELECT AZIDP_DE, DIPEN_DE, CONTT_CO, REP_DE, EMAIL_DE, MANSIO_DE FROM VA_RUBRI WHERE CATEG_CO='" +  self.tipo_rubrica + "'" + v_where_ricerca + " ORDER BY AZIDP_DE")
        # o per rubrica email
        else:
            v_cursor.execute("SELECT AZIDP_DE, DIPEN_DE, CONTT_CO, REP_DE,  MANSIO_DE FROM VA_RUBRI WHERE CATEG_CO='" +  self.tipo_rubrica + "'" + v_where_ricerca + " ORDER BY AZIDP_DE")

        # carico tutte le righe in una lista
        v_row = v_cursor.fetchall()

        # chiudo la connessione
        v_cursor.close()
        v_connection.close()

        # restituisco le righe lette
        return v_row    
                                   
    def slot_b_ricerca(self):
        """
            esegue la ricerca 
        """        
        # lista contenente le intestazioni
        if self.tipo_rubrica == "T":
            intestazioni = ['Azienda','Dipendente','Telefono','Reparto','Email','Mansione']
        else:
            intestazioni = ['Azienda','Dipendente','Email','Reparto','Mansione']
                    
        # leggo la tabella da db
        matrice_dati = self.load_rubrica()        
        
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
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    # esempio con rubrica telefonica
    application = rubrica_class('T') 
    application.show()
    sys.exit(app.exec())        