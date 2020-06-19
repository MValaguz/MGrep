# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 16/06/2020
 Descrizione...: Programma per interrogare i table space di un DB Oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_table_space_ui.py è ricavato partendo da oracle_table_space_ui.ui 
"""

#Librerie sistema
import sys
import os
import re
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_table_space_ui import Ui_oracle_table_space_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info

# classe principale       
class oracle_table_space_class(QtWidgets.QMainWindow):
    """
        Oracle table space
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_table_space_class, self).__init__()
        self.ui = Ui_oracle_table_space_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        # automaticamente scatterà l'evento sulla lista dei server che richiamerà
        # la funzione slot_changed_server
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
            
        self.v_current_table_space = ''
        self.v_nome_primo_dbfile = ''
        self.v_dbfile_dimension = 0
            
    def get_elenco_table_space(self):
        """
            Restituisce in una tupla elenco dei table space
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
        
        # select table space
        v_select = """SELECT DF.TABLESPACE_NAME "TABLESPACE",
                             ROUND(TU.TOTALUSEDSPACE * 100 / DF.TOTALSPACE) "PERC_USED",
                             DF.TOTALSPACE "TOTAL MB",
                             TOTALUSEDSPACE "USED MB",
                             (DF.TOTALSPACE - TU.TOTALUSEDSPACE) "FREE MB"
                      FROM   (SELECT TABLESPACE_NAME,
                                     ROUND(SUM(BYTES) / 1048576) TOTALSPACE
                              FROM   DBA_DATA_FILES
                              GROUP BY TABLESPACE_NAME) DF,
                             (SELECT ROUND(SUM(BYTES)/(1024*1024)) TOTALUSEDSPACE,
                                     TABLESPACE_NAME
                              FROM   DBA_SEGMENTS
                              GROUP BY TABLESPACE_NAME) TU
                      WHERE DF.TABLESPACE_NAME = TU.TABLESPACE_NAME
                        AND DF.TOTALSPACE <> 0
                      ORDER BY ROUND(TU.TOTALUSEDSPACE * 100 / DF.TOTALSPACE) DESC
                   """        
                
        # carico i dati
        v_cursor.execute(v_select)        
        v_row = v_cursor.fetchall()
        
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
                               
    def slot_changed_server(self):            
        """
            Carica a video elenco dei table space
        """       
        matrice_dati = self.get_elenco_table_space()                        
        
        # lista contenente le intestazioni
        intestazioni = ['Tablespace name','% Used','Total Mbyte','Used Mbyte','Free MByte']                        
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
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()
        
    def get_elenco_dbfile(self, p_tablespace_name):
        """
            Restituisce elenco dbfile in una table in base al tablespace ricevuto in ingresso
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
        
        # select table space
        v_select = """SELECT FILE_NAME,
                             BYTES / (1024 * 1024) SPACES,
                             FILE_ID,
                             AUTOEXTENSIBLE,
                             STATUS
                      FROM  DBA_DATA_FILES WHERE TABLESPACE_NAME='""" + p_tablespace_name + """'
                      ORDER BY FILE_NAME DESC
                   """        
        
        # carico i dati        
        v_cursor.execute(v_select)        
        v_row = v_cursor.fetchall()
        
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row        
    
    def slot_table_space_selected(self):
        """
           Carica elenco dei dbfile collegati al table space selezionato
        """
        # ottengo un oggetto index-qt della riga selezionata
        index = self.ui.o_lst1.currentIndex()                
        # non devo prendere la cella selezionata ma la cella 0 della riga selezionata (quella che contiene il nome del table space)
        v_item_0 = self.lista_risultati.itemFromIndex( index.sibling(index.row(), 0) )                
        if v_item_0 != None:            
            self.v_current_table_space = v_item_0.text()
        
        if self.v_current_table_space != '':
            # carico elenco
            matrice_dati = self.get_elenco_dbfile(self.v_current_table_space)                        
            # lista contenente le intestazioni
            intestazioni = ['Name DBfile','Mbyte','File ID','Autoextensible','Available']                        
            # creo un oggetto modello-matrice che va ad agganciarsi all'oggetto grafico lista        
            self.lista_risultati2 = QtGui.QStandardItemModel()
            # carico nel modello la lista delle intestazioni
            self.lista_risultati2.setHorizontalHeaderLabels(intestazioni)        
            # creo le colonne per contenere i dati
            self.lista_risultati2.setColumnCount(len(intestazioni))        
            # creo le righe per contenere i dati
            self.lista_risultati2.setRowCount(len(matrice_dati))        
            y =0
            # carico i dati presi dal db dentro il modello
            for row in matrice_dati:            
                x = 0                            
                for field in row:
                    # mi salvo il primo nome dbfile dell'elenco..sarà quello che userò per ricavare il prossimo
                    # nome di dbfile e creare lo script
                    if x == 0 and y == 0:
                        self.v_nome_primo_dbfile = str(field) 
                    # mi salvo la dimensione del dbfile
                    if x == 1 and y == 0:
                        self.v_dbfile_dimension = field                         
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
                    self.lista_risultati2.setItem(y, x, q_item )                
                    x += 1
                y += 1
            # carico il modello nel widget        
            self.ui.o_lst2.setModel(self.lista_risultati2)                                   
            # indico di calcolare automaticamente la larghezza delle colonne
            self.ui.o_lst2.resizeColumnsToContents()  
            
    def slot_create_script(self):
        """
           Crea lo script SQL per lanciare la creazione di un nuovo DBFile
        """
        if self.v_nome_primo_dbfile == '':
            return 'ko'
        
        # splitto la stringa come nel seguente esempio ['', 'ora03', 'oradata', 'SMIG', 'tsmile94.dbf']
        v_lista = self.v_nome_primo_dbfile.split('/')
        v_nome_db = v_lista[4]
        v_prefisso = v_nome_db.split('.')[0]
        v_parte_numerica = int(re.search(r'\d+', v_prefisso).group(0))
        v_new_parte_numerica = v_parte_numerica + 1
        v_new_nome_db = v_lista[0]+'/'+v_lista[1]+'/'+v_lista[2]+'/'+v_lista[3]+'/'+v_lista[4].replace(str(v_parte_numerica),str(v_new_parte_numerica))
        # compongo lo script
        v_script = "ALTER TABLESPACE " + self.v_current_table_space + " ADD DATAFILE '" + v_new_nome_db + "' SIZE " + str(self.v_dbfile_dimension) + "M"
        # visualizzo il risultato
        self.ui.e_sql_script.setText(v_script)
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_table_space_class() 
    application.show()
    sys.exit(app.exec())        