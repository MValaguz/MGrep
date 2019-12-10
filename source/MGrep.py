# -*- coding: utf-8 -*-

"""
 __  __  ____                
|  \/  |/ ___|_ __ ___ _ __  
| |\/| | |  _| '__/ _ \ '_ \ 
| |  | | |_| | | |  __/ |_) |
|_|  |_|\____|_|  \___| .__/ 
                      |_|    

 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 18/11/2019
 Descrizione...: Main del programma MGrep
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file MGrep_ui.py è ricavato partendo da MGrep_ui.ui 
"""

#Librerie sistema
import os
import sys
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from MGrep_ui import Ui_MGrepWindow
#Librerie interne 
from preferenze import preferenze
from utilita import message_error, message_info, message_question_yes_no
       
class MGrep_class(QtWidgets.QMainWindow):
    """
       Programma per la ricerca delle stringhe all'interno dei sorgenti di Oracle forms
    """                
    def __init__(self):
        super(MGrep_class, self).__init__()
        self.ui = Ui_MGrepWindow()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()
    
        # se dalle preferenze emerge che vanno aperte delle window in una certa posizione, procedo con apertura
        self.apre_finestre_salvate()    
        
    def apre_finestre_salvate(self):
        """
           Apre le finestre che sono state salvate nella loro posizione e dimensione
        """        
        for my_window_pos in self.o_preferenze.l_windows_pos:
            if 'MGrepWindow' in my_window_pos:
                o_rect = QtCore.QRect()
                o_rect.setRect( int(my_window_pos[1]), int(my_window_pos[2]), int(my_window_pos[3]), int(my_window_pos[4]) )
                self.setGeometry(o_rect)                
            '''    
            elif 'MyPrefFileWindow' in my_window_pos:
                canvas1 = file_preferiti(self, modalita_test=False)
            elif 'MyPrefDir' in my_window_pos:
                canvas2 = directory_preferite(self, modalita_test=False)
            elif 'SearchString' in my_window_pos:
                canvas3 = ricerca_stringhe(self, modalita_test=False)
            elif 'SearchFile' in my_window_pos:
                canvas4 = ricerca_file(self, modalita_test=False)                
            elif 'OraRecompiler' in my_window_pos:
                canvas4 = oracle_recompiler(self, modalita_test=False)                            
            elif 'OraLocks' in my_window_pos:
                canvas4 = oracle_locks(self, modalita_test=False)                                        
            elif 'OraSessions' in my_window_pos:
                canvas4 = oracle_sessions(self, modalita_test=False)                                                        
            elif 'OraJobsStatus' in my_window_pos:
                canvas4 = oracle_jobs(self, modalita_test=False)                                                    
            elif 'OraSize' in my_window_pos:
                canvas4 = oracle_size(self, modalita_test=False)                                                                
            '''        
    
    def slot_actionSave_the_windows_position(self):
        """
           Salva la posizione delle finestre per riaprirle identiche all'avvio del programma
        """
        if message_question_yes_no('Do you want to save the windows position and set them for the next program startup?') == 'Yes':
            # pulisco la lista delle posizioni delle window
            self.o_preferenze.l_windows_pos.clear()
            
            # ricerco informazioni della window principale                                                
            o_pos = self.geometry()            
            o_rect = o_pos.getRect()            
            self.o_preferenze.l_windows_pos.append( "MGrepWindow " + str(o_rect[0]) + " " + str(o_rect[1]) + " " +  str(o_rect[2]) + " " + str(o_rect[3]) )                                    
            # ricerco le dimensione delle varie window che vengono aperte dal programma (non tutte al momento vengono salvate)
            o_window_list = self.ui.mdiArea.subWindowList()                        
            for i in range(0,len(o_window_list)):
                v_titolo = ''                
                if o_window_list[i].windowTitle() == 'My favorites files':
                    v_titolo = 'MyPrefFile'
                elif o_window_list[i].windowTitle() == 'My favorites directories':
                    v_titolo = 'MyPrefDir'                    
                elif o_window_list[i].windowTitle() == 'Search string in sources of Oracle Forms/Reports':
                    v_titolo = 'SearchString'                                        
                elif o_window_list[i].windowTitle() == 'Search file in system':
                    v_titolo = 'SearchFile'                                                            
                elif o_window_list[i].windowTitle() == 'Oracle recompiler':
                    v_titolo = 'OraRecompiler'                                                                                
                elif o_window_list[i].windowTitle() == 'Oracle locks':
                    v_titolo = 'OraLocks'                                                                                                    
                elif o_window_list[i].windowTitle() == 'Oracle sessions list':
                    v_titolo = 'OraSessions'                                                                                                                        
                elif o_window_list[i].windowTitle() == 'Oracle jobs':
                    v_titolo = 'OraJobsStatus'                                                                                                                                            
                elif o_window_list[i].windowTitle() == 'Oracle tables size':
                    v_titolo = 'OraSize'                                                                                                                                                                
                
                if v_titolo != '':                    
                    o_pos = o_window_list[i].geometry()            
                    o_rect = o_pos.getRect()            
                    self.o_preferenze.l_windows_pos.append( v_titolo + "  " + str(o_rect[0]) + " " + str(o_rect[1]) + " " +  str(o_rect[2]) + " " + str(o_rect[3]) )                                                        
                    
            # salvo la lista
            self.o_preferenze.salva_pos_finestre()            

    
    def slot_actionReset_main_window_position(self):
        """
           Reimposta la posizione e la dimensione della finestra principale
        """
        if message_question_yes_no('Do you want to reset position and size of main window?') == 'Yes':
            # dimensione finestra
            self.resize( 800, 600 )                        
            # centratura della window
            qr = self.frameGeometry()                
            cp = QtWidgets.QDesktopWidget().availableGeometry().center()                
            qr.moveCenter(cp)                
            self.move(qr.topLeft())            
    
    def slot_actionFactory_reset(self):
        """
           Ritorna alle preferenze di base eliminando la directory di lavoro. Al termine il programma viene chiuso senza salvare
        """
        if message_question_yes_no('Do you want delete the preferences files in folder ' + self.o_preferenze.work_dir + '?') == 'Yes':
            if message_question_yes_no('Are you sure?') == 'Yes':
                self.o_preferenze.cancella_tutto()
                message_info('Preferences files deleted! Close and restart the program!')                
            
    def slot_actionSearch_string(self):
        """
           Richiamo form di ricerca stringa
        """                
        from ricerca_stringhe import ricerca_stringhe_class        
        my_app = ricerca_stringhe_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()   
        
    def slot_actionFiles_in_system(self):
        """
           Richiamo form di ricerca files
        """                
        from ricerca_file import ricerca_file_class        
        my_app = ricerca_file_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()  
        
    def slot_actionImage_link_in_web_page(self):
        """
           Richiamo form di ricerca immagini in pagine web
        """                
        from ricerca_elementi_in_pagina_web import ricerca_elementi_in_pagina_web_class        
        my_app = ricerca_elementi_in_pagina_web_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()    
        
    def slot_actionPhone_book(self):
        """
           Richiamo form di ricerca rubrica telefonica
        """                
        from rubrica import rubrica_class        
        my_app = rubrica_class('T')        
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)                        
        my_app.show()            
        
    def slot_actionEmail_book(self):
        """
           Richiamo form di ricerca rubrica email
        """                
        from rubrica import rubrica_class        
        my_app = rubrica_class('E')
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()    
        
    def slot_actionRecompiler(self):
        """
           Richiamo form di ricompilazione oggetti invalidi lato oracle
        """                
        from oracle_recompiler import oracle_recompiler_class
        my_app = oracle_recompiler_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()            
        
    def slot_actionLocks(self):
        """
           Richiamo form di controllo sessioni e tabelle bloccate
        """                
        from oracle_locks import oracle_locks_class
        my_app = oracle_locks_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()   
        
    def slot_actionFavorites_files(self):
        """
           Richiamo form elenco e gestione file preferiti
        """                
        from file_preferiti import file_preferiti_class
        my_app = file_preferiti_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()           
        
    def slot_actionFavorites_dirs(self):
        """
           Richiamo form elenco e gestione directory preferite
        """                
        pass
        
    def slot_actionHelp(self):
        """
            visualizza help del programma
        """
        os.system("start help\\MGrep_help.html")
        
    def slot_actionProgram_info(self):
        """
           Richiamo form delle informazioni di programma
        """
        from program_info import program_info_class
        my_app = program_info_class(self.ui.mdiArea)
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_app.show()                   
        
    def slot_actionChange_log(self):
        """
           Richiamo changelog
        """
        os.system("start help\\MGrep_changelog.html")    
    
    def slot_actionConsole(self):
        """
           Richiamo visualizzazione della console python
        """
        pass                
                    
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = MGrep_class()
    application.show()
    sys.exit(app.exec())        