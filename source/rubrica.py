# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 29/03/2018
 Descrizione...: Apre una finestra con lettura e ricerca rubrica aziendale
"""

#Librerie di data base
import  cx_Oracle
#Librerie grafiche
import  wx
import  wx.dataview
#Librerie interne SmiGrep
from test_app import Test_App
from utilita import pathname_icons

class rubrica:
    """
        Apre una finestra visualizzando la rubrica aziendale
        Va indicato attraverso l'instanziazione della classe:
           tipo_rubrica  = T=Telefonica, E=Email
    """
    def __init__(self, o_window_base, tipo_rubrica, modalita_test):
        self.tipo_rubrica = tipo_rubrica

        # creo la finestra come figlia della finestra di partenza
        p_win = wx.MDIChildFrame(o_window_base, -1, u"Book", size=(780,510),pos=(0,0))
        p_win.SetIcon(wx.Icon( pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        self.panel = wx.Panel(p_win, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # definizione dei widget
        self.l_ricerca = wx.StaticText( self.panel, wx.ID_ANY, u"Search:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_ricerca = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TE_PROCESS_ENTER)
        self.b_ricerca = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )

        # definizione del widget lista risultati
        self.lista_db = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        if self.tipo_rubrica == "T":
            self.lista_db.AppendTextColumn(label='Azienda', width=wx.COL_WIDTH_AUTOSIZE, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Dipendente', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Telefono', width=wx.COL_WIDTH_AUTOSIZE, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Reparto', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Email', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Mansione', width=250, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        else:
            self.lista_db.AppendTextColumn(label='Azienda', width=100, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Dipendente', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Email', width=wx.COL_WIDTH_AUTOSIZE, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Reparto', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
            self.lista_db.AppendTextColumn(label='Mansione', width=170, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        # collego gli eventi agli oggetti (pulsante di ricerca e tasto enter sulla campo ricerca)
        self.b_ricerca.Bind( wx.EVT_BUTTON, self.imposta_lista )
        self.e_ricerca.Bind( wx.EVT_TEXT_ENTER, self.imposta_lista )

        # caricamento iniziale della lista
        self.imposta_lista(None)

        # visualizzazione del risultato
        bSizer_padre   = wx.BoxSizer( wx.VERTICAL )

        wSizer_figlio1 = wx.WrapSizer( wx.HORIZONTAL )
        bSizer_figlio2 = wx.BoxSizer( wx.VERTICAL )

        bSizer_padre.Add( wSizer_figlio1, 0, wx.ALL, 5 )
        bSizer_padre.Add( bSizer_figlio2, 1, wx.ALL | wx.EXPAND, 5 )

        wSizer_figlio1.Add( self.l_ricerca, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        wSizer_figlio1.Add( self.e_ricerca, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        wSizer_figlio1.Add( self.b_ricerca, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        # il valore 1 alla proporzione indica che deve espandersi anche verticalmente
        bSizer_figlio2.Add( self.lista_db, 1, wx.ALL|wx.EXPAND, 5 )

        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

        #p_win.Maximize()

    def load_rubrica(self):
        """
            restituisce una lista con i risultati della ricerca
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user='SMILE', password='SMILE', dsn='ICOM_815')
        except:
            wx.MessageBox(message='Connection to oracle rejected!', caption='Error', style=wx.OK | wx.ICON_ERROR)
            return 'Error'

        # apro cursori
        v_cursor = v_connection.cursor()

        # select per la ricerca degli oggetti invalidi
        if self.e_ricerca.GetLineText(0) != '':
            v_where_ricerca = "AND UPPER(AZIDP_DE || DIPEN_DE || CONTT_CO || REP_DE || EMAIL_DE || MANSIO_DE) LIKE UPPER('%" + self.e_ricerca.GetLineText(0).replace(' ','%') + "%')"
        else:
            v_where_ricerca = ''

        # definizione della select (per rubrica telefonica)
        if self.tipo_rubrica == 'T':
            v_cursor.execute("SELECT AZIDP_DE, DIPEN_DE, CONTT_CO, REP_DE, EMAIL_DE, MANSIO_DE FROM VA_RUBRI WHERE CATEG_CO='" +  self.tipo_rubrica + "'" + v_where_ricerca + " ORDER BY AZIDP_DE")
        # o per rubrica email
        else:
            v_cursor.execute("SELECT AZIDP_DE, DIPEN_DE, CONTT_CO, REP_DE,  MANSIO_DE FROM VA_RUBRI WHERE CATEG_CO='" +  self.tipo_rubrica + "'" + v_where_ricerca + " ORDER BY AZIDP_DE")

        # carico tutte le righe in una lista
        v_row = v_cursor.fetchall()

        # chiudo la connessione
        v_cursor.close()
        v_connection.close()

        # restituisco le righe lette
        return v_row

    def imposta_lista(self, event):
        # pulisco la lista a video
        self.lista_db.DeleteAllItems()

        # leggo la tabella da db
        tree_data = self.load_rubrica()

        # carico la lista a video (viene fatta la conversione in stringa in quanto andava in crash il programma
        # ... credo per problemi sul contenuto dei dati
        rec_to_stringa = []
        for record in tree_data:
            if self.tipo_rubrica == "T":
                rec_to_stringa = (str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[4]), str(record[5]))
            else:
                rec_to_stringa = (str(record[0]), str(record[1]), str(record[2]), str(record[3]), str(record[4]))
            self.lista_db.AppendItem(rec_to_stringa)

# ----------------------------------------
# TESTING APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    # valori ammessi T=Telefono, E=Email
    test = rubrica(o_window_base, tipo_rubrica="T", modalita_test=True)

    app.MainLoop()
