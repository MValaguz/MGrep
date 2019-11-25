# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 30/07/2018
 Descrizione...: Programma per controllare le sessioni di sistema di un DB Oracle
"""

#Librerie grafiche
import wx
import wx.dataview
#Librerie oracle
import cx_Oracle
#Librerie di sistema
import os
#Librerie interne smigrep
from test_app import Test_App
from preferenze import preferenze
from utilita_database import killa_sessione
from utilita import pathname_icons

class oracle_sessions:
    """
        Programma per controllare le sessioni di sistema di un DB Oracle
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
            if 'OraSessions' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))             
                  
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Oracle sessions list", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon( pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # selezione del server
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"Oracle name server:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_server_name = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('ICOM_815','BACKUP_815','BACKUP_2_815'))
        self.e_server_name.SetSelection(0)

        # lista delle sessioni
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, u"User name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_user_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER)
        self.l_titolo3 = wx.StaticText( self.panel, wx.ID_ANY, u"Program name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_program_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER)        
        self.l_titolo4 = wx.StaticText( self.panel, wx.ID_ANY, u"Terminal:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_terminal = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER)                
        
        self.b_go = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "go.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_go.SetToolTip("Search the specific session. It is not case sensitive and accept partial strings.")

        self.b_session_information = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "sql.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_session_information.SetToolTip("Create a file with session information (open cursor)")        
        self.b_kill_session = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "kill.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_kill_session.SetToolTip("Kill the selected session")

        self.o_lst_sessions = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        self.o_lst_sessions.AppendTextColumn(label='#Row', width=50, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Sid', width=50, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Serial Nr.', width=60, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Terminal', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Session Name', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='User Name', width=200, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Status', width=70, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Program', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Description', width=250, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Action', width=90, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='Logon time', width=110, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        # collego gli eventi agli oggetti
        self.b_go.Bind( wx.EVT_BUTTON, self.on_click_cerca_sessioni )
        self.e_user_name.Bind( wx.EVT_TEXT_ENTER, self.on_click_cerca_sessioni )
        self.e_program_name.Bind( wx.EVT_TEXT_ENTER, self.on_click_cerca_sessioni )
        self.e_terminal.Bind( wx.EVT_TEXT_ENTER, self.on_click_cerca_sessioni )
        self.b_session_information.Bind( wx.EVT_BUTTON, self.on_click_session_information )
        self.b_kill_session.Bind( wx.EVT_BUTTON, self.on_click_kill_sessione )

        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # sizer con titolo e combobox
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.Add( self.b_session_information,  wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.b_kill_session,         wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )        

        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        gbSizer1.Add( self.l_titolo1,              wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_server_name,          wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_titolo2,              wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_user_name,            wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_titolo3,              wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_program_name,         wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )        
        gbSizer1.Add( self.l_titolo4,              wx.GBPosition( 2, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_terminal,             wx.GBPosition( 2, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )                
        gbSizer1.Add( self.b_go,                   wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( gbSizer2,                    wx.GBPosition( 2, 6 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT, 1 )
        gbSizer1.Add( self.o_lst_sessions,         wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 7 ), wx.ALL|wx.EXPAND, 1 )        
        gbSizer1.AddGrowableCol(6)
        gbSizer1.AddGrowableRow(3)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer1, 1, wx.ALL | wx.EXPAND, 5 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

        # mi posiziono sul campo nome utente
        self.e_user_name.SetFocus()
        
    def on_click_session_information(self, event):
        """
            crea un file riportante le informazioni di sessione (al momento i cursori aperti)
        """
        if self.o_lst_sessions.GetItemCount() > 0 and self.o_lst_sessions.GetValue(self.o_lst_sessions.GetSelectedRow(), 1) != '':
            # prendo il numero della sessione
            v_session_id = self.o_lst_sessions.GetValue(self.o_lst_sessions.GetSelectedRow(), 1)
            v_file_name = os.path.join(self.o_preferenze.work_dir, 'session_information.sql')
            v_file = open( v_file_name, 'w')            
            try:
                # connessione al DB come amministratore
                v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                                 password=self.o_preferenze.v_oracle_password_sys,
                                                 dsn=self.e_server_name.GetString(self.e_server_name.GetSelection()),
                                                 mode=cx_Oracle.SYSDBA)
                v_ok = True
            except:
                wx.MessageBox(message='Connection to oracle rejected. Please control login information.', caption='Error', style=wx.OK|wx.ICON_ERROR)
                v_ok = False
        
            if v_ok:
                # apro cursore
                v_cursor = v_connection.cursor()            
        
                # select per la ricerca dei cursori aperti e relativo sql
                v_select = "SELECT sql_text FROM v$sql WHERE hash_value IN (SELECT hash_value FROM v$open_cursor WHERE SID=" + str(v_session_id) + ") GROUP BY sql_text"                
        
                v_cursor.execute(v_select)        
                for result in v_cursor:
                    # scrivo i risultati nel file
                    v_file.write( result[0] + '\n')
        
                v_cursor.close()
                v_connection.close()            

            v_file.close()           
            wx.MessageBox(message=v_file_name + ' created', caption='Sql', style=wx.OK|wx.ICON_INFORMATION)

    def on_click_cerca_sessioni(self, event):
        """
            visualizza tutte le sessioni o solo quelle di un particolare utente
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.GetString(self.e_server_name.GetSelection()),
                                             mode=cx_Oracle.SYSDBA)
            v_ok = True
        except:
            wx.MessageBox(message='Connection to oracle rejected. Please control login information.', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        if v_ok:
            # apro cursori
            v_cursor = v_connection.cursor()
            v_user = ""

            # ricerca parziale su nome utente
            if self.e_user_name.GetValue() != '':
                v_user += " AND Upper(USERNAME) LIKE '%" + self.e_user_name.GetValue().upper() + "%' "            
                            
            # ricerca parziale su nome programma
            if self.e_program_name.GetValue() != '':
                v_user += " AND Upper(MODULE) LIKE '%" + self.e_program_name.GetValue().upper() + "%' "
                                                
            # ricerca parziale su nome terminale
            if self.e_terminal.GetValue() != '':
                v_user += " AND Upper(TERMINAL) LIKE '%" + self.e_terminal.GetValue().upper() + "%' "
            

            # select per la ricerca degli oggetti invalidi
            v_select = "SELECT ROWNUM,    \n\
                               SID,       \n\
                               SERIAL#,   \n\
                               TERMINAL,  \n\
                               USERNAME,  \n\
                               DECODE((SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,TERMINAL,NULL,'I','I') FROM DUAL),NULL,(SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,USERNAME,NULL,'I','I') FROM DUAL),(SELECT DESCRIZIONE('MS_UTN','NOME_DE','LOGIN_CO',NULL,NULL,TERMINAL,NULL,'I','I') FROM DUAL)) COGNOME_NOME, \n\
                               STATUS STATO, \n\
                               MODULE PROGRAMMA, \n\
                               PROG_DE DESCRIZIONE, \n\
                               ACTION AZIONE, \n\
                               LOGON_TIME \n\
                        FROM   V$SESSION,(SELECT PROG_CO, PROG_DE FROM ML_PROG WHERE LNG_CO = 'I') ML_PROG \n\
                        WHERE  USERNAME NOT IN ('SYS','SYSTEM','DBSNMP') AND MODULE = PROG_CO(+) \n\
                        " + v_user + "ORDER BY ROWNUM"

            v_cursor.execute(v_select)
            # pulisce la lista di eventuali valori precedenti
            self.o_lst_sessions.DeleteAllItems()

            for result in v_cursor:
                # visualizzo output nell'area di testo (le funzioni rjust e ljust inserisco a destra o sinistra degli spazi)
                self.o_lst_sessions.AppendItem( ( result[0], result[1], str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6]), str(result[7]), str(result[8]), str(result[9]), str(result[10]) ) )

            v_cursor.close()
            v_connection.close()

    def on_click_kill_sessione(self, event):
        """
            killa la sessione selezionata nell'elenco dei blocchi di sessione
        """
        if self.o_lst_sessions.GetItemCount() > 0 and self.o_lst_sessions.GetValue(self.o_lst_sessions.GetSelectedRow(), 1) != '':
            killa_sessione(self.o_lst_sessions.GetValue(self.o_lst_sessions.GetSelectedRow(), 1), # colonna 1 della riga
                           self.o_lst_sessions.GetValue(self.o_lst_sessions.GetSelectedRow(), 2), # colonna 2 della riga
                           self.o_preferenze.v_oracle_user_sys,
                           self.o_preferenze.v_oracle_password_sys,
                           self.e_server_name.GetString( self.e_server_name.GetSelection() ) )

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
    test = oracle_sessions(o_window_base, modalita_test=True)

    app.MainLoop()
