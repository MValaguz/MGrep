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
 
 Note!!!!!!!!!!! Il programma quando si avvia reindirizza output verso i file di testo! Quindi se non lanciato da Wing-Editor, gli errori potrebbero non vedersi!
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
from utilita import message_error, message_info, message_question_yes_no, my_console
       
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
                
        # l'attributo frozen viene attivato quando il programma viene compilato; quindi,
        # quando il programma viene eseguito onsite, evenutali errori non controllati vengono reindirizzati
        # verso specifici file di testo presenti nella directory di lavoro        
        sys.stdout = my_console(self.o_preferenze.work_dir + '\\MGrep_stdout.txt')
        sys.stderr = my_console(self.o_preferenze.work_dir + '\\MGrep_stderr.txt')
        
    def apre_finestre_salvate(self):
        """
           Apre le finestre che sono state salvate nella loro posizione e dimensione
        """
        for my_window_pos in self.o_preferenze.l_windows_pos:                        
            if 'MainWindow' in my_window_pos:
                o_rect = QtCore.QRect()
                o_rect.setRect( int(my_window_pos[1]), int(my_window_pos[2]), int(my_window_pos[3]), int(my_window_pos[4]) )
                self.setGeometry(o_rect)                
            elif 'Search string in sources of Oracle Forms/Reports'.replace(' ','_') in my_window_pos:
                self.slot_actionSearch_string()
            elif 'Search file in system'.replace(' ','_') in my_window_pos:
                self.slot_actionFiles_in_system()
            elif 'Search images in web pages'.replace(' ','_') in my_window_pos:
                self.slot_actionImage_link_in_web_page()
            elif 'Phone book'.replace(' ','_') in my_window_pos:
                self.slot_actionPhone_book()
            elif 'Email book'.replace(' ','_') in my_window_pos:
                self.slot_actionEmail_book()
            elif 'Oracle recompiler'.replace(' ','_') in my_window_pos:
                self.slot_actionRecompiler()
            elif 'Oracle locks'.replace(' ','_') in my_window_pos:
                self.slot_actionLocks()
            elif 'Oracle sessions list'.replace(' ','_') in my_window_pos:
                self.slot_actionSessions()
            elif 'Oracle jobs'.replace(' ','_') in my_window_pos:
                self.slot_actionJobs_status()
            elif 'Oracle volume'.replace(' ','_') in my_window_pos:
                self.slot_actionVolume()
            elif 'My favorites files'.replace(' ','_') in my_window_pos:
                self.slot_actionFavorites_files()
            elif 'My favorites directories'.replace(' ','_') in my_window_pos:            
                self.slot_actionFavorites_dirs()
            elif 'Ascii_Graphics_Generator'.replace(' ','_') in my_window_pos:            
                self.slot_actionAscii_graphics()                            
    
    def slot_actionSave_the_windows_position(self):
        """
           Salva la posizione delle finestre per riaprirle identiche all'avvio del programma
        """
        if message_question_yes_no('Do you want to save the windows position and set them for the next program startup?') == 'Yes':
            # pulisco la lista delle posizioni delle window
            self.o_preferenze.l_windows_pos.clear()
            
            # ricerco informazioni della window principale (è l'unica window di cui salvo sia posizione che dimensione)
            o_pos = self.geometry()            
            o_rect = o_pos.getRect()            
            self.o_preferenze.l_windows_pos.append( "MainWindow " + str(o_rect[0]) + " " + str(o_rect[1]) + " " +  str(o_rect[2]) + " " + str(o_rect[3]) )                                    
            # salvo i nomi delle varie finestre aperte
            o_window_list = self.ui.mdiArea.subWindowList()                        
            for i in range(0,len(o_window_list)):                
                self.o_preferenze.l_windows_pos.append( str(o_window_list[i].windowTitle()).replace(' ','_') ) 
                    
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
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/search_string.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)
        my_app.show()   
        
    def slot_actionFiles_in_system(self):
        """
           Richiamo form di ricerca files
        """                
        from ricerca_file import ricerca_file_class        
        my_app = ricerca_file_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/search_file.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)        
        my_app.show()  
        
    def slot_actionImage_link_in_web_page(self):
        """
           Richiamo form di ricerca immagini in pagine web
        """                
        from ricerca_elementi_in_pagina_web import ricerca_elementi_in_pagina_web_class        
        my_app = ricerca_elementi_in_pagina_web_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/paint.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                
        my_app.show()    
        
    def slot_actionPhone_book(self):
        """
           Richiamo form di ricerca rubrica telefonica
        """                
        from rubrica import rubrica_class        
        my_app = rubrica_class('T')        
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)                        
        my_sub_window.setWindowTitle('Phone book')
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/phone.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                        
        my_app.show()            
        
    def slot_actionEmail_book(self):
        """
           Richiamo form di ricerca rubrica email
        """                
        from rubrica import rubrica_class        
        my_app = rubrica_class('E')
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_sub_window.setWindowTitle('Email book')
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/mail.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                
        my_app.show()    
        
    def slot_actionRecompiler(self):
        """
           Richiamo form di ricompilazione oggetti invalidi lato oracle
        """                
        from oracle_recompiler import oracle_recompiler_class
        my_app = oracle_recompiler_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/gears.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                        
        my_app.show()            
        
    def slot_actionLocks(self):
        """
           Richiamo form di controllo sessioni e tabelle bloccate
        """                
        from oracle_locks import oracle_locks_class
        my_app = oracle_locks_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/lock.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                
        my_app.show()   
        
    def slot_actionSessions(self):
        """
           Richiamo form di elenco sessioni
        """                
        from oracle_sessions import oracle_sessions_class
        my_app = oracle_sessions_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/table.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                        
        my_app.show()           
                
    def slot_actionTop_sessions(self):
        """
           Richiamo form di elenco dei processi-sessioni (questa finestra ho deciso di non incorporarla insieme alle altre)
        """                
        from oracle_top_sessions import oracle_top_sessions_class                
        # Controllo che l'app non sia già in esecuzione perchè non committando i dati, una seconda istanza manderebbe in blocco il DB sqlite
        v_error = False
        try:
            if self.top_sessions != None and self.top_sessions.v_app_top_session_open:
                message_error('Top sessions is already execute')
                v_error = True
        except:
            v_error = False
        
        if not v_error:
            self.top_sessions = oracle_top_sessions_class()
            self.top_sessions.show()
        
    def slot_actionJobs_status(self):
        """
           Richiamo form stato dei jobs 
        """                
        from oracle_jobs import oracle_jobs_class
        my_app = oracle_jobs_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/oracle.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                
        my_app.show()   
        
    def slot_actionTable_space(self):
        """
           Richiamo form table space 
        """                
        from oracle_table_space import oracle_table_space_class
        my_app = oracle_table_space_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/db.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                
        my_app.show()   
        
    def slot_actionVolume(self):
        """
           Richiamo form occupazione volume
        """                
        from oracle_volume import oracle_volume_class
        my_app = oracle_volume_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/compile.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                        
        my_app.show()               
            
    def slot_actionFavorites_files(self):
        """
           Richiamo form elenco e gestione file preferiti
        """                
        from file_preferiti import file_preferiti_class
        my_app = file_preferiti_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/favorites_files.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                                
        my_app.show()           
        
    def slot_actionFavorites_dirs(self):
        """
           Richiamo form elenco e gestione directory preferite
        """                
        from directory_preferite import directory_preferite_class
        my_app = directory_preferite_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/favorites_directories.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                                        
        my_app.show()       
        
    def slot_actionImport_Export(self):
        """
           Richiamo tools per import-export
        """                
        from import_export import import_export_class
        my_app = import_export_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/db.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                                                
        my_app.show()             
        
    def slot_actionAscii_graphics(self):
        """
           Richiamo form per conversione testo in big testo
        """                
        from ascii_graphics import ascii_graphics_class
        my_app = ascii_graphics_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/font.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                                                
        my_app.show()     
        
    def slot_actionDownload(self):
        """
           Richiamo form per download di un sorgente da server iAS12g
        """                
        from download_from_server import download_from_server_class
        my_app = download_from_server_class()
        my_sub_window = self.ui.mdiArea.addSubWindow(my_app)        
        my_icon = QtGui.QIcon()
        my_icon.addPixmap(QtGui.QPixmap(":/icons/icons/download.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)                
        my_sub_window.setWindowIcon(my_icon)                                                                                                
        my_app.show()             
        
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
                        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])
    application = MGrep_class()
    # titolo dell'applicazione!
    application.setWindowTitle('MGrep 1.3')
    application.show()
    sys.exit(app.exec())        