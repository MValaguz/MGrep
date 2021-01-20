# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 18/01/2021
 Descrizione...: Programma ricercare in un ambiente Oracle lo spazio occulto occupato dalle tabelle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_table_wasted_ui.py è ricavato partendo da oracle_table_wasted_ui.ui 
"""

#Librerie sistema
import sys
# Libreria per la corretta formattazione dei numeri
import locale
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_table_wasted_ui import Ui_oracle_table_wasted_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info

# classe principale       
class oracle_table_wasted_class(QtWidgets.QMainWindow, Ui_oracle_table_wasted_window):
    """
        Oracle table wasted
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_table_wasted_class, self).__init__()        
        self.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.e_server_name.addItem(nome)
                                                   
    def get_elenco_tabelle(self, p_table_to_search):
        """
            Restituisce elenco dbfile in una table in base al tablespace ricevuto in ingresso
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []

        # apro cursori
        v_cursor = v_connection.cursor()
        
        # select table space
        if p_table_to_search != '':
            v_where = " AND TABLE_NAME LIKE '%' || '" + p_table_to_search.upper() + "' || '%'"
        else:
            v_where = ''
            
        v_select = """SELECT OWNER,
                             TABLE_NAME,
                             ROUND((BLOCKS * 8)/1000,0) "SIZE_MBYTE",
                             ROUND((NUM_ROWS * AVG_ROW_LEN / 1024)/1000, 0) "ACTUAL_DATA_MBYTE",
                            (ROUND((BLOCKS * 8)/1000,0) - ROUND((NUM_ROWS * AVG_ROW_LEN / 1024)/1000, 0)) "WASTED_MBYTE"
                      FROM   DBA_TABLES
                      WHERE (ROUND((BLOCKS * 8)/1000,0) - ROUND((NUM_ROWS * AVG_ROW_LEN / 1024)/1000, 0)) > 0
                        AND OWNER <> 'SYS'
                        """ + v_where + """
                      ORDER BY 5 DESC
                   """        
        
        # carico i dati                
        v_cursor.execute(v_select)        
        v_row = v_cursor.fetchall()
        
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row        
    
    def slot_start_search(self):
        """
           Carica elenco dei dbfile collegati al table space selezionato
        """
        # carico elenco
        matrice_dati = self.get_elenco_tabelle(self.e_search.text())                        
        # lista contenente le intestazioni
        intestazioni = ['Owner','Table name','Total size'+chr(10)+'(MByte)','Used size'+chr(10)+'(MByte)','Wasted size'+chr(10)+'(MByte)']                        
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
                # carico item nella lista a video
                q_item = QtGui.QStandardItem()                
                # imposto il dato. E' stato usato il metodo setData perché in questo modo ho visto che i campi numerici 
                # si riescono poi ad ordinare correttamente.                 
                # Se il campo è numerico --> formatto e allineo a destra               
                if isinstance(field, float) or isinstance(field, int):                    
                    q_item.setData( '{:10.0f}'.format(field), QtCore.Qt.EditRole )                           
                    q_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                # altrimenti formatto automaticamente (EditRole) e allineo a sinistra
                else:
                    q_item.setData( field, QtCore.Qt.EditRole )                           
                    q_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)                    
                # carico l'item nella matrice-modello    
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        # carico il modello nel widget        
        self.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.o_lst1.resizeColumnsToContents()  
        
        # carico il totale dello spazio occulto occupato dalle tabelle in elenco
        v_totale = 0
        for row in matrice_dati:            
            # row[4] è la colonna che contiene il valore di spazio occulto
            v_totale += row[4]
        if v_totale > 0:            
            self.l_total_space_wasted2.setText( locale.format_string('%.2f', v_totale/1000, grouping=True) )
        else:
            self.l_total_space_wasted2.setText('...')
            
    def slot_create_script(self):
        """
           Crea lo script SQL per lanciare la creazione di un nuovo DBFile
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.o_lst1.currentIndex()                
        # non devo prendere la cella selezionata ma le celle 0 e 1 della riga selezionata (quella che contiene il nome dello schema e della tabella)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        v_item_1 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 1) )                
        if v_item_0 != None:            
            v_schema = v_item_0.text()        
            v_tabella = v_item_1.text()                    
            v_script = 'ALTER TABLE ' + v_schema + '.' + v_tabella + ' MOVE'
            
            try:
                # connessione al DB come amministratore
                v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                                 password=self.o_preferenze.v_oracle_password_sys,
                                                 dsn=self.e_server_name.currentText(),
                                                 mode=cx_Oracle.SYSDBA)            
            except:
                message_error('Connection to oracle rejected. Please control login information.')
                return []
    
            # apro cursori
            v_cursor = v_connection.cursor()
            
            # select table space
            v_select = """SELECT INDEX_NAME, TABLESPACE_NAME 
                          FROM   DBA_INDEXES 
                          WHERE  OWNER = '""" + v_schema + """'
                            AND  TABLE_NAME= '""" + v_tabella + """'
                            AND  INDEX_TYPE='NORMAL' 
                          ORDER BY INDEX_NAME
                       """        
            
            # carico i dati              
            v_cursor.execute(v_select)        
            v_rows = v_cursor.fetchall()
            
            # chiudo sessione
            v_cursor.close()
            v_connection.close()
            
            # compongo il resto dello script con il nome degli indici
            for v_row in v_rows:
                v_script = v_script + chr(10) + '/' + chr(10) + 'ALTER INDEX ' + v_schema + '.' + v_row[0] + ' REBUILD'
                        
            self.e_sql_script.setText(v_script)                        
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_table_wasted_class() 
    application.show()
    sys.exit(app.exec())        