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
       
class import_export_class(QtWidgets.QMainWindow):
    """
        Tools import export
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(import_export_class, self).__init__()
        self.ui = Ui_import_export_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_dboracle.addItem(nome)
            
        # carico il resto delle preferenze
        self.ui.e_dboracle.setCurrentText( self.o_preferenze.dboracle )
        self.ui.e_sqlite_db.setText( self.o_preferenze.sqlite_db )
        self.ui.e_where_cond.setText( self.o_preferenze.where_cond )
        self.ui.e_table_name.setCurrentText( self.o_preferenze.table_name )
        self.ui.e_table_excel.setCurrentText( self.o_preferenze.table_excel )
        self.ui.e_excel_file.setText( self.o_preferenze.excel_file )
        self.ui.e_table_to_oracle.setCurrentText( self.o_preferenze.table_to_oracle )
        self.ui.e_import_excel.setText( self.o_preferenze.import_excel )        
        self.ui.e_oracle_table.setCurrentText( self.o_preferenze.oracle_table )
        self.ui.e_csv_file.setText( self.o_preferenze.csv_file )
        self.ui.e_csv_separator.setText( self.o_preferenze.csv_separator )
                    
    def slot_b_sqlite_db(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName[0] = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName != "":
            self.ui.e_sqlite_db.setText( fileName[0] )    
    
    def slot_b_copy_to_sqlite(self):
        pass
    
    def slot_b_view_table(self):
        pass
    
    def slot_b_excel_file(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.ui.e_excel_file.setText( fileName[0] )    
    
    def slot_b_start_excell(self):
        pass
    
    def slot_b_import_excel(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.ui.e_import_excel.setText( fileName[0] )  
    
    def slot_b_copy_to_oracle(self):
        pass
    
    def slot_b_start_import_excel(self):
        pass
    
    def slot_b_csv_file(self):
        """
          selezione del file tramite dialogbox
        """        
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Choose a file")                  
        if fileName[0] != "":
            self.ui.e_csv_file.setText( fileName[0] )  
    
    def slot_b_start_csv_to_excel(self):
        pass
    
    def slot_b_start_clip_to_excel(self):
        pass
    
    def slot_b_save(self):
        """
           Salva le preferenze
        """
        self.o_preferenze.dboracle = self.ui.e_dboracle.currentText()
        self.o_preferenze.sqlite_db = self.ui.e_sqlite_db.text()
        self.o_preferenze.where_cond = self.ui.e_where_cond.text()
        self.o_preferenze.table_name = self.ui.e_table_name.currentText()
        self.o_preferenze.table_excel = self.ui.e_table_excel.currentText()
        self.o_preferenze.excel_file = self.ui.e_excel_file.text()
        self.o_preferenze.table_to_oracle = self.ui.e_table_to_oracle.currentText()
        self.o_preferenze.import_excel = self.ui.e_import_excel.text()
        self.o_preferenze.oracle_table = self.ui.e_oracle_table.currentText()
        self.o_preferenze.csv_file = self.ui.e_csv_file.text()
        self.o_preferenze.csv_separator = self.ui.e_csv_separator.text()
        
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