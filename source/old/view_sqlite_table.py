# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 10/10/2018
 Descrizione...: Scopo del programma è visualizzare il contenuto di una tabella SQLite
"""
#Librerie di data base
import sqlite3 
#Importa librerie grafiche
import wx
import wx.dataview
import wx.lib.agw.pybusyinfo as PBI
#Import dei moduli interni
from utilita_database import estrae_struttura_tabella_sqlite
from test_app import Test_App
from utilita import pathname_icons

class view_sqlite_table:
    """
        Visualizza il contenuto di una tabella SQLite
        Va indicato attraverso l'instanziazione della classe:
            p_table_name     = Nome della tabella SQLite da esportare            
            p_sqlite_db_name = Nome del DB SQLite            
    """
    def __init__(self,
                 o_window_base,
                 p_table_name,
                 p_sqlite_db_name,
                 p_modalita_test):
        
        # creo la finestra come figlia della finestra di partenza (la posizione e la dimensione vengono lette dalla preferenze)
        win_pos = (0,0)
        win_size = (780,510)
        my_window = wx.MDIChildFrame(o_window_base, -1, u"View SQLite table", size=win_size, pos=win_pos)
        my_window.SetIcon(wx.Icon( pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        panel = wx.Panel(my_window, wx.ID_ANY)
        panel.SetBackgroundColour("WHITE")
        
        ####
        #Apro il DB sqlite    
        ####
        v_sqlite_conn = sqlite3.connect(database=p_sqlite_db_name)
        #Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = bytes
        v_sqlite_cur = v_sqlite_conn.cursor()                
        #Carico struttura della tabella
        elenco_colonne = estrae_struttura_tabella_sqlite('1', v_sqlite_cur, p_table_name)                         
        
        # definizione del widget che visualizza la tabella
        lista_db = wx.dataview.DataViewListCtrl( panel, id=wx.ID_ANY, pos=wx.DefaultPosition,  size=win_size, style = wx.dataview.DV_HORIZ_RULES)
        # aggiunta delle colonne in base alla struttura della tabella (la prima colonna contiene il numero di riga)        
        for colonna in elenco_colonne:            
            lista_db.AppendTextColumn(label=colonna, width=wx.COL_WIDTH_AUTOSIZE, flags=wx.COL_SORTABLE|wx.COL_RESIZABLE)
                        
        # Finestra di wait mentre si caricano i dati
        wait_win = PBI.PyBusyInfo(message="Please wait a moment...", parent=None, title="Loading data")
        
        ####
        #Carico la tabella                
        ####
        #Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
        v_sqlite_conn.text_factory = str
        v_sqlite_cur = v_sqlite_conn.cursor()        
        #Lettura del contenuto della tabella    
        query = estrae_struttura_tabella_sqlite('s', v_sqlite_cur, p_table_name)         
        v_sqlite_cur.execute(query)
        rows = v_sqlite_cur.fetchall()    
        v_sqlite_conn.close()                             
        i = 0
        for record in rows:
            lista_db.AppendItem(record)        
            # aggiorno la wait window con il numero di record caricati
            i += 1
            if i % 10000 == 0:
                wait_win = PBI.PyBusyInfo(message="Please wait a moment..." + str(i), parent=None, title="Loading data")
                    
        # Impaginazione degli elementi                
        bSizer = wx.BoxSizer( wx.VERTICAL )
        bSizer.Add( lista_db, 1, wx.ALL | wx.EXPAND)        
        panel.SetSizer( bSizer)
        panel.Layout()
        my_window.Show()                
        
        del wait_win         

# Eseguo test
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    test = view_sqlite_table(o_window_base,
                             'OC_ORTES',
                             'C:\SmiGrep\SmiGrepTransfer.db',
                             True)    
    app.MainLoop()