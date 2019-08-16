# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 17/07/2018
 Descrizione...: Programma per la ricerca dei file in un percorso di directory
"""

#Librerie sistema
import os
#Librerie di data base
import sqlite3
#Librerie grafiche
import wx
#Librerie interne SmiGrep
from preferenze import preferenze
from test_app import Test_App
from utilita import pathname_icons

class ricerca_file:
    """
        Programma per la ricerca dei file nel file system
    """
    def __init__(self, o_window_base, modalita_test):
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()

        # creo la finestra come figlia della finestra di partenza (la posizione e la dimensione vengono lette dalla preferenze)
        win_pos = (0,0)
        win_size = (780,510)
        for my_window_pos in self.o_preferenze.l_windows_pos:
            if 'SearchFile' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))

        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Search file in system", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon( pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # variabili per controllo caricamento della cache
        self.v_t2_pathname = ''
        self.v_t2_filter = ''
        self.v_t2_excludepath = ''

        self.l_filesearch = wx.StaticText( self.panel, wx.ID_ANY, u"File search", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_filesearch = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        self.l_pathname = wx.StaticText( self.panel, wx.ID_ANY, u"Folder name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_pathname = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        self.b_pathname = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "folder.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.l_filter = wx.StaticText( self.panel, wx.ID_ANY, u"File filter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_filter = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        self.l_excludepath = wx.StaticText( self.panel, wx.ID_ANY, u"Exclude directories", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_excludepath = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        self.b_excludepath = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "folder.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.c_cache_file_system = wx.CheckBox( self.panel, wx.ID_ANY, u"Clear cache file system", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.c_cache_file_system.SetValue(True)
        self.b_save_pref = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "disk.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_save_pref.SetToolTip( u"Save the search data in order to be retrieved at the next start of SmiGrep" )
        self.b_add_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "add.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_add_line.SetToolTip( u"Add the selected line to 'My favorites files'" )
        self.b_search = wx.Button( self.panel, wx.ID_ANY, u"Start search", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_search.SetBitmap(wx.Bitmap( pathname_icons() + "go.gif", wx.BITMAP_TYPE_ANY ))
        o_lst1Choices = []
        self.o_lst1 = wx.ListBox( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,100), o_lst1Choices, style = wx.LB_SINGLE|wx.HSCROLL|wx.VSCROLL)
        self.l_risultati = wx.StaticText( self.panel, wx.ID_ANY, u"Result:", wx.DefaultPosition, wx.DefaultSize, 0 )

        # collego gli eventi agli oggetti (pulsante di ricerca e tasto enter sulla campo ricerca)
        self.b_pathname.Bind( wx.EVT_BUTTON, self.folder_dialog )
        self.b_excludepath.Bind( wx.EVT_BUTTON, self.exclude_dialog )
        self.b_add_line.Bind( wx.EVT_BUTTON, self.aggiunge_riga_preferiti )
        self.b_save_pref.Bind( wx.EVT_BUTTON, self.salva_preferenze )
        self.b_search.Bind( wx.EVT_BUTTON, self.avvia_ricerca_file )
        self.o_lst1.Bind( wx.EVT_LISTBOX_DCLICK, self.doppio_click )

        # imposto i valori ricevuti come preferiti
        self.e_filesearch.SetValue( self.o_preferenze.filesearch )
        self.e_pathname.SetValue( self.o_preferenze.pathname2 )
        self.e_excludepath.SetValue( self.o_preferenze.excludepath2 )
        self.e_filter.SetValue( self.o_preferenze.filter2 )

        ###
        # Impaginazione degli elementi
        ###

        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # box figlio
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer1.Add( self.l_filesearch,        wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_filesearch,        wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_pathname,          wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_pathname,          wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_pathname,          wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_filter,            wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_filter,            wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_excludepath,       wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_excludepath,       wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_excludepath,       wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.c_cache_file_system, wx.GBPosition( 3, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_risultati,         wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_BOTTOM|wx.LEFT, 1 )
        gbSizer1.Add( self.o_lst1,              wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 1 )
        # indico che la colonna 4 (dove finisce la lista dei risultati e la progress bar) e la riga 8 (dove è posizionata la lista) sono flessibili
        gbSizer1.AddGrowableCol(4)
        gbSizer1.AddGrowableRow(5)

        # box nipote per pulsanti di avvio ricerca
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer2.Add( self.b_save_pref,  wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 0 )
        gbSizer2.Add( self.b_add_line,   wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 0 )
        gbSizer2.Add( self.b_search,     wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 0 )
        gbSizer2.AddGrowableCol(2)

        # inserisco il nipote dentro il figlio
        gbSizer1.Add( gbSizer2, wx.GBPosition( 4, 3 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 10 )

        # inserisco il figlio dentro il padre
        bSizer_padre.Add( gbSizer1, 1, wx.ALL | wx.EXPAND, 10 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()
        #self.my_window.Maximize()

    def salva_preferenze(self, event):
        self.o_preferenze.filesearch = self.e_filesearch.GetValue()
        self.o_preferenze.pathname2 = self.e_pathname.GetValue()
        self.o_preferenze.excludepath2 = self.e_excludepath.GetValue()
        self.o_preferenze.filter2 = self.e_filter.GetValue()
        self.o_preferenze.salva()

    def folder_dialog(self, event):
        """
            selezione in tab string search apre la finestra di dialogo per selezionare una directory
        """
        dlg = wx.DirDialog(self.my_window, "Choose a directory:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.e_pathname.SetValue( dlg.GetPath() )
        dlg.Destroy()

    def exclude_dialog(self, event):
        """
            button esclusioni in tab string search apre la finestra di dialogo per selezionare una directory
        """
        dlg = wx.DirDialog(self.my_window, "Choose a directory:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            # Prenderò solo la parte della directory, di solito la seconda posizione
            v_directory_scelta = os.path.split( dlg.GetPath() )[1]
            if v_directory_scelta != '':
                if self.e_excludepath.GetValue() != '':
                    self.e_excludepath.SetValue(self.e_excludepath.GetValue() + ',' + v_directory_scelta)
                else:
                    self.e_excludepath.SetValue(v_directory_scelta)
        dlg.Destroy()

    def aggiunge_riga_preferiti(self, event):
        """
            aggiunge la riga nei preferiti
        """
        f_output = open(self.o_preferenze.favorites_file, 'a')
        f_output.write(self.o_lst1.GetString(self.o_lst1.GetSelection()) + '\n')
        f_output.close()

    def doppio_click(self,event):
        """
            doppio click su listbox risultati della ricerca
        """
        v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        if v_seltext != '':
            try:
                os.startfile(v_seltext)
            except:
                wx.MessageBox(text='File not found or problem during open application!', caption = 'Error', style = ex.OK | wx.ICON_ERROR)

    def copy_file_system_in_db(self,
                               v_sqlite_db_name,
                               v_root_node,
                               v_filter,
                               v_exclude):
        """
            Copia nella tabella FILE_SYSTEM del db p_sqlite_db_name
            tutto l'albero dei files, partendo dalla radice p_path_name

            Nota Bene: Passando p_sqlite_db_name = ':MEMORY' verrà creato in RAM e non su disco
        """
        # Apre il DB sqlite
        v_sqlite_conn = sqlite3.connect(database=v_sqlite_db_name)
        # Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()

        # Cancello la tabella se già presente nel db sqlite
        try:
            v_sqlite_cur.execute('DROP TABLE FILE_SYSTEM')
        except:
            pass

        # Creo la tabella
        v_sqlite_cur.execute('CREATE TABLE FILE_SYSTEM (DIR_NAME VARCHAR2(1000), FILE_NAME VARCHAR2(1000))')

        # ricavo una tupla contenente i filtri di ricerca separati
        v_filtri_ricerca = v_filter.split(',')

        # ricavo una tupla contenente le directory da escludere
        v_exclude_ricerca = v_exclude.split(',')

        # lista dei files contenuti nella directory (os.walk restituisce le tuple di tutte le directory partendo dal punto di root)
        for root, dirs, files in os.walk(v_root_node):
            # elimino dall'albero delle dir quelle che vanno escluse!
            # Se la stessa dir fosse presente anche ai livelli successivi, viene eliminata anche da li
            for i in range(0, len(v_exclude_ricerca)):
                if v_exclude_ricerca[i] in dirs:
                    dirs.remove(v_exclude_ricerca[i])
            # scorro le tuple dei nomi dentro tupla dei files
            for name in files:
                # stesso discorso istruzione precedente per quanto riguarda la directory (viene poi salvata nel file risultato)
                v_dir = os.path.join(root)
                # stesso discorso istruzione precedente per quanto riguarda il file (viene poi salvata nel file risultato)
                v_file = os.path.join(name)
                # se presenti i filtri di ricerca --> controllo che il file corrisponda alla lista indicata
                v_file_is_valid = False
                if v_filter != '':
                    for i in range(0, len(v_filtri_ricerca)):
                        if v_file.find(v_filtri_ricerca[i]) > 0:
                            v_file_is_valid = True
                            break
                else:
                    v_file_is_valid = True
                # se file è valido --> lo scrivo nel db
                if v_file_is_valid:
                    # scrittura del risultato della ricerca
                    v_sql = "INSERT INTO FILE_SYSTEM(DIR_NAME, FILE_NAME) VALUES(:v_dir,:v_file)"
                    v_sqlite_cur.execute(v_sql, {'v_dir': v_dir, 'v_file': v_file})
                    # refresh della window (per avanzamento della progress bar)
                    self.wait_win.Pulse()
        # commit
        v_sqlite_conn.commit()
        # chiusura dei cursori
        v_sqlite_conn.close()

    def ricerca_file(self,
                     v_root_node,
                     v_filesearch,
                     v_filter,
                     v_exclude):
        """
            ricerca file
        """
        # Se richiesto dal flag della cache...
        if self.c_cache_file_system.GetValue():
            # emetto messaggio sulla progress bar
            self.wait_win.Pulse('Load file system cache...please wait...')
            # copio il file system dentro la cache di un db sqlite (questo per velorizzare le ricerche successive)
            self.copy_file_system_in_db(self.o_preferenze.name_file_for_db_cache,
                                        v_root_node,
                                        v_filter,
                                        v_exclude)
            # la cache è caricata e non è necessario ricaricarla successivamente
            self.c_cache_file_system.SetValue(False)

        # Apre il DB sqlite
        v_sqlite_conn = sqlite3.connect(database=self.o_preferenze.name_file_for_db_cache)
        # Indico al db di funzionare in modalità str altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()
        v_sqlite_cur.execute("SELECT DIR_NAME, FILE_NAME FROM FILE_SYSTEM WHERE UPPER(FILE_NAME) LIKE :filesearch",
                             {'filesearch': '%' + v_filesearch + '%'})
        for row in v_sqlite_cur:
            # visualizzo output nell'area di testo (normalizzo la pathname del file con i separatori corretti)
            v_nome_completo_file = os.path.normpath(row[0] + "/" + row[1])
            self.o_lst1.Append(v_nome_completo_file)
            # Chiudo connessione
        v_sqlite_conn.close()

    def avvia_ricerca_file(self, event):
        """
            esegue la ricerca del file
        """
        v_ok = True
        # controllo che ci siano i dati obbligatori
        if self.e_filesearch.GetValue() == '':
            wx.MessageBox(message='Please enter a file name', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_pathname.GetValue() == '':
            wx.MessageBox(message='Please enter a pathname', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # i controlli sono stati superati --> avvio la ricerca
        if v_ok:
            # Se la cache non è attiva, controllo se sono cambiati i valori di ricerca (es. path) perché allora vuol dire che la cache va ripristinata
            if not self.c_cache_file_system.GetValue():
                if self.v_t2_pathname != self.e_pathname.GetValue() or self.v_t2_filter != self.e_filter.GetValue() or self.v_t2_excludepath != self.e_excludepath.GetValue():
                    # I valori sono cambiati e la cache va ricaricata
                    self.c_cache_file_system.SetValue(True)

            # Carico le var globali che permetteranno il confronto ai giri successivi. In pratica la cache va ricaricata automaticamente se sono cambiati dei parametri di ricerca
            self.v_t2_pathname = self.e_pathname.GetValue()
            self.v_t2_filter = self.e_filter.GetValue()
            self.v_t2_excludepath = self.e_excludepath.GetValue()

            # avanzamento progressbar
            self.wait_win = wx.ProgressDialog(title='Searching', message='Please wait', maximum=1000, parent=None, style=wx.PD_AUTO_HIDE|wx.PD_ELAPSED_TIME)
            self.wait_win.Show()

            # pulizia dell'item dei risultati
            self.o_lst1.Clear()

            # richiama la ricerca nel file system se presente file system
            self.ricerca_file(self.e_pathname.GetValue(),
                              self.e_filesearch.GetValue(),
                              self.e_filter.GetValue(),
                              self.e_excludepath.GetValue())

            # fermo la progressbar
            self.wait_win.Destroy()

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    ###
    # test ricerca file
    ###
    test = ricerca_file(o_window_base, modalita_test=True)

    app.MainLoop()
