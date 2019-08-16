# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 03/01/2019
 Descrizione...: Programma per controllare le dimensioni delle tabelle di database di SMILE
"""

#Librerie grafiche
import wx
import wx.dataview
import wx.lib.agw.piectrl as PC
#Librerie oracle
import cx_Oracle
#Librerie di sistema
import os
# Libreria per la corretta formattazione dei numeri
import locale
#Librerie interne smigrep
from test_app import Test_App
from preferenze import preferenze
from utilita import pathname_icons

class oracle_size:
    """
        Programma per controllare le dimensioni delle tabelle schema SMILE
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
            if 'OraSize' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))             
                  
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Oracle tables size", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon( pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # selezione del server
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"Oracle name server:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_server_name = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('ICOM_815','BACKUP_815','BACKUP_2_815'))
        self.e_server_name.SetSelection(0)

        # lista delle sessioni
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, u"Table name:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_table_name = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ), wx.TE_PROCESS_ENTER)
        
        self.b_go = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "go.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_go.SetToolTip("Search the specific table. It is not case sensitive and accept partial strings.")
        
        self.o_lst_sessions = wx.dataview.DataViewListCtrl( self.panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=wx.Size( 100,100 ), style = wx.dataview.DV_HORIZ_RULES)
        self.o_lst_sessions.AppendTextColumn(label='Table Name', width=200, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
        self.o_lst_sessions.AppendTextColumn(label='MegaByte', width=100, align=wx.ALIGN_RIGHT, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)

        self.l_titolo3 = wx.StaticText( self.panel, wx.ID_ANY, u"Total size in MegaByte:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_total_size_mb = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ))
        self.l_titolo4 = wx.StaticText( self.panel, wx.ID_ANY, u"Total size in GigaByte:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_total_size_gb = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ))        
        self.l_titolo5 = wx.StaticText( self.panel, wx.ID_ANY, u"Total size in TeraByte:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_total_size_tb = wx.StaticText( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 150,-1 ))                
        self.l_note = wx.StaticText( self.panel, wx.ID_ANY, u"Note: Table size also includes the size of related indexes", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        # collego gli eventi agli oggetti
        self.b_go.Bind( wx.EVT_BUTTON, self.on_click_cerca_size_table )
        self.e_table_name.Bind( wx.EVT_TEXT_ENTER, self.on_click_cerca_size_table )
        
        # creo il grafico a torta
        self.grafico = PC.PieCtrl( self.panel, -1, wx.DefaultPosition, wx.Size(350,350) )                                
        self.grafico.GetLegend().SetTransparent(True)
        self.grafico.GetLegend().SetWindowStyle(wx.STATIC_BORDER)        
        self.grafico.SetShowEdges(True)            
        self.grafico.SetAngle(25/180.0*3.14)        
        self.grafico.GetLegend().SetLabelFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
                                                           wx.FONTSTYLE_NORMAL,
                                                           wx.FONTWEIGHT_NORMAL,
                                                           False, "Arial"))        
        self.grafico.SetHeight(10)
        self.grafico.GetLegend().SetPosition(wx.Point(0,0))                
        
        # carico un primo valore fittizio nel grafico
        part = PC.PiePart()
        part.SetLabel('Table name')
        part.SetValue(100)
        part.SetColour(wx.Colour(255,0,0))
        self.grafico._series.append(part)
        
        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )
        
        # sizer
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
        gbSizer1.Add( self.l_titolo1,              wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_server_name,          wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_titolo2,              wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_table_name,           wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_go,                   wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.o_lst_sessions,         wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 3 ), wx.ALL|wx.EXPAND, 1 )        
        gbSizer1.Add( self.l_titolo3,              wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_total_size_mb,        wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )        
        gbSizer1.Add( self.l_titolo4,              wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_total_size_gb,        wx.GBPosition( 3, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )                
        gbSizer1.Add( self.l_titolo5,              wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_total_size_tb,        wx.GBPosition( 4, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )                                
        gbSizer1.Add( self.l_note,                 wx.GBPosition( 4, 2 ), wx.GBSpan( 1, 3 ), wx.ALL, 1 )                                
        gbSizer1.Add( self.grafico,                wx.GBPosition( 1, 3 ), wx.GBSpan( 1, 2 ), wx.ALIGN_CENTER, 1 )                                
        
        gbSizer1.AddGrowableCol(4)
        gbSizer1.AddGrowableRow(1)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer1, -1, wx.ALL | wx.EXPAND, 5 )        

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

        # mi posiziono sul campo nome utente
        self.e_table_name.SetFocus()
        
    def on_click_cerca_size_table(self, event):
        """
            visualizza la dimensione delle tabelle 
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
            v_table = ""

            # ricerca parziale su nome utente
            if self.e_table_name.GetValue() != '':
                v_table += " AND Upper(table_name) LIKE '%" + self.e_table_name.GetValue().upper() + "%' "            
                            
            # select per la ricerca degli oggetti invalidi
            v_select = '''SELECT table_name, 
                                 sum(bytes)/1024/1024 MB
                          FROM   (SELECT segment_name table_name, owner, bytes
                                  FROM   dba_segments
                                  WHERE  segment_type = 'TABLE'
                                  
                                  UNION  ALL
                                  
                                  SELECT i.table_name, i.owner, s.bytes
                                  FROM   dba_indexes i, 
                                         dba_segments s
                                  WHERE  s.segment_name = i.index_name
                                    AND  s.owner = i.owner
                                    AND  s.segment_type = 'INDEX'
                                  
                                  UNION ALL
                               
                                  SELECT l.table_name, l.owner, s.bytes
                                  FROM   dba_lobs l, 
                                         dba_segments s
                                  WHERE  s.segment_name = l.segment_name
                                    AND  s.owner = l.owner
                                    AND  s.segment_type = 'LOBSEGMENT'
                                  
                                  UNION ALL
                          
                                  SELECT l.table_name, l.owner, s.bytes
                                  FROM   dba_lobs l, 
                                         dba_segments s
                                  WHERE  s.segment_name = l.index_name
                                    AND  s.owner = l.owner
                                    AND  s.segment_type = 'LOBINDEX')
                                  
                          WHERE owner = UPPER('SMILE')
                            AND table_name NOT LIKE '%$%'
                       ''' + v_table + '''     
                          GROUP BY table_name, owner
                          ORDER BY SUM(bytes) desc 
                       '''

            v_cursor.execute(v_select)
            # pulisce la lista di eventuali valori precedenti
            self.o_lst_sessions.DeleteAllItems()

            v_total_size = 0
            locale.setlocale(locale.LC_ALL, 'ita')
            v_prime_10_tabelle = 1            
            # pulisco il contenuto del grafico (max 10 elementi)
            self.grafico._series.clear()
            v_colori = [(255,0,0), (255,255,0), (128,255,0), (0,255,255), (0,128,255), (255,0,128), (255,128,0), (128,128,0), (0,128,0), (128,0,0)]
            v_other_size = 0
            for result in v_cursor:
                # visualizzo output nell'area di testo (le funzioni rjust e ljust inserisco a destra o sinistra degli spazi)
                v_size = result[1]
                v_total_size += v_size
                # converto il numero in stringa con separatori migliaglia e decimali (viene utilizzata la libreria locale poco sopra inizializzata)
                #v_size_fmt = '{:0,.2f}'.format(v_size)
                v_size_fmt = locale.format_string('%.2f', v_size, grouping=True)
                self.o_lst_sessions.AppendItem( ( result[0], v_size_fmt ) )
                # nel grafico a torta carico solo le prime 10 tabelle
                if v_prime_10_tabelle < 10:                    
                    part = PC.PiePart()
                    part.SetLabel( result[0] )                    
                    part.SetValue( v_size )                    
                    part.SetColour( wx.Colour(v_colori[v_prime_10_tabelle-1]) )                    
                    self.grafico._series.append(part)                    
                    v_prime_10_tabelle += 1                    
                else:
                    v_other_size += v_size
                    
            # aggiungo se calcolata la 10 fetta 
            if v_other_size > 0:
                part = PC.PiePart()
                part.SetLabel( 'Other' )                    
                part.SetValue( v_other_size )                    
                part.SetColour( wx.Colour(v_colori[9]) )                    
                self.grafico._series.append(part)                                    

            # imposta il totale 
            self.l_total_size_mb.SetLabel( locale.format_string('%.2f', v_total_size, grouping=True) )
            self.l_total_size_gb.SetLabel( locale.format_string('%.2f', v_total_size/1024, grouping=True) )
            self.l_total_size_tb.SetLabel( locale.format_string('%.2f', v_total_size/1024/1024, grouping=True) )
            
            v_cursor.close()
            v_connection.close()
            
            # rinfresco il pannello per ridisegnare il grafico                        
            self.grafico.Refresh()            

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    ###
    # test 
    ###
    test = oracle_size(o_window_base, modalita_test=True)

    app.MainLoop()
