# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 24/07/2018
 Descrizione...: Programma per la ricompilazione degli oggetti di un database oracle
"""

#Librerie grafiche
import wx
import wx.dataview
import wx.lib.agw.pybusyinfo as PBI
#Librerie oracle
import cx_Oracle
#Librerie interne smigrep
from test_app import Test_App
from preferenze import preferenze
from utilita import pathname_icons

class oracle_recompiler:
    """
        Programma per la ricompilazione degli oggetti di un database oracle
    """
    def __init__(self, o_window_base, modalita_test):

        self.o_window_base = o_window_base
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        
        
        # creo la finestra come figlia della finestra di partenza (la posizione e la dimensione vengono lette dalla preferenze)
        win_pos = (0,0)
        win_size = (780,510)
        for my_window_pos in self.o_preferenze.l_windows_pos:
            if 'OraRecompiler' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))             
        
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Oracle recompiler", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # selezione del server
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"Oracle name server:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_server_name = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('ICOM_815','BACKUP_815','BACKUP_2_815'))
        self.e_server_name.SetSelection(0)

        self.b_search_all = wx.Button( self.panel, wx.ID_ANY, u"Search invalid objects", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_search_all.SetBitmap(wx.Bitmap( pathname_icons() + "search.gif", wx.BITMAP_TYPE_ANY ))
        self.b_search_all.SetToolTip("Search all invalid objects into oracle db server")

        self.b_compile_all = wx.Button( self.panel, wx.ID_ANY, u"Compile all invalid objects", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_compile_all.SetBitmap(wx.Bitmap( pathname_icons() + "compile.gif", wx.BITMAP_TYPE_ANY ))
        self.b_compile_all.SetToolTip("Recompile all invalid objects into oracle db server. At the end refresh the list with the remain invalid objects.")

        # definizione del widget lista risultati
        self.lista_db = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        self.lista_db.AppendTextColumn(label='Num.', width=50, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.lista_db.AppendTextColumn(label='Owner', width=150, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.lista_db.AppendTextColumn(label='Object name', width=300, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.lista_db.AppendTextColumn(label='Object type', width=200, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        # collego gli eventi agli oggetti (pulsante di ricerca e tasto enter sulla campo ricerca)
        self.b_search_all.Bind( wx.EVT_BUTTON, self.on_click_search_all )
        self.b_compile_all.Bind( wx.EVT_BUTTON, self.on_click_compile_all )

        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # sizer con titolo e combobox
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer1.Add( self.l_titolo1,      wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        gbSizer1.Add( self.e_server_name, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        # sizer con pulsanti
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer2.Add( self.b_search_all,   wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.Add( self.b_compile_all,  wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.AddGrowableCol(0)
        gbSizer2.AddGrowableCol(1)

        # sizer lista risultati
        gbSizer3 = wx.GridBagSizer( 0, 0 )
        gbSizer3.SetFlexibleDirection( wx.BOTH )
        gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer3.Add( gbSizer1,  wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer3.Add( gbSizer2,  wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer3.Add( self.lista_db,  wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer3.AddGrowableCol(1)
        gbSizer3.AddGrowableRow(2)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer3, 1, wx.ALL | wx.EXPAND, 10 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

    def on_click_search_all(self, event):
        """
            ricerca tutti gli oggetti invalidi
        """
        # pulisce la lista di eventuali valori precedenti
        self.lista_db.DeleteAllItems()
        # connessione al DB come amministratore
        try:
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.GetString(self.e_server_name.GetSelection()),
                                             mode=cx_Oracle.SYSDBA)
            v_error = False
        except:
            wx.MessageBox(message='Connection to oracle rejected. Please control login information.', caption='Error', style = wx.OK|wx.ICON_ERROR)
            v_error = True

        if not v_error:
            # apro cursori
            v_cursor = v_connection.cursor()
            # select per la ricerca degli oggetti invalidi
            v_cursor.execute(
                "SELECT OWNER, OBJECT_NAME, OBJECT_TYPE  FROM ALL_OBJECTS WHERE STATUS='INVALID' ORDER BY OBJECT_TYPE")
            i = 0
            rec_to_stringa = []
            for record in v_cursor:
                # visualizzo output nell'area di testo (le funzioni rjust e ljust inserisco a destra o sinistra degli spazi)
                i = i + 1
                rec_to_stringa = (str(i), str(record[0]), str(record[1]), str(record[2]))
                self.lista_db.AppendItem(rec_to_stringa)

            v_cursor.close()
            v_connection.close()

    def on_click_compile_all(self, event):
        """
            compila tutti gli oggetti invalidi
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.GetString(self.e_server_name.GetSelection()),
                                             mode=cx_Oracle.SYSDBA)
            v_error = False
        except:
            wx.MessageBox(message='Connection to oracle rejected. Please control login information.', caption='Error', style = wx.OK|wx.ICON_ERROR)
            v_error = True

        if not v_error:
            wait_win = PBI.PyBusyInfo(message="Please wait a moment...", parent=None, title="Recompiling")

            # apro cursori
            v_cursor = v_connection.cursor()

            # esecuzione dello script che ricompila tutti gli oggetti invalidi
            v_cursor.execute("BEGIN UTL_RECOMP.RECOMP_SERIAL(); END;")
            v_cursor.close()
            v_connection.close()

            # select per la ricerca degli oggetti invalidi
            self.on_click_search_all(None)

            del wait_win
            wx.MessageBox(message='Invalid objects recompiled!', caption='Info', style=wx.OK|wx.ICON_INFORMATION)

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    ###
    # test gestione file preferiti
    ###
    test = oracle_recompiler(o_window_base, modalita_test=True)

    app.MainLoop()
