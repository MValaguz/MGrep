# -*- coding: utf-8 -*-

"""
 ____  __  __ ___ ____ ____  _____ ____
/ ___||  \/  |_ _/ ___|  _ \| ____|  _ \
\___ \| |\/| || | |  _| |_) |  _| | |_) |
 ___) | |  | || | |_| |  _ <| |___|  __/
|____/|_|  |_|___\____|_| \_\_____|_|

 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con wxPython
 Data prima ver: 03/11/2016 
 Descrizione...: Per la spiegazione del programma fare riferimento al relativo file presente nella cartella help
 Note changelog: Per il changelog fare riferimento al relativo file presente nella cartella help

 Alcune note per la creazione dell'eseguibile che poi si può distribuire (al momento installato in O:\Install\SmiGrep)
   - deve essere installato il pkg pyinstaller
   - accertarsi che nella dir del sorgente di questo programma NON siano presenti directory dist e build
   - aprire una shell dos
   - posizionarsi sulla cartelle dove sono contenuti i sorgenti di questo programma
   - lanciare il comando "pyinstaller --windowed --icon=SmiGrep.ico SmiGrep.pyw" che crea due directory: la build si può eliminare,
     mentre la dist è quella che contiene-conterrà tutti gli elementi atti al funzionamento del programma senza
     avere python installato
   - nella directory dist copiare la cartella "icon" e "help"
   - nella directory dist copiare anche i file pscp.exe e plink.exe che servono per la pubblicazione di form e report
 E' stato creato anche un apposito script per la compilazione e distribuzione che funziona ovviamente solo con una
 determinata configurazione (presenza disco di rete "O" di windows)
"""

# wxpython base
import wx
# sistema
import os
import sys
# libreria per la gestione delle date
import datetime
# librerie del programma
from ricerca_stringhe import ricerca_stringhe
from ricerca_file import ricerca_file
from file_preferiti import file_preferiti
from directory_preferite import directory_preferite
from oracle_recompiler import oracle_recompiler
from oracle_locks import oracle_locks
from oracle_jobs import oracle_jobs
from oracle_sessions import oracle_sessions
from oracle_size import oracle_size
from rubrica import rubrica
from ricerca_elementi_in_pagina_web import ricerca_elementi_in_pagina_web
from tools_import_export import tools_import_export
from informazioni_programma import info
from preferenze import preferenze
from console import console
from utilita import pathname_icons

