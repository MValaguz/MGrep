# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 16/08/2018
 Descrizione...: Scopo del programma è prendere una tabella di SQLite ed esportala in un file Excel
"""
#Librerie di data base
import sqlite3 
#Librerie di sistema
import os
#Librerie grafiche
import  wx
#Libreria per export in excel
from    xlsxwriter.workbook import Workbook
#Import dei moduli interni
from utilita_database import estrae_struttura_tabella_sqlite
from utilita import pathname_icons

class export_from_sqlite_to_excel:
    """
        Esporta una tabella SQLite in un file Excel
        Va indicato attraverso l'instanziazione della classe:
            p_table_name     = Nome della tabella SQLite da esportare            
            p_sqlite_db_name = Nome del DB SQLite
            p_excel_file     = Nome del file di Excel (il nome deve essere comprensivo di pathname)
    """
    def __init__(self, 
                 p_table_name,                 
                 p_sqlite_db_name,
                 p_excel_file,
                 p_modalita_test):
        
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.Frame(None, title = u"Export SQLite table to Excel", size=(400,120))
        self.my_window.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        self.label_1 = wx.StaticText(self.panel, wx.ID_ANY, "...")
        self.gauge_1 = wx.Gauge(self.panel, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.label_2 = wx.StaticText(self.panel, wx.ID_ANY, "...")

        # creo il layout
        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer1.Add( self.label_1, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 2 )
        gbSizer1.Add( self.gauge_1, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 2 )
        gbSizer1.Add( self.label_2, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER|wx.ALL, 2 )
        gbSizer1.AddGrowableCol(0)
        bSizer1.Add( gbSizer1, 1, wx.ALL|wx.EXPAND, 10 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer1 )
        self.my_window.Centre(wx.BOTH)
        self.my_window.SetFocus()
        self.my_window.Show()    
        
        ###############################
        #Avvio la copia della tabella  
        ###############################      
        
        #Apre il DB sqlite (lo apro in modalità classica....non dovrei avere problemi con utf-8)
        v_sqlite_conn = sqlite3.connect(database=p_sqlite_db_name)
        v_sqlite_cur = v_sqlite_conn.cursor()        
                
        #Conta dei record della tabella (serve unicamente per visualizzare la progress bar)
        query = 'SELECT COUNT(*) FROM ' + p_table_name
        try:
            v_sqlite_cur.execute(query)
        except:
            wx.MessageBox(message="Table in SQLite DB not exists!", caption="Error", style=wx.OK|wx.ICON_ERROR)           
            #esco
            return None
        
        v_total_rows = 0
        for row in v_sqlite_cur:                  
            v_total_rows = row[0]
        #Calcolo il 10% che rappresenta lo spostamento della progress bar        
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100        
        self.label_1.SetLabel('Total records number to export...' + str(v_total_rows))
        self.panel.Layout()
        self.panel.Update()
                
        #Creazione del file excel
        workbook = Workbook(p_excel_file)
        worksheet = workbook.add_worksheet()
        
        #Estraggo elenco dei campi
        v_struttura = estrae_struttura_tabella_sqlite('1',v_sqlite_cur,p_table_name)
        
        #Carico elenco dei campi nella prima riga del foglio        
        pos = 0
        for i in v_struttura:
            worksheet.write(0, pos, i)
            pos += 1

        #Carico tutte le altri righe della tabella                
        v_progress = 0        
        query = 'SELECT * FROM ' + p_table_name        
        v_sqlite_cur.execute(query)
        for i, row in enumerate(v_sqlite_cur):            
            for j, value in enumerate(row):
                worksheet.write(i+1, j, row[j])        
            #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
            if v_total_rows > 100:
                v_progress += 1
                if v_progress % v_rif_percent == 0:                
                    self.gauge_1.SetValue( (v_progress*100//v_total_rows)+1 )
                    self.label_2.SetLabel( 'Exporting...' + str((v_progress*100//v_total_rows)+1) + '%' )
                    self.panel.Layout()
                    self.panel.Update()
                
        #Chiusura del file e del db
        self.label_2.SetLabel('Finalizing process...')
        self.panel.Layout()
        self.panel.Update()
        
        workbook.close()
        v_sqlite_conn.close()                    
        #Messaggio finale        
        wx.MessageBox(message='Table export completed!', caption='Info', style=wx.OK | wx.ICON_INFORMATION)
        
        self.my_window.Close()
        return None                

# Eseguo applicazione d'esempio se non richiamato da altro programma
if __name__ == "__main__":    
    app = wx.App()
    app = export_from_sqlite_to_excel("TA_FILES",                                      
                                      "C:\SmiGrep\SmiGrepTransfer.db",
                                      "C:\SmiGrep\Export.xlsx",
                                      True)      
