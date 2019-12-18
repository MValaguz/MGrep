# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 18/12/2019
 Descrizione...: Programma per la ricerca delle sessioni in un database di oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_sessions_ui.py è ricavato partendo da oracle_sessions_ui.ui 
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
from oracle_sessions_ui import Ui_oracle_sessions_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
from utilita_database import killa_sessione
       
class oracle_sessions_class(QtWidgets.QMainWindow):
    """
        Oracle sessions
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_sessions_class, self).__init__()
        self.ui = Ui_oracle_sessions_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
                                                            
    def get_elenco_sessioni(self):
        """
            Restituisce in una tupla elenco delle sessioni 
            considerando eventuali parametri indicati a video (utente, nomepc, ecc.)
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

        v_user = ""

        # ricerca parziale su nome utente
        if self.ui.e_user_name.displayText() != '':
            v_user += " AND Upper(USERNAME) LIKE '%" + self.ui.e_user_name.displayText().upper() + "%' "            
                        
        # ricerca parziale su nome programma
        if self.ui.e_program_name.displayText() != '':
            v_user += " AND Upper(MODULE) LIKE '%" + self.ui.e_program_name.displayText().upper() + "%' "
                                            
        # ricerca parziale su nome terminale
        if self.ui.e_terminal.displayText() != '':
            v_user += " AND Upper(TERMINAL) LIKE '%" + self.ui.e_terminal.displayText().upper() + "%' "
        
        # select per la ricerca degli oggetti invalidi
        v_select = "SELECT SID,       \n\
                           SERIAL#,   \n\
                           TERMINAL,  \n\
                           USERNAME,  \n\
                           DECODE((SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,TERMINAL,NULL,'I','I') FROM DUAL),NULL,(SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,USERNAME,NULL,'I','I') FROM DUAL),(SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,TERMINAL,NULL,'I','I') FROM DUAL)) COGNOME_NOME, \n\
                           STATUS STATO, \n\
                           MODULE PROGRAMMA, \n\
                           PROG_DE DESCRIZIONE, \n\
                           ACTION AZIONE, \n\
                           LOGON_TIME \n\
                    FROM   V$SESSION,(SELECT PROG_CO, PROG_DE FROM ML_PROG WHERE LNG_CO = 'I') ML_PROG \n\
                    WHERE  USERNAME NOT IN ('SYS','SYSTEM','DBSNMP') AND MODULE = PROG_CO(+) \n\
                    " + v_user + "ORDER BY ROWNUM"
        
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( result[0], result[1], str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8]), str(result[9]) ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
                               
    def slot_search_session(self):            
        """
            Ricerca le sessioni 
        """
        matrice_dati = self.get_elenco_sessioni()
        
        # lista contenente le intestazioni
        intestazioni = ['Sid','Serial Nr.','Terminal','Session Name','User Name','Status','Program','Description','Action','Logon time']                        
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
    
    def slot_kill_session(self):
        """
            Killa la sessione selezionata nell'elenco
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.ui.o_lst1.currentIndex()                
        # non devo prendere la cella selezionata ma la cella 0 e 1 della riga selezionata (esse contengono sid e serial nr della sessione)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        v_item_1 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 1) )                        
        v_sid = v_item_0.text()
        v_serial_n = v_item_1.text()                
        if v_sid != None and v_serial_n != None:            
            killa_sessione(v_sid, # colonna 0 della riga
                           v_serial_n, # colonna 1 della riga
                           self.o_preferenze.v_oracle_user_sys,
                           self.o_preferenze.v_oracle_password_sys,
                           self.ui.e_server_name.currentText() )    
                            
    def slot_log_session(self, event):
        """
            crea un file riportante le informazioni di sessione (al momento i cursori aperti)
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.ui.o_lst1.currentIndex()                
        # non devo prendere la cella selezionata ma la cella 0 e 1 della riga selezionata (esse contengono sid e serial nr della sessione)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        v_item_1 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 1) )                        
        v_sid = v_item_0.text()
        v_serial_n = v_item_1.text()                
        
        # apro il file dei risultati
        v_file_name = os.path.join(self.o_preferenze.work_dir, 'session_information.sql')
        v_file = open( v_file_name, 'w')            
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            

        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return None
                    
        # apro cursore
        v_cursor = v_connection.cursor()            

        # select per la ricerca dei cursori aperti e relativo sql
        v_select = "SELECT sql_text FROM v$sql WHERE hash_value IN (SELECT hash_value FROM v$open_cursor WHERE SID=" + str(v_sid) + ") GROUP BY sql_text"                

        v_cursor.execute(v_select)        
        for result in v_cursor:
            # scrivo i risultati nel file
            v_file.write( result[0] + '\n')

        v_cursor.close()
        v_connection.close()            

        v_file.close()           
        message_info(v_file_name + ' created!')
        
        # apre il file appena creato
        os.startfile(v_file_name)        
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_sessions_class() 
    application.show()
    sys.exit(app.exec())        