class o_smigrep_base ( wx.MDIParentFrame ):
    """
        creazione della finestra di base
    """
    def __init__( self, parent, p_program_version):

        self.versione_del_programma = p_program_version
        
        self.win_size = (800, 600)
        wx.MDIParentFrame.__init__(self, None, -1, title = u"SmiGrep " + self.versione_del_programma, size = self.win_size, style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        self.bg_bmp = wx.Bitmap( pathname_icons() + 'background15d.jpg', wx.BITMAP_TYPE_ANY )        
        self.GetClientWindow().Bind(wx.EVT_ERASE_BACKGROUND, self.disegna_background)

        # defizione status bar
        self.o_statusbar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        # definizione dei menu
        self.o_w1_menu_bar = wx.MenuBar( 0 )

        # menu file
        self.m_file = wx.Menu()

        self.m_save_windows_pos = wx.MenuItem( self.m_file, wx.ID_ANY, u"Save the windows position", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_save_windows_pos.SetBitmap(wx.Bitmap(pathname_icons() + 'disk.gif'))
        self.m_file.Append( self.m_save_windows_pos )
        
        self.m_reset_windows_pos = wx.MenuItem( self.m_file, wx.ID_ANY, u"Reset main window position", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_reset_windows_pos.SetBitmap(wx.Bitmap(pathname_icons() + 'centre.gif'))
        self.m_file.Append( self.m_reset_windows_pos )        

        self.m_factory_reset = wx.MenuItem( self.m_file, wx.ID_ANY, u"Factory &Reset", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_factory_reset.SetBitmap(wx.Bitmap(pathname_icons() + 'factory.gif'))
        self.m_file.Append( self.m_factory_reset )

        self.m_file.AppendSeparator()

        self.m_exit = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_exit.SetBitmap(wx.Bitmap( pathname_icons() + 'kill.gif'))
        self.m_file.Append( self.m_exit )

        self.o_w1_menu_bar.Append( self.m_file, "&File" )

        # menu search
        self.m_search = wx.Menu()

        self.m_search_string = wx.MenuItem( self.m_search, wx.ID_ANY, u"&String in the code source", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_search_string.SetBitmap(wx.Bitmap( pathname_icons() + 'search_string.gif'))
        self.m_search.Append( self.m_search_string )

        self.m_search_file = wx.MenuItem( self.m_search, wx.ID_ANY, u"&File in system", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_search_file.SetBitmap(wx.Bitmap( pathname_icons() + 'search_file.gif'))
        self.m_search.Append( self.m_search_file )

        self.m_search.AppendSeparator()

        self.m_search_image_link = wx.MenuItem( self.m_search, wx.ID_ANY, u"&Image link in web page", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_search_image_link.SetBitmap(wx.Bitmap( pathname_icons() + 'paint.gif'))
        self.m_search.Append( self.m_search_image_link )

        self.o_w1_menu_bar.Append( self.m_search, "&Search" )

        # menu books
        self.m_books = wx.Menu()
        self.m_phone_book = wx.MenuItem( self.m_books, wx.ID_ANY, u"&Phone Book", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_phone_book.SetBitmap(wx.Bitmap( pathname_icons() + 'phone.gif'))
        self.m_books.Append( self.m_phone_book )

        self.m_email_book = wx.MenuItem( self.m_books, wx.ID_ANY, u"&Email Book", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_email_book.SetBitmap(wx.Bitmap( pathname_icons() + 'mail.gif'))
        self.m_books.Append( self.m_email_book )

        self.o_w1_menu_bar.Append( self.m_books, "&Books" )

        # menu oracle
        self.m_oracle = wx.Menu()

        self.m_oracle_recompiler = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Recompiler", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_oracle_recompiler.SetBitmap(wx.Bitmap( pathname_icons() + 'gears.gif'))
        self.m_oracle.Append( self.m_oracle_recompiler )

        self.m_oracle_locks = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Locks", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_oracle_locks.SetBitmap(wx.Bitmap( pathname_icons() + 'lock.gif'))
        self.m_oracle.Append( self.m_oracle_locks )

        self.m_oracle_sessions = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Sessions", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_oracle_sessions.SetBitmap(wx.Bitmap( pathname_icons() + 'table.gif'))
        self.m_oracle.Append( self.m_oracle_sessions )
        
        self.m_oracle_jobs = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Jobs status", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_oracle_jobs.SetBitmap(wx.Bitmap( pathname_icons() + 'oracle.gif'))
        self.m_oracle.Append( self.m_oracle_jobs )
        
        self.m_oracle_size = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Tables Size", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_oracle_size.SetBitmap(wx.Bitmap( pathname_icons() + 'compile.gif'))
        self.m_oracle.Append( self.m_oracle_size )
                
        self.o_w1_menu_bar.Append( self.m_oracle, "&Oracle" )

        # menu favorites
        self.m_favorites = wx.Menu()

        self.m_favorites_files = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Files", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_favorites_files.SetBitmap(wx.Bitmap( pathname_icons() + 'favorites_files.gif'))
        self.m_favorites.Append( self.m_favorites_files )

        self.m_favorites_dirs = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Directories", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_favorites_dirs.SetBitmap(wx.Bitmap( pathname_icons() + 'favorites_directories.gif'))
        self.m_favorites.Append( self.m_favorites_dirs )

        self.o_w1_menu_bar.Append( self.m_favorites, "F&avorites" )
        
        # menu tools
        self.m_tools = wx.Menu()

        self.m_tools1 = wx.MenuItem( self.m_file, wx.ID_ANY, u"&Import-Export", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_tools1.SetBitmap(wx.Bitmap( pathname_icons() + 'db.gif'))
        self.m_tools.Append( self.m_tools1 )

        self.o_w1_menu_bar.Append( self.m_tools, "&Tools" )        

        # menu help
        self.m_help_and_info = wx.Menu()
        self.m_help = wx.MenuItem( self.m_help_and_info, wx.ID_ANY, u"&Help", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_help.SetBitmap(wx.Bitmap( pathname_icons() + 'help.gif'))
        self.m_help_and_info.Append( self.m_help )

        self.m_program_info = wx.MenuItem( self.m_help_and_info, wx.ID_ANY, u"&Program Info", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_program_info.SetBitmap(wx.Bitmap( pathname_icons() + 'info.gif'))
        self.m_help_and_info.Append( self.m_program_info )

        self.m_change_log = wx.MenuItem( self.m_help_and_info, wx.ID_ANY, u"&Change Log", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_change_log.SetBitmap(wx.Bitmap( pathname_icons() + 'history.gif'))
        self.m_help_and_info.Append( self.m_change_log )

        self.m_console = wx.MenuItem( self.m_file, wx.ID_ANY, u"Console", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_console.SetBitmap(wx.Bitmap( pathname_icons() + 'console.gif'))
        self.m_help_and_info.Append( self.m_console )

        self.o_w1_menu_bar.Append( self.m_help_and_info, "&Help" )

        # fine costruzione menu
        self.SetMenuBar( self.o_w1_menu_bar )

        # connessione degli eventi chiusura programma
        self.Bind(wx.EVT_CLOSE, self.on_click_chiusura_programma)

        # connessione eventi selezioni di menu
        self.Bind(wx.EVT_MENU, self.on_click_save_windows_pos, id = self.m_save_windows_pos.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_reset_windows_pos, id = self.m_reset_windows_pos.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_factory_reset, id = self.m_factory_reset.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_chiusura_programma, id = self.m_exit.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_rubrica_telefonica, id = self.m_phone_book.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_rubrica_email, id = self.m_email_book.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_ricerca_stringhe, id =self.m_search_string.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_ricerca_file, id =self.m_search_file.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_file_preferiti, id = self.m_favorites_files.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_directory_preferite, id = self.m_favorites_dirs.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_oracle_recompiler, id = self.m_oracle_recompiler.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_oracle_locks, id = self.m_oracle_locks.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_oracle_sessions, id = self.m_oracle_sessions.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_oracle_jobs, id = self.m_oracle_jobs.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_oracle_size, id = self.m_oracle_size.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_import_export_tools, id = self.m_tools1.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_help_programma, id = self.m_help.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_informazioni_programma, id = self.m_program_info.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_changelog_programma, id = self.m_change_log.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_ricerca_elementi_in_pagina_web, id = self.m_search_image_link.GetId() )
        self.Bind(wx.EVT_MENU, self.on_click_view_console, id = self.m_console.GetId() )

        # centratura automatica della window
        self.Centre( wx.BOTH )

        # creo la finestra console nascosta!
        self.o_console = console(self, modalita_test=False)
        # se il programma è lanciato "live", cioè da editor, la console si apre di default
        # l'attributo frozen che viene controllato viene generato durante la compilazione tramite il comando pyinstaller
        if not getattr(sys, 'frozen', False):
            self.o_console.view_console()

        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()

        # se dalle preferenze emerge che vanno aperte delle window in una certa posizione, procedo con apertura
        self.apre_finestre_salvate()

    def disegna_background(self, event):
        """
            disegna il background della finestra
        """
        dc = event.GetDC()
    
        # tile the background bitmap
        try:
            sz = self.GetClientSize()
        except RuntimeError:#closing demo
            return
        w = self.bg_bmp.GetWidth()
        h = self.bg_bmp.GetHeight()
        x = 0

        while x < sz.width:
            y = 0
            while y < sz.height:
                dc.DrawBitmap(self.bg_bmp, x, y)
                y = y + h

            x = x + w

    def apre_finestre_salvate(self):
        """
            Apre le finestre che sono state salvate nella loro posizione e dimensione
        """
        for my_window_pos in self.o_preferenze.l_windows_pos:
            if 'SmiGrep' in my_window_pos:
                self.SetPosition( (int(my_window_pos[1]), int(my_window_pos[2])) )
                self.SetSize( (int(my_window_pos[3]), int(my_window_pos[4])) )
            elif 'MyPrefFile' in my_window_pos:
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

    def on_click_save_windows_pos(self, event):
        """
            Salva la posizione delle finestre per riaprirle identiche all'avvio del programma
        """
        if wx.MessageBox(message='Do you want to save the windows position and set them for the next program startup?' , caption='Question', style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            # pulisco la lista delle posizioni delle window
            self.o_preferenze.l_windows_pos.clear()
            
            # ricerco informazioni della window principale                                    
            o_pos = self.GetPosition()
            o_size = self.GetSize()
            self.o_preferenze.l_windows_pos.append( "SmiGrep " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )            

            # ricerco informazioni della window dei files preferiti
            o_win = self.FindWindowByLabel('My favorites files')
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "MyPrefFile " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )

            # ricerco informazioni della window delle directories preferite
            o_win = self.FindWindowByLabel('My favorites directories')
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "MyPrefDir " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )

            # ricerco informazioni della window della ricerca stringhe
            o_win = self.FindWindowByLabel("Search string in sources of Oracle Forms/Report and Oracle Apex")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "SearchString " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                
                    
            # ricerco informazioni della window della ricerca stringhe
            o_win = self.FindWindowByLabel("Search file in system")
            if o_win is not None:            
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "SearchFile " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                
            
            # ricerco informazioni della window delle ricompilazioni
            o_win = self.FindWindowByLabel("Oracle recompiler")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "OraRecompiler " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                
                
            # ricerco informazioni della window dei lock
            o_win = self.FindWindowByLabel("Oracle locks")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "OraLocks " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                            
                
            # ricerco informazioni della window delle sessions
            o_win = self.FindWindowByLabel("Oracle sessions list")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "OraSessions " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                            
                
            # ricerco informazioni della window delle sessions
            o_win = self.FindWindowByLabel("Oracle jobs")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "OraJobsStatus " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                                        
                                    
            # ricerco informazioni della window delle table dimension
            o_win = self.FindWindowByLabel("Oracle tables size")
            if o_win is not None:                
                o_label = o_win.GetLabel()
                o_pos = o_win.GetPosition()
                o_size = o_win.GetSize()
                self.o_preferenze.l_windows_pos.append( "OraSize " + str(o_pos.Get()[0]) + " " + str(o_pos.Get()[1]) + " " +  str(o_size.Get()[0]) + " " + str(o_size.Get()[1]) )                                        
                                    
            # salvo la lista
            self.o_preferenze.salva_pos_finestre()            

    def on_click_reset_windows_pos(self, event):
        """
            Reimposta la posizione e la dimensione della finestra principale
        """
        if wx.MessageBox(message='Do you want to reset position and size of main window?' , caption='Question', style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            self.SetSize( self.win_size[0], self.win_size [1] )            
            self.Centre( wx.BOTH )
            
    def on_click_import_export_tools(self, evetn):
        """
            richiama la procedura dei tools di import-export
        """
        # apro una nuova finestra figlia della principale
        canvas = tools_import_export(self, modalita_test=False)        
    
    def on_click_view_console(self, event):
        """
            Rende visibile la finestra di console
        """
        self.o_console.view_console()

    def on_click_file_preferiti(self, event):
        """
            richiama la procedura di gestione dei file preferiti
        """
        # apro una nuova finestra figlia della principale
        canvas = file_preferiti(self, modalita_test=False)

    def on_click_directory_preferite(self, event):
        """
            richiama la procedura di gestione delle directory preferite
        """
        # apro una nuova finestra figlia della principale
        canvas = directory_preferite(self, modalita_test=False)

    def on_click_ricerca_stringhe(self, event):
        """
            richiama la procedura di ricerca delle stringhe
        """
        # apro una nuova finestra figlia della principale
        canvas = ricerca_stringhe(self, modalita_test=False)

    def on_click_ricerca_file(self, event):
        """
            richiama la procedura di ricerca dei file
        """
        # apro una nuova finestra figlia della principale
        canvas = ricerca_file(self, modalita_test=False)

    def on_click_oracle_recompiler(self, event):
        """
            richiama la procedura di ricompilazione oggetti invalidi di oracle
        """
        # apro una nuova finestra figlia della principale
        canvas = oracle_recompiler(self, modalita_test=False)

    def on_click_oracle_locks(self, event):
        """
            richiama la procedura di controllo locks
        """
        # apro una nuova finestra figlia della principale
        canvas = oracle_locks(self, modalita_test=False)

    def on_click_oracle_sessions(self, event):
        """
            richiama la procedura di controllo sessioni
        """
        # apro una nuova finestra figlia della principale
        canvas = oracle_sessions(self, modalita_test=False)
        
    def on_click_oracle_jobs(self, event):
        """
            richiama la procedura di controllo job
        """
        # apro una nuova finestra figlia della principale
        canvas = oracle_jobs(self, modalita_test=False)
        
    def on_click_oracle_size(self, event):
        """
            richiama la procedura di verifica dimensione tabelle
        """
        # apro una nuova finestra figlia della principale
        canvas = oracle_size(self, modalita_test=False)
                
    def on_click_rubrica_telefonica(self, event):
        """
            richiama la procedura di ricerca rubrica telefonica
        """
        # apro una nuova finestra figlia della principale
        canvas = rubrica(self, tipo_rubrica="T", modalita_test=False)

    def on_click_rubrica_email(self, event):
        """
            richiama la procedura di ricerca rubrica email
        """
        # apro una nuova finestra figlia della principale
        canvas = rubrica(self, tipo_rubrica="E", modalita_test=False)

    def on_click_ricerca_elementi_in_pagina_web(self, event):
        """
            richiama la procedura che ricerca immagini in pagina web
        """
        canvas = ricerca_elementi_in_pagina_web(self, modalita_test=False)

    def on_click_help_programma(self, event):
        """
            visualizza help del programma
        """
        os.system("start help\\smigrep_help.html")

    def on_click_informazioni_programma(self, event):
        """
            visualizza info del programma
        """
        info(self.versione_del_programma)

    def on_click_changelog_programma(self, event):
        """
            visualizza il changelog del programma
        """
        os.system("start help\\smigrep_changelog.html")

    def on_click_factory_reset(self, event):
        """
            ritorna alle preferenze di base eliminando la directory di lavoro. Al termine il programma viene chiuso senza salvare
        """
        if wx.MessageBox(message='Do you want delete the preferences files in folder ' + self.o_preferenze.work_dir + '?' , caption='Factory reset', style=wx.YES_NO|wx.ICON_EXCLAMATION) == wx.YES:
            if wx.MessageBox(message='Are you sure?', caption='Factory reset', style=wx.YES_NO|wx.ICON_EXCLAMATION) == wx.YES:
                self.o_preferenze.cancella_tutto()
                wx.MessageBox(message='Preferences files deleted! The program will be closed! Then you can restart it!', caption='Factory reset', style=wx.OK|wx.ICON_INFORMATION)
                # chiude il programma
                self.Destroy()

    def on_click_chiusura_programma(self, event):
        """
            chiude il programma
        """
        self.Destroy()

# ------------------------
# avvio l'applicazione
# ------------------------
if __name__ == "__main__":
    # redirect = false attiva la possibilità di reindirizzare stdout e stderr su una window
    app = wx.App(redirect = False)
    o_window_base = o_smigrep_base(None, '1.6b')
    o_window_base.Show(True)
    app.MainLoop()
