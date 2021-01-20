# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 03/12/2019
 Descrizione...: Programma per la ricerca delle immagini in una pagina web
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file ricerca_elementi_in_pagina_web_ui.py è ricavato partendo da ricerca_elementi_in_pagina_web_ui.ui 
"""

#Librerie sistema
import sys
#Librerie per leggere pagina web
from urllib import request
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from ricerca_elementi_in_pagina_web_ui import Ui_Ricerca_elementi_in_pagina_web_window
#Librerie interne MGrep
from utilita import message_error, message_info
       
class ricerca_elementi_in_pagina_web_class(QtWidgets.QMainWindow, Ui_Ricerca_elementi_in_pagina_web_window):
    """
        Apre una finestra dove richieste l'indirizzo web e ne analizza il contenuto
    """                
    def __init__(self):
        super(ricerca_elementi_in_pagina_web_class, self).__init__()        
        self.setupUi(self)
        
        # creo un oggetto modello che va ad agganciarsi all'oggetto grafico lista
        self.lista_risultati = QtGui.QStandardItemModel()        
        self.o_lst1.setModel(self.lista_risultati)
                        
    def b_search_slot(self):
        """
            esegue la ricerca 
        """        
        if self.e_url.displayText() == '':
            message_error('Please insert a valid URL')
            return None

        # pulizia dell'item dei risultati            
        self.lista_risultati.clear()            

        # legge la pagina web        
        try:
            v_pagina_web=request.urlopen(self.e_url.displayText())
        except:
            message_error('Page not found or unknow error')
            return None
        v_contenuto=str(v_pagina_web.read())
        v_pos=v_contenuto.find('<img alt="')
        v_risultato=[]
        while v_pos > 0:
            v_pos_fin=v_contenuto.find('"',v_pos+10)
            v_risultato.append(v_contenuto[v_pos+10:v_pos_fin])
            v_pos=v_contenuto.find('<img alt="', v_pos+1)

        # carica la lista ordinando i risultati alfabeticamente
        v_risultato_ordinato=sorted(v_risultato)
        for i in range(1,len(v_risultato_ordinato)):
            self.lista_risultati.appendRow(QtGui.QStandardItem(v_risultato_ordinato[i]))                                                    

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = ricerca_elementi_in_pagina_web_class()
    application.show()
    sys.exit(app.exec())        