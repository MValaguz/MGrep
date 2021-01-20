# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 13/01/2020
 Descrizione...: Programma che richiama le varie utilità di import-export dei dati
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file import_export_ui.py è ricavato partendo da import_export_ui.ui 
"""

#Librerie sistema
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from import_export_ui import Ui_import_export_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
from copy_from_oracle_to_sqlite import copy_from_oracle_to_sqlite
from export_from_sqlite_to_excel import export_from_sqlite_to_excel
from copy_from_sqlite_to_oracle import copy_from_sqlite_to_oracle
from import_excel_into_oracle import import_excel_into_oracle
from convert_csv_to_excel import convert_csv_to_excel
from convert_csv_to_excel import convert_csv_clipboard_to_excel
from view_table import view_table_class
import utilita_database 
       
class import_export_class(QtWidgets.QMainWindow, Ui_import_export_window):
    """
        Tools import export
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(import_export_class, self).__init__()        
        self.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.e_dboracle.addItem(nome)
            
        # carico elenco degli user (al momento fisso)        
        self.e_oracle_user.addItem('SMILE')        
        self.e_oracle_user.addItem('SMI')        
        
        # carico il resto delle preferenze
        self.e_dboracle.setCurrentText( self.o_preferenze.dboracle )
        self.e_sqlite_db.setText( self.o_preferenze.sqlite_db )
        self.e_where_cond.setText( self.o_preferenze.where_cond )
        self.e_table_name.setCurrentText( self.o_preferenze.table_name )
        self.e_table_excel.setCurrentText( self.o_preferenze.table_excel )
        self.e_excel_file.setText( self.o_preferenze.excel_file )
        self.e_table_to_oracle.setCurrentText( self.o_preferenze.table_to_oracle )
        self.e_import_excel.setText( self.o_preferenze.import_excel )        
        self.e_oracle_table.setCurrentText( self.o_preferenze.oracle_table )
        self.e_csv_file.setText( self.o_preferenze.csv_file )
        self.e_csv_separator.setText( self.o_preferenze.csv_separator )
        
        # carico i valori nelle combobox
        self.carica_i_combo_box()
        
    def slot_b_sqlite_db(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.e_sqlite_db.setText( fileName[0] )    
    
    def slot_b_copy_to_sqlite(self):
        """
            esegue la procedura che copia una tabella di Oracle dentro un DB di SQLite
        """        
        v_ok = True
        if self.e_dboracle.currentText() == '':
            message_error('Please enter a Oracle connection')            
            v_ok = False
        if self.e_sqlite_db.displayText() == '':
            message_error('Please enter a SQLite DB destination')
            v_ok = False
        if self.e_table_name.currentText() == '':
            message_error('Please enter a Table Name')
            v_ok = False

        # Richiamo copia della tabella
        if v_ok:            
            app = copy_from_oracle_to_sqlite(self.e_oracle_user.currentText(),
                                             self.e_oracle_user.currentText(),
                                             self.e_dboracle.currentText(),
                                             self.e_table_name.currentText(),
                                             self.e_where_cond.toPlainText(), 
                                             self.e_sqlite_db.displayText(),
                                             self.o_preferenze.work_dir,
                                             False)    
            # aggiorno i valori delle combobox
            self.carica_i_combo_box()            
    
    def slot_b_view_table(self):
        """
           visualizza il contenuto di una tabella sqlite
        """
        self.my_app = view_table_class( self.e_table_excel.currentText(), self.e_sqlite_db.displayText() )      
        self.my_app.show()
    
    def slot_b_excel_file(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.e_excel_file.setText( fileName[0] )    
    
    def slot_b_start_excel(self):
        """
            esegue la procedura che esporta una tabella SQLite dentro un file di excel
        """
        v_ok = True
        if self.e_sqlite_db.displayText() == '':
            message_error('Please enter a SQLite DB')
            v_ok = False
        if self.e_table_excel.currentText() == '':
            message_error('Please enter a Table Name')
            v_ok = False
        if self.e_excel_file.displayText() == '':
            message_error('Please enter a Destination file')
            v_ok = False

        # Richiamo export della tabella in excel
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            app = export_from_sqlite_to_excel(self.e_table_excel.currentText(),
                                              self.e_sqlite_db.displayText(),
                                              self.e_excel_file.displayText(),
                                              False)        
    
    def slot_b_import_excel(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.e_import_excel.setText( fileName[0] )  
    
    def slot_b_copy_to_oracle(self):
        """
           prende una tabella sqlite e la copia dentro tabella oracle
        """
        app = copy_from_sqlite_to_oracle(self.e_table_to_oracle.currentText(),  
                                         self.e_sqlite_db.displayText(),
                                         self.o_preferenze.work_dir,                               
                                         self.e_oracle_user.currentText(),
                                         self.e_oracle_user.currentText(),
                                         self.e_dboracle.currentText(),
                                         self.e_oracle_table.currentText(),
                                         False)  
        # aggiorno i valori delle combobox
        self.carica_i_combo_box()                    
    
    def slot_b_start_import_excel(self):
        """
           copia un foglio di excel dentro una tabella oracle
        """
        app = import_excel_into_oracle(False,
                                       self.e_oracle_user.currentText(),
                                       self.e_oracle_user.currentText(),
                                       self.e_dboracle.currentText(),
                                       self.e_oracle_table.currentText(),
                                       self.e_import_excel.displayText(),
                                       False)      
        # aggiorno i valori delle combobox
        self.carica_i_combo_box()                    
    
    def slot_b_csv_file(self):
        """
           selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.e_csv_file.setText( fileName[0] )  
    
    def slot_b_start_csv_to_excel(self):
        """
           converte csv in file excel
        """
        app = convert_csv_to_excel(self.e_csv_file.displayText(),
                                   self.e_csv_separator.displayText(),
                                   False)        
    
    def slot_b_start_clip_to_excel(self):
        """
           converte il contenuto della clipboard in excel
        """        
        app = convert_csv_clipboard_to_excel(self.o_preferenze.work_dir,
                                             self.e_csv_separator.displayText(),
                                             False)        
    
    def carica_i_combo_box(self):
        """
           Carica tutti i valori delle combobox. Ho usato questo meccanismo perché non riuscivo ad intercettare il focus sulla combobox.
           Di fatto è possibile personalizzando la classe QComboBox ma avendo QTDesigner di mezzo non riesco a fare questa cosa....
        """
        v_elenco_tabelle_oracle = utilita_database.estrae_elenco_tabelle_oracle( '1', self.e_oracle_user.currentText(), self.e_oracle_user.currentText(), self.e_dboracle.currentText() )
        # carica la combobox tabelle di oracle
        v_valore_corrente = self.e_table_name.currentText()
        self.e_table_name.clear()                
        self.e_table_name.addItems( v_elenco_tabelle_oracle )            
        self.e_table_name.setCurrentText( v_valore_corrente )
        # carica la combobox delle tabelle di oracle SMILE
        v_valore_corrente = self.e_oracle_table.currentText()
        self.e_oracle_table.clear()        
        self.e_oracle_table.addItems( v_elenco_tabelle_oracle )                    
        self.e_oracle_table.setCurrentText( v_valore_corrente )
    
        # carica la combobox tabelle per export in excel
        if self.e_sqlite_db.displayText() != '':
            v_valore_corrente = self.e_table_excel.currentText()
            self.e_table_excel.clear()
            self.e_table_excel.addItems( utilita_database.estrae_elenco_tabelle_sqlite('1', self.e_sqlite_db.displayText()) )
            self.e_table_excel.setCurrentText( v_valore_corrente )

        # carica la combobox tabelle per export in excel
        if self.e_sqlite_db.displayText() != '':
            v_valore_corrente = self.e_table_to_oracle.currentText()
            self.e_table_to_oracle.clear()
            self.e_table_to_oracle.addItems( utilita_database.estrae_elenco_tabelle_sqlite('1', self.e_sqlite_db.displayText()) )    
            self.e_table_to_oracle.setCurrentText( v_valore_corrente )
                           
    def slot_b_save(self):
        """
           Salva le preferenze
        """
        self.o_preferenze.dboracle = self.e_dboracle.currentText()
        self.o_preferenze.sqlite_db = self.e_sqlite_db.text()
        self.o_preferenze.where_cond = self.e_where_cond.toPlainText()
        self.o_preferenze.table_name = self.e_table_name.currentText()
        self.o_preferenze.table_excel = self.e_table_excel.currentText()
        self.o_preferenze.excel_file = self.e_excel_file.text()
        self.o_preferenze.table_to_oracle = self.e_table_to_oracle.currentText()
        self.o_preferenze.import_excel = self.e_import_excel.text()
        self.o_preferenze.oracle_table = self.e_oracle_table.currentText()
        self.o_preferenze.csv_file = self.e_csv_file.text()
        self.o_preferenze.csv_separator = self.e_csv_separator.text()
        
        self.o_preferenze.salva()
                
        message_info('Preferences was saved')
                                                                    
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = import_export_class() 
    application.show()
    sys.exit(app.exec())        