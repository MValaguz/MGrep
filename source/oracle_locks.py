# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 05/12/2019
 Descrizione...: Programma per la ricerca delle sessioni in blocco in un database Oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_locks_ui.py è ricavato partendo da oracle_locks_ui.ui 
"""

#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_locks_ui import Ui_oracle_locks_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
from utilita_database import estrae_elenco_tabelle_oracle
from utilita_database import killa_sessione
       
class oracle_locks_class(QtWidgets.QMainWindow):
    """
        Oracle locks
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_locks_class, self).__init__()
        self.ui = Ui_oracle_locks_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
                                                            
    def get_elenco_sessioni_bloccate(self):
        """
            Restituisce in una tupla elenco delle sessioni bloccate
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

        # select per la ricerca degli oggetti bloccati
        v_select = "WITH sessions AS \n\
                    (SELECT sid, serial#, blocking_session, P2, row_wait_obj#, sql_id, username,terminal,program \n\
                     FROM v$session) \n\
                     SELECT DECODE(LEVEL,1,'', LPAD(' ', LEVEL*2)) || sid sid,  serial#, username,terminal,program, object_name \n\
                     FROM (SELECT sid, serial#, blocking_session, P2, row_wait_obj#, sql_id, username,terminal,program \n\
                           FROM v$session) s \n\
                     LEFT OUTER JOIN dba_objects \n\
                     ON (object_id = row_wait_obj#) \n\
                     WHERE sid IN (SELECT blocking_session FROM sessions) \n\
                     OR blocking_session IS NOT NULL \n\
                    CONNECT BY PRIOR sid = blocking_session \n\
                    START WITH blocking_session IS NULL"
        
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # ricerco il posizionamento del PC in termini di locazione e referente
            v_location = ''
            v_referent = ''
            v_phone    = ''
            v_ricerca_sql = v_connection.cursor()
            # campo di ricerca (nome pc o nome utente)
            if str(result[3]) == '':
                v_utente = str(result[2])
            else:
                v_utente = str(result[3])

            v_ricerca_sql.execute("""SELECT HW_DISPO.NOME_DE, 
                                          HW_DISPO.DISLO_DE,  
                                          CP_DIPEN.DIPEN_DE,  
                                          VA_RUBRICA.TELIN_NU   
                                   FROM   SMILE.HW_DISPO,     
                                          SMILE.MA_CESPH,     
                                          SMILE.CP_DIPEN,     
                                          SMILE.VA_RUBRICA    
                                   WHERE  UPPER(HW_DISPO.NOME_DE) LIKE '%""" + v_utente + """%'  AND 
                                          MA_CESPH.AZIEN_CO = HW_DISPO.AZIEN_CO AND 
                                          MA_CESPH.MATRI_CO = HW_DISPO.MATRI_CO AND  
                                          MA_CESPH.UTAZI_CO = CP_DIPEN.AZIEN_CO AND  
                                          MA_CESPH.UTMAT_CO = CP_DIPEN.DIPEN_CO AND  
                                          VA_RUBRICA.AZIEN_CO = CP_DIPEN.AZIEN_CO AND 
                                          VA_RUBRICA.DIPEN_CO = CP_DIPEN.DIPEN_CO""")
            
            for campi in v_ricerca_sql:
                if v_location == '':
                    v_location = campi[1]
                if v_referent == '':
                    v_referent = campi[2]
                if v_phone == '':
                    v_phone    = campi[3]
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(v_referent), str(v_phone), str(v_location), str(result[4]), str(result[5]) ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
                               
    def slot_search_session_lock(self):            
        """
            ricerca le sessioni bloccate
        """
        matrice_dati = self.get_elenco_sessioni_bloccate()
        
        # lista contenente le intestazioni
        intestazioni = ['Sid','Serial Nr.','Username','Terminal','Referent','Phone','Location','Program','Object Name']                        
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
    
    def slot_kill_session_lock(self):
        """
            killa la sessione selezionata nell'elenco dei blocchi di sessione
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
    
    def slot_load_table_list(self):
        """
            Carica la combobox delle tabelle di oracle SMILE
        """        
        self.ui.e_table_name.clear()
        elenco_tabelle = estrae_elenco_tabelle_oracle( '1','SMILE','SMILE',self.ui.e_server_name.currentText() ) 
        # carico elenco dei server prendendolo dalle preferenze
        for tabella in elenco_tabelle:            
            self.ui.e_table_name.addItem(tabella)                
            
    def get_elenco_tabelle_bloccate(self):
        """
            Restituisce in una tupla elenco delle sessioni bloccate
        """                
        if self.ui.e_table_name.currentText() == '':
            message_error('Please insert a Oracle table name')           
            return []
        
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []
        
        v_row = []
        # apro cursori
        v_cursor = v_connection.cursor()

        # select per la ricerca degli oggetti invalidi
        v_select = """SELECT v$lock.SID  SID, 
                             v$session.SERIAL# SERIAL_NUMBER, 
                             V$SESSION.USERNAME USERNAME,
                             V$SESSION.STATUS STATUS, 
                             V$SESSION.OSUSER OSUSER, 
                             V$SESSION.MACHINE MACHINE,
                             V$SESSION.PROGRAM||'.'||V$SESSION.MODULE PROGRAM
                    FROM v$lock, v$session
                    WHERE id1 = (SELECT object_id
                                 FROM   all_objects
                                 WHERE  owner ='SMILE' AND
                                        object_name = RTRIM(LTRIM(UPPER('""" + self.ui.e_table_name.currentText() + """')))) AND 
                          v$lock.sid=v$session.sid"""
        v_cursor.execute(v_select)
        
        # carico tutte le righe in una lista
        v_row = v_cursor.fetchall()

        # chiudo connessione e restituisco la tupla
        v_cursor.close()
        v_connection.close()                
        
        return v_row
    
    def slot_search_table_lock(self):
        """
            Visualizza le sessioni che bloccano una specifica tabella sul server ICOM_815
        """
        matrice_dati = self.get_elenco_tabelle_bloccate()
                
        # lista contenente le intestazioni
        intestazioni = ['Sid','Serial Nr.','Username','Status','Os User','Machine','Program']                        
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
        self.ui.o_lst2.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst2.resizeColumnsToContents()                
    
    def slot_kill_table_lock(self):
        """
            killa la sessione selezionata nell'elenco dei blocchi di tabella
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.ui.o_lst2.currentIndex()                
        # non devo prendere la cella selezionata ma la cella 0 e 1 della riga selezionata (esse contengono sid e serial nr della sessione)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        v_item_1 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 1) )                                
        v_sid = v_item_0.text()
        v_serial_n = v_item_1.text()                                    
        if v_sid != '' and v_serial_n != '':                        
            killa_sessione(v_sid, # colonna 0 della riga
                           v_serial_n, # colonna 1 della riga
                           self.o_preferenze.v_oracle_user_sys,
                           self.o_preferenze.v_oracle_password_sys,
                           self.ui.e_server_name.currentText() )    
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_locks_class() 
    application.show()
    sys.exit(app.exec())        