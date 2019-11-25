# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 27/07/2018
 Descrizione...: Programma per controllare gli oggetti bloccati a sistema
"""

#Librerie grafiche
import wx
import wx.dataview
#Librerie oracle
import cx_Oracle
#Librerie interne smigrep
from test_app import Test_App
from preferenze import preferenze
from utilita_database import estrae_elenco_tabelle_oracle
from utilita_database import killa_sessione
from utilita import pathname_icons

class oracle_locks:
    """
        Programma per controllare gli oggetti bloccati a sistema
    """
    def __init__(self, o_window_base, modalita_test):

        self.o_window_base = o_window_base
        self.modalita_test = modalita_test
            
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        
        
        # creo la finestra come figlia della finestra di partenza (la posizione e la dimensione vengono lette dalla preferenze)
        win_pos = (0,0)
        win_size = (780,510)
        for my_window_pos in self.o_preferenze.l_windows_pos:
            if 'OraLocks' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))             
                  
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Oracle locks", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon(pathname_icons()+ 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # selezione del server
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"Oracle name server:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_server_name = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('ICOM_815','BACKUP_815','BACKUP_2_815'))
        self.e_server_name.SetSelection(0)

        # lock di sessione
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, u"Check sessions lock:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_session_lock = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_session_lock.SetToolTip("Search lock session")

        self.b_kill_session_lock = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'kill.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_kill_session_lock.SetToolTip("Kill the selected session")

        self.o_lst_session_lock = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        self.o_lst_session_lock.AppendTextColumn(label='Sid', width=70, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Serial Nr.', width=60, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Username', width=70, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Terminal', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Referent', width=120, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Phone', width=50, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Location', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Program', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_session_lock.AppendTextColumn(label='Object Name', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        # lock di tabella
        self.l_titolo3 = wx.StaticText( self.panel, wx.ID_ANY, "Check table lock:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_table_name = wx.StaticText( self.panel, wx.ID_ANY, "Table Name" , wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_table_name = wx.ComboBox( self.panel, wx.ID_ANY, "", wx.DefaultPosition , (200,-1 ), [], 0 )
        self.b_table_lock = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_table_lock.SetToolTip("Search lock table")
        self.b_kill_table_lock = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'kill.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_kill_table_lock.SetToolTip("Kill the selected session")
        self.o_lst_table_lock = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        self.o_lst_table_lock.AppendTextColumn(label='Sid', width=70, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Serial Nr.', width=70, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Username', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Status', width=80, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Os User', width=140, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Machine', width=150, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_table_lock.AppendTextColumn(label='Program', width=160, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        # collego gli eventi agli oggetti
        self.b_session_lock.Bind( wx.EVT_BUTTON, self.on_click_sessioni_di_blocco )
        self.b_kill_session_lock.Bind( wx.EVT_BUTTON, self.on_click_kill_sessioni_di_blocco )
        self.e_table_name.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_drop_down_combo_tabelle)
        self.b_table_lock.Bind( wx.EVT_BUTTON, self.on_click_blocco_tabella)
        self.b_kill_table_lock.Bind( wx.EVT_BUTTON, self.on_click_kill_blocco_tabella )

        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # sizer con titolo e combobox
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer1.Add( self.l_titolo1,      wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_server_name, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )

        # sizer lock sessioni
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer2.Add( self.l_titolo2,           wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 1 )
        gbSizer2.Add( self.b_session_lock,      wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.b_kill_session_lock, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.o_lst_session_lock,  wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.AddGrowableCol(1)
        gbSizer2.AddGrowableRow(1)

        # sizer lock tabelle
        gbSizer3 = wx.GridBagSizer( 0, 0 )
        gbSizer3.SetFlexibleDirection( wx.BOTH )
        gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer3.Add( self.l_titolo3,         wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer3.Add( self.l_table_name,      wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )
        gbSizer3.Add( self.e_table_name,      wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 1 )
        gbSizer3.Add( self.b_table_lock,      wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 1 )
        gbSizer3.Add( self.b_kill_table_lock, wx.GBPosition( 1, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer3.Add( self.o_lst_table_lock,  wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 5 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer3.AddGrowableCol(3)
        gbSizer3.AddGrowableRow(2)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer1, 1, wx.ALL, 5 )
        bSizer_padre.Add( gbSizer2, 100, wx.ALL | wx.EXPAND, 5 )
        bSizer_padre.Add( gbSizer3, 100, wx.ALL | wx.EXPAND, 5 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

    def on_click_sessioni_di_blocco(self, event):
        """
            visualizza le sessioni di blocco del sistema di produzione ICOM_815
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.GetString(self.e_server_name.GetSelection()),
                                             mode=cx_Oracle.SYSDBA)
            v_error = False
        except:
            wx.MessageBox( message='Connection to oracle rejected. Please control login information.', caption='Error', style=wx.OK|wx.ICON_INFORMATION )
            v_error = True

        if not v_error:
            # apro cursori
            v_cursor = v_connection.cursor()

            # select per la ricerca degli oggetti bloccati
            v_select = "WITH sessions AS \n\
                        (SELECT sid, serial#, blocking_session, P2, row_wait_obj#, sql_id, username,terminal,program \n\
                         FROM v$session) \n\
                         SELECT DECODE(LEVEL,1,'', LPAD(' ', LEVEL*2)) || sid sid,  serial#, username,terminal,program, object_name \n\
                         FROM (SELECT sid, serial#, blocking_session, P2, row_wait_obj#, sql_id, username,terminal,program \n\
                               FROM v$session) s \n\
                         LEFT OUTER JOIN dba_objects \n\
                         ON (object_id = row_wait_obj#) \n\
                         WHERE sid IN (SELECT blocking_session FROM sessions) \n\
                         OR blocking_session IS NOT NULL \n\
                        CONNECT BY PRIOR sid = blocking_session \n\
                        START WITH blocking_session IS NULL"
            v_cursor.execute(v_select)
            # pulisce la lista di eventuali valori precedenti
            self.o_lst_session_lock.DeleteAllItems()

            for result in v_cursor:
                # ricerco il posizionamento del PC in termini di locazione e referente
                v_location = ''
                v_referent = ''
                v_phone    = ''
                v_ricerca_sql = v_connection.cursor()
                # campo di ricerca (nome pc o nome utente)
                if str(result[3]) == '':
                    v_utente = str(result[2])
                else:
                    v_utente = str(result[3])

                v_ricerca_sql.execute("""SELECT HW_DISPO.NOME_DE, 
                                              HW_DISPO.DISLO_DE,  
                                              CP_DIPEN.DIPEN_DE,  
                                              VA_RUBRICA.TELIN_NU   
                                       FROM   SMILE.HW_DISPO,     
                                              SMILE.MA_CESPH,     
                                              SMILE.CP_DIPEN,     
                                              SMILE.VA_RUBRICA    
                                       WHERE  UPPER(HW_DISPO.NOME_DE) LIKE '%""" + v_utente + """%'  AND 
                                              MA_CESPH.AZIEN_CO = HW_DISPO.AZIEN_CO AND 
                                              MA_CESPH.MATRI_CO = HW_DISPO.MATRI_CO AND  
                                              MA_CESPH.UTAZI_CO = CP_DIPEN.AZIEN_CO AND  
                                              MA_CESPH.UTMAT_CO = CP_DIPEN.DIPEN_CO AND  
                                              VA_RUBRICA.AZIEN_CO = CP_DIPEN.AZIEN_CO AND 
                                              VA_RUBRICA.DIPEN_CO = CP_DIPEN.DIPEN_CO""")
                
                for campi in v_ricerca_sql:
                    if v_location == '':
                        v_location = campi[1]
                    if v_referent == '':
                        v_referent = campi[2]
                    if v_phone == '':
                        v_phone    = campi[3]
                # carico la riga nella lista
                self.o_lst_session_lock.AppendItem((str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(v_referent), str(v_phone), str(v_location), str(result[4]), str(result[5])))

            v_cursor.close()
            v_connection.close()

    def on_click_blocco_tabella(self, event):
        """
            visualizza le sessioni che bloccano una specifica tabella sul server ICOM_815
        """
        v_ok = True
        if self.e_table_name.GetValue() == '':
            wx.MessageBox(message='Please insert a Oracle table name', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        if v_ok:
            try:
                # connessione al DB come amministratore
                v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                                 password=self.o_preferenze.v_oracle_password_sys,
                                                 dsn=self.e_server_name.GetString( self.e_server_name.GetSelection() ),
                                                 mode=cx_Oracle.SYSDBA)
                v_ok = True
            except:
                wx.MessageBox(message='Connection to oracle rejected. Please control login information.', caption='Error', style=wx.OK|wx.ERROR)
                v_ok = False

        if v_ok:
            # apro cursori
            v_cursor = v_connection.cursor()

            # select per la ricerca degli oggetti invalidi
            v_select = "SELECT v$lock.SID, v$session.SERIAL#, V$SESSION.USERNAME, \n\
                               V$SESSION.STATUS, V$SESSION.OSUSER, V$SESSION.MACHINE, \n\
                               V$SESSION.PROGRAM||'.'||V$SESSION.MODULE \n\
                        FROM v$lock, v$session \n\
                        WHERE id1 = (SELECT object_id \n\
                                     FROM   all_objects \n\
                                     WHERE  owner ='SMILE' AND \n\
                                            object_name = RTRIM(LTRIM(UPPER('" + self.e_table_name.GetValue() + "')))) AND \n\
                              v$lock.sid=v$session.sid"
            v_cursor.execute(v_select)
            # pulisce la lista di eventuali valori precedenti
            self.o_lst_table_lock.DeleteAllItems()

            for result in v_cursor:
                # visualizzo output nell'area di testo (le funzioni rjust e ljust inserisco a destra o sinistra degli spazi)
                self.o_lst_table_lock.AppendItem((str(result[0]), str(result[1]), str(result[2]), str(result[3]), str(result[4]), str(result[5]), str(result[6])))

            v_cursor.close()
            v_connection.close()

    def on_drop_down_combo_tabelle(self, event):
        """
            carica la combobox delle tabelle di oracle SMILE
        """
        self.e_table_name.Clear()
        self.e_table_name.Append( estrae_elenco_tabelle_oracle( '1','SMILE','SMILE',self.e_server_name.GetString(self.e_server_name.GetSelection()) ) )

    def on_click_kill_sessioni_di_blocco(self, event):
        """
            killa la sessione selezionata nell'elenco dei blocchi di sessione
        """
        if self.o_lst_session_lock.GetItemCount() > 0 and self.o_lst_session_lock.GetValue(self.o_lst_session_lock.GetSelectedRow(), 0) != '':
            killa_sessione(self.o_lst_session_lock.GetValue(self.o_lst_session_lock.GetSelectedRow(), 0), # colonna 0 della riga
                           self.o_lst_session_lock.GetValue(self.o_lst_session_lock.GetSelectedRow(), 1), # colonna 1 della riga
                           self.o_preferenze.v_oracle_user_sys,
                           self.o_preferenze.v_oracle_password_sys,
                           self.e_server_name.GetString( self.e_server_name.GetSelection() ) )

    def on_click_kill_blocco_tabella(self, event):
        """
            killa la sessione selezionata nell'elenco dei blocchi di tabella
        """
        if self.o_lst_table_lock.GetItemCount() > 0 and self.o_lst_table_lock.GetValue(self.o_lst_table_lock.GetSelectedRow(), 0) != '':
            killa_sessione(self.o_lst_table_lock.GetValue(self.o_lst_table_lock.GetSelectedRow(), 0), # colonna 0 della riga
                           self.o_lst_table_lock.GetValue(self.o_lst_table_lock.GetSelectedRow(), 1), # colonna 1 della riga
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
    test = oracle_locks(o_window_base, modalita_test=True)

    app.MainLoop()
