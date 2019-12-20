# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 20/12/2019
 Descrizione...: Dato un testo, lo converte in big text
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file ascii_graphics.py è ricavato partendo da ascii_graphics_ui.ui 
"""

#Librerie sistema
import sys
import os
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from ascii_graphics_ui import Ui_ascii_graphics_window
#Librerie per convertire caratteri ascii in big text
import pyfiglet 
#Librerie interne MGrep
from utilita import message_error, message_info
from utilita import file_in_directory
       
class ascii_graphics_class(QtWidgets.QMainWindow):
    """
        Dato un testo, lo converte in big text
    """                
    def __init__(self):
        super(ascii_graphics_class, self).__init__()
        self.ui = Ui_ascii_graphics_window()
        self.ui.setupUi(self)
        
        v_lista_fonts = self.carica_lista_fonts()
        for font in v_lista_fonts:
            self.ui.e_fonts_list.addItem(font)                   
        
    def carica_lista_fonts(self):
        '''
           Carica la listbox con elenco dei fonts (in pratica i files contenuti nella directory fonts)
           Ci sono due modalità di esecuzione. Una quando il programma è in fase di sviluppo per cui la directory fonts è annegate dentro le dir di sistema 
           e una modalità quando viene "compilato" dove la dir fonts è sotto la tabella pyfiglet. Per entrambe le situazioni il costrutto __file__ sembra andare bene!!
        '''         
        v_pyfiglet_fonts_dir = pyfiglet.__file__
        v_pyfiglet_fonts_dir = os.path.dirname(v_pyfiglet_fonts_dir)
        v_root_node = v_pyfiglet_fonts_dir + '\\fonts'        
        v_elenco_file = file_in_directory(v_root_node)
        v_lista_finale = []
        # inserisco un primo elemento vuoto
        v_lista_finale.append('')
        #v_lista_finale.append(v_root_node) questa è una riga utile per eventuale debug in quanto inserisce come primo elemento il nome della cartella dove va a cercare i font
        for nome_file in v_elenco_file:
            # filtro l'elenco dei file prendendo solo quelli con il suffisso .flf che sono quelli dei font disponibili
            if nome_file.find('.flf')>0:                
                # estrae solo il nome del file dalla stringa
                v_solo_nome_file = os.path.basename(nome_file)                
                # nella lista aggiunge solo la parte del nome senza il suffisso                
                v_lista_finale.append(os.path.splitext(v_solo_nome_file)[0])
        return v_lista_finale    
        
    def slot_converte(self):
        ''' 
           Esegue la conversione del testo semplice in testo graphics ascii
        '''
        if self.ui.e_converte.displayText() == '':
            message_error('Please insert a text')
            return None
        # il risultato viene impostato con il font richiesto (da non confondersi con il font con cui viene visualizzato)
        if self.ui.e_fonts_list.currentText() != '':
            risultato = pyfiglet.figlet_format( self.ui.e_converte.displayText(), font=self.ui.e_fonts_list.currentText() )         
        # se però non è stato indicato alcun fonts, lascio il default
        else:
            risultato = pyfiglet.figlet_format( self.ui.e_converte.displayText() )         
        # imposto il risultato nella textbox
        self.ui.e_risultato.clear()
        self.ui.e_risultato.append(risultato)

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = ascii_graphics_class()
    application.show()
    sys.exit(app.exec())        