# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 07/08/2018
 Descrizione...: Programma di utilità per import e export dei dati tra DB Oracle, DB SQLite e Excel
"""

#Librerie grafiche
import wx
#Librerie interne SmiGrep
from preferenze import preferenze
from test_app import Test_App 
from utilita import pathname_icons
from utilita_database import estrae_elenco_tabelle_oracle
from utilita_database import estrae_elenco_tabelle_sqlite
from copy_from_oracle_to_sqlite import copy_from_oracle_to_sqlite
from utilita_database import estrae_elenco_tabelle_sqlite
from export_from_sqlite_to_excel import export_from_sqlite_to_excel
from copy_from_sqlite_to_oracle import copy_from_sqlite_to_oracle
from import_excel_into_oracle import import_excel_into_oracle
from convert_csv_to_excel import convert_csv_to_excel
from convert_csv_to_excel import convert_csv_clipboard_to_excel
from view_sqlite_table import view_sqlite_table

class tools_import_export:
    """
        Frame che contiene il nome del DB Oracle e il nome del DB SQLite
    """
    def __init__(self, o_window_base, modalita_test):
        # imposto pathname delle icone-immagini
        self.modalita_test=modalita_test
        self.o_window_base=o_window_base
        
        # carico le preferenze
        self.o_preferenze = preferenze()
        self.o_preferenze.carica()        
        
        # creo la finestra come figlia della finestra di partenza 
        win_pos = (0,0)
        win_size = (780,510)        
        my_window = wx.MDIChildFrame(o_window_base, -1, u"Import-Export tools 'to' and 'from' a database Oracle, SQLite e Excel", size=win_size,pos=win_pos)    
        
        # creo un pannello contenitore
        self.panel = wx.Panel(my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")   
        
        # creo una toolbar con i dati generali
        tb = my_window.CreateToolBar( wx.TB_FLAT|wx.TB_TEXT )        
        tb.AddTool(10, "Save", wx.Bitmap( pathname_icons() + "disk.gif", wx.BITMAP_TYPE_ANY ), u"Save the data in order to be retrieved at the next start of SmiGrep" )
        tb.AddSeparator()
        
        self.l_dboracle = wx.StaticText( tb, wx.ID_ANY, u"Oracle connection:", wx.DefaultPosition, wx.DefaultSize, 0 )
        tb.AddControl(self.l_dboracle)        
        self.e_dboracle = wx.TextCtrl( tb, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        tb.AddControl(self.e_dboracle)
        tb.AddSeparator()
        
        self.l_sqlite_db = wx.StaticText( tb, wx.ID_ANY, u"SQLite DB:", wx.DefaultPosition, wx.DefaultSize, 0 )
        tb.AddControl(self.l_sqlite_db)
        self.e_sqlite_db = wx.TextCtrl( tb, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )
        tb.AddControl(self.e_sqlite_db)
        self.b_pathname = wx.BitmapButton( tb, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'folder.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        tb.AddControl(self.b_pathname)
        
        tb.Realize()        
        
        # definisco un font in grassetto per fare i titoli
        my_font = wx.Font()        
        my_font.SetWeight(wx.FONTWEIGHT_BOLD)
                                            
        # titolo1
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u'Copy an Oracle table into a SQLite DB:', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.l_titolo1.SetFont(my_font)
        self.l_table_name = wx.StaticText( self.panel, wx.ID_ANY, u'Table Name', wx.DefaultPosition, wx.DefaultSize, 0 )        
        self.e_table_name = wx.ComboBox( self.panel, wx.ID_ANY, "", wx.DefaultPosition , (200,-1 ), [], 0 )

        self.l_where_cond = wx.StaticText( self.panel, wx.ID_ANY, u'Where Condition', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_where_cond = wx.TextCtrl( self.panel, wx.ID_ANY, value='', size=(200,50), style=wx.TE_MULTILINE)                

        self.b_copy_to_sqlite = wx.Button( self.panel, wx.ID_ANY, 'Start copy table from' + chr(10) + 'Oracle DB to SQLite DB', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_copy_to_sqlite.SetBitmap( wx.Bitmap( pathname_icons() + "go.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_copy_to_sqlite.SetToolTip( "The specified table is copied from the Oracle DB to the SQlite DB. If the SQLite DB does not exist, it is automatically created." )        
        
        # titolo2
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, 'SQLite table utility:', wx.DefaultPosition, wx.DefaultSize, 0 )        
        self.l_titolo2.SetFont(my_font)
        
        self.l_table_excel = wx.StaticText( self.panel, wx.ID_ANY, 'Table name', wx.DefaultPosition, wx.DefaultSize, 0 )                        
        self.e_table_excel = wx.ComboBox( self.panel, wx.ID_ANY, "", wx.DefaultPosition , (200,-1 ), [], 0 )        
        
        self.l_excel_file = wx.StaticText( self.panel, wx.ID_ANY, 'Destination file', wx.DefaultPosition, wx.DefaultSize, 0 )                        
        self.e_excel_file = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )        
        self.b_excel_file = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'folder.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )        
        
        self.b_view_table = wx.Button( self.panel, wx.ID_ANY, 'View Table', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_view_table.SetBitmap( wx.Bitmap( pathname_icons() + "table.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_view_table.SetToolTip( "The table shown in the SQLite DB is displayed! Caution! This operation may take a long time!" )        
        
        self.b_start_excel = wx.Button( self.panel, wx.ID_ANY, 'Export to Excel', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_start_excel.SetBitmap( wx.Bitmap( pathname_icons() + "excel.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_start_excel.SetToolTip( "The table shown in the SQLite DB is exported to an Excel format file" )                                
            
        # titolo3
        self.l_titolo4 = wx.StaticText( self.panel, wx.ID_ANY, 'Copy a SQLite table or Excel file, into an Oracle table:', wx.DefaultPosition, wx.DefaultSize, 0 )                        
        self.l_titolo4.SetFont(my_font)
                
        self.l_table_to_oracle = wx.StaticText( self.panel, wx.ID_ANY, 'SQLite table name', wx.DefaultPosition, wx.DefaultSize, 0 )                                        
        self.e_table_to_oracle = wx.ComboBox( self.panel, wx.ID_ANY, "", wx.DefaultPosition , (200,-1 ), [], 0 )                
            
        self.l_import_excel = wx.StaticText( self.panel, wx.ID_ANY, 'Excel file', wx.DefaultPosition, wx.DefaultSize, 0 )                                        
        self.e_import_excel = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )        
        self.b_import_excel = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'folder.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )        
    
        self.l_oracle_table = wx.StaticText( self.panel, wx.ID_ANY, 'Destination table', wx.DefaultPosition, wx.DefaultSize, 0 )                                                
        self.e_oracle_table = wx.ComboBox( self.panel, wx.ID_ANY, "", wx.DefaultPosition , (200,-1 ), [], 0 )        
        
        self.b_copy_to_oracle = wx.Button( self.panel, wx.ID_ANY, 'Start copy table from' + chr(10) + 'SQLite DB to Oracle DB', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_copy_to_oracle.SetBitmap( wx.Bitmap( pathname_icons() + "go.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_copy_to_oracle.SetToolTip( "The table shown in the SQLite DB is copied to the Oracle table. The Oracle table must not exist!" )                                
                                                          
        self.b_start_import_excel = wx.Button( self.panel, wx.ID_ANY, 'Import Excel file into Oracle table', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_start_import_excel.SetBitmap( wx.Bitmap( pathname_icons() + "csv.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_start_import_excel.SetToolTip( "The indicated Excel file is copied to an Oracle table. The destination table must not exist!" )                                  
        
        # titolo4
        self.l_titolo5 = wx.StaticText( self.panel, wx.ID_ANY, 'Convert a CSV file format in Excel file format:', wx.DefaultPosition, wx.DefaultSize, 0 )                                        
        self.l_titolo5.SetFont(my_font)

        self.l_csv_file  = wx.StaticText( self.panel, wx.ID_ANY, 'CSV file', wx.DefaultPosition, wx.DefaultSize, 0 )                                        
        self.e_csv_file = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 200,-1 ) )                        
        self.b_csv_file = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'folder.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
    
        self.l_csv_separator = wx.StaticText( self.panel, wx.ID_ANY, 'CSV separator', wx.DefaultPosition, wx.DefaultSize, 0 )                                                
        self.e_csv_separator = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size( 20,-1 ) )                
        
        self.b_start_csv_to_excel = wx.Button( self.panel, wx.ID_ANY, 'CSV file format to Excel format', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_start_csv_to_excel.SetBitmap( wx.Bitmap( pathname_icons() + "excel.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_start_csv_to_excel.SetToolTip( "Convert the CSV file to Excel format. The result is stored in the same folder as the original file!" )                                  
    
        self.b_start_clip_to_excel = wx.Button( self.panel, wx.ID_ANY, 'Text Clipboard to Excel format', wx.DefaultPosition, wx.DefaultSize, 0 )
        self.b_start_clip_to_excel.SetBitmap( wx.Bitmap( pathname_icons() + "clipboard.gif", wx.BITMAP_TYPE_ANY ) )
        self.b_start_clip_to_excel.SetToolTip( "Convert clipboard contents to Excel format! In the clipboard must be present text formatted with indicated field separator!" )                                  

        # collego gli eventi agli oggetti 
        tb.Bind(wx.EVT_TOOL, self.salva_preferenze , id=10)        
        self.b_pathname.Bind( wx.EVT_BUTTON, self.folder_dialog )
        self.e_table_name.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_drop_down_combo_table_name)
        self.e_table_name.Bind(wx.EVT_TEXT, self.on_text_combo_table_name)
        self.e_table_excel.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_drop_down_combo_table_excel)
        self.b_import_excel.Bind(wx.EVT_BUTTON, self.b_import_excel_folder_dialog )
        self.e_table_to_oracle.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_drop_down_combo_e_table_to_oracle)        
        self.e_oracle_table.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.on_drop_down_combo_e_oracle_table)        
        self.b_excel_file.Bind( wx.EVT_BUTTON, self.b_excel_file_folder_dialog )
        self.b_csv_file.Bind( wx.EVT_BUTTON, self.b_csv_file_folder_dialog )
        self.b_start_clip_to_excel.Bind(wx.EVT_BUTTON, self.converte_clipboard_to_excel)
        self.b_copy_to_sqlite.Bind(wx.EVT_BUTTON, self.avvia_copy_from_oracle_to_sqlite)        
        self.b_start_excel.Bind(wx.EVT_BUTTON, self.avvia_export_from_sqlite_to_excel)
        self.b_copy_to_oracle.Bind(wx.EVT_BUTTON, self.avvia_copy_from_sqlite_to_oracle)
        self.b_start_import_excel.Bind(wx.EVT_BUTTON, self.avvia_import_excel_to_oracle)
        self.b_start_csv_to_excel.Bind(wx.EVT_BUTTON, self.converte_csv_to_excel)
        self.b_view_table.Bind(wx.EVT_BUTTON, self.visualizza_tabella_sqlite)
        
        # imposto i valori ricevuti come preferiti
        self.e_dboracle.SetValue( self.o_preferenze.dboracle )
        self.e_sqlite_db.SetValue( self.o_preferenze.sqlite_db )
        self.e_where_cond.SetValue( self.o_preferenze.where_cond )
        self.e_table_name.SetValue( self.o_preferenze.table_name )
        self.e_table_excel.SetValue( self.o_preferenze.table_excel )
        self.e_excel_file.SetValue( self.o_preferenze.excel_file )
        self.e_table_to_oracle.SetValue( self.o_preferenze.table_to_oracle )
        self.e_import_excel.SetValue( self.o_preferenze.import_excel )
        self.e_oracle_table.SetValue( self.o_preferenze.oracle_table )
        self.e_csv_file.SetValue( self.o_preferenze.csv_file )
        self.e_csv_separator.SetValue( self.o_preferenze.csv_separator )

        ###
        # Impaginazione degli elementi
        ###

        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # box figlio
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        # titolo1
        gbSizer1.Add( self.l_titolo1,            wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 10 ), wx.ALL, 1 )
        gbSizer1.Add( self.l_table_name,         wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.e_table_name,         wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )        
        gbSizer1.Add( self.l_where_cond,         wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_where_cond,         wx.GBPosition( 2, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.b_copy_to_sqlite,     wx.GBPosition( 2, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 ) 
        
        # titolo2
        gbSizer1.Add( self.l_titolo2,            wx.GBPosition( 4, 0 ), wx.GBSpan( 1, 10 ), wx.ALL, 1 )         
        gbSizer1.Add( self.l_table_excel,        wx.GBPosition( 5, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_table_excel,        wx.GBPosition( 5, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )         
        gbSizer1.Add( self.l_excel_file,         wx.GBPosition( 6, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_excel_file,         wx.GBPosition( 6, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )         
        gbSizer1.Add( self.b_excel_file,         wx.GBPosition( 6, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )         
        gbSizer1.Add( self.b_view_table,         wx.GBPosition( 5, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 )                         
        gbSizer1.Add( self.b_start_excel,        wx.GBPosition( 6, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 ) 
        
        # titolo3
        gbSizer1.Add( self.l_titolo4,            wx.GBPosition( 8, 0 ), wx.GBSpan( 1, 10 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.l_table_to_oracle,    wx.GBPosition( 9, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_table_to_oracle,    wx.GBPosition( 9, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )             
        gbSizer1.Add( self.l_import_excel,       wx.GBPosition(10, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_import_excel,       wx.GBPosition(10, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.b_import_excel,       wx.GBPosition(10, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.l_oracle_table,       wx.GBPosition(11, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_oracle_table,       wx.GBPosition(11, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.b_copy_to_oracle,     wx.GBPosition( 9, 4 ), wx.GBSpan( 2, 1 ), wx.EXPAND, 1 )                                                           
        gbSizer1.Add( self.b_start_import_excel, wx.GBPosition(11, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 ) 
        
        # titolo4
        gbSizer1.Add( self.l_titolo5,            wx.GBPosition(13, 0 ), wx.GBSpan( 1, 10 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.l_csv_file,           wx.GBPosition(14, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_csv_file,           wx.GBPosition(14, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )                 
        gbSizer1.Add( self.b_csv_file,           wx.GBPosition(14, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.l_csv_separator,      wx.GBPosition(15, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 ) 
        gbSizer1.Add( self.e_csv_separator,      wx.GBPosition(15, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )         
        gbSizer1.Add( self.b_start_csv_to_excel, wx.GBPosition(14, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 )         
        gbSizer1.Add( self.b_start_clip_to_excel,wx.GBPosition(15, 4 ), wx.GBSpan( 1, 1 ), wx.EXPAND, 1 ) 
                        
        # inserisco il figlio dentro il padre
        bSizer_padre.Add( gbSizer1, 1, wx.ALL | wx.EXPAND, 10 )

        # inserisco il sizer dentro il pannello
        self.panel.SetSizer( bSizer_padre)        
        self.panel.Layout()
        
    def salva_preferenze(self, event):
        self.o_preferenze.dboracle = self.e_dboracle.GetValue()
        self.o_preferenze.sqlite_db = self.e_sqlite_db.GetValue()
        self.o_preferenze.where_cond = self.e_where_cond.GetValue()
        self.o_preferenze.table_name = self.e_table_name.GetValue()
        self.o_preferenze.table_excel = self.e_table_excel.GetValue()
        self.o_preferenze.excel_file = self.e_excel_file.GetValue()
        self.o_preferenze.table_to_oracle = self.e_table_to_oracle.GetValue()
        self.o_preferenze.import_excel = self.e_import_excel.GetValue()
        self.o_preferenze.oracle_table = self.e_oracle_table.GetValue()
        self.o_preferenze.csv_file = self.e_csv_file.GetValue()
        self.o_preferenze.csv_separator = self.e_csv_separator.GetValue()
        
        self.o_preferenze.salva()
        
        wx.MessageBox(message='Preferences was saved', caption='Save', style=wx.OK|wx.ICON_INFORMATION)
        
    def visualizza_tabella_sqlite(self, event):
        """
            esegue la procedura che visualizza il contenuto di una tabella SQLite
        """
        v_ok = True
        if self.e_sqlite_db.GetValue() == '':
            wx.MessageBox(message='Please enter a SQLite DB', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_table_excel.GetValue() == '':
            wx.MessageBox(message='Please enter a Table Name', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # Richiamo export della tabella in excel
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            app = view_sqlite_table(self.o_window_base,
                                    self.e_table_excel.GetValue(),
                                    self.e_sqlite_db.GetValue(),
                                    self.modalita_test)    
            
    def converte_csv_to_excel(self, event):
        """
            esegue la procedura che converte un file CSV in un file di Excel
        """
        v_ok = True
        if self.e_csv_file.GetValue() == '':
            wx.MessageBox(message='Please enter a CSV file name', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_csv_separator.get() == '':
            wx.MessageBox(message='Please enter a CSV separator', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # Richiamo export della tabella in excel
        if v_ok:
            app = convert_csv_to_excel(self.e_csv_file.GetValue(),
                                       self.e_csv_separator.GetValue(),
                                       self.modalita_test)    
    
    def avvia_import_excel_to_oracle(self, event):
        """
            esegue la procedura che importa un file di excel dentro una tabella Oracle
        """
        v_ok = True
        if self.e_dboracle.GetValue() == '':
            wx.MessageBox(message='Please enter a Oracle connection', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_import_excel.GetValue() == '':
            wx.MessageBox(message='Please enter a Excel source file', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_oracle_table.GetValue() == '':
            wx.MessageBox(message='Please enter a destination Table', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # Richiamo copia della tabella
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            v_oracle_con = self.e_dboracle.GetValue()
            v_oracle_con = v_oracle_con.replace('/','@')
            v_oracle_con_result = v_oracle_con.split('@')
            app = import_excel_into_oracle(False,
                                           v_oracle_con_result[0],
                                           v_oracle_con_result[1],
                                           v_oracle_con_result[2],
                                           self.e_oracle_table.GetValue(),
                                           self.e_import_excel.GetValue(),
                                           self.modalita_test)
    
    def avvia_copy_from_sqlite_to_oracle(self, event):
        """
            esegue la procedura che copia una tabella di SQLite in DB Oracle
        """
        v_ok = True
        if self.e_dboracle.GetValue() == '':
            wx.MessageBox(message='Please enter a Oracle connection', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_sqlite_db.GetValue() == '':
            wx.MessageBox(message='Please enter a SQLite DB destination', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_table_to_oracle.GetValue() == '':
            wx.MessageBox(message='Please enter a source SQLite Table', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_oracle_table.GetValue() == '':
            wx.MessageBox(message='Please enter a destination Table', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # Richiamo copia della tabella
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            v_oracle_con = self.e_dboracle.GetValue()
            v_oracle_con = v_oracle_con.replace('/','@')
            v_oracle_con_result = v_oracle_con.split('@')
            app = copy_from_sqlite_to_oracle(self.e_table_to_oracle.GetValue(),
                                             self.e_sqlite_db.GetValue(),
                                             self.o_preferenze.work_dir,
                                             v_oracle_con_result[0],
                                             v_oracle_con_result[1],
                                             v_oracle_con_result[2],
                                             self.e_oracle_table.GetValue(),
                                             self.modalita_test)
    
    def avvia_export_from_sqlite_to_excel(self, event):
        """
            esegue la procedura che esporta una tabella SQLite dentro un file di excel
        """
        v_ok = True
        if self.e_sqlite_db.GetValue() == '':
            wx.MessageBox(message='Please enter a SQLite DB', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_table_excel.GetValue() == '':
            wx.MessageBox(message='Please enter a Table Name', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False
        if self.e_excel_file.GetValue() == '':
            wx.MessageBox(message='Please enter a Destination file', caption='Error', style=wx.OK|wx.ICON_ERROR)
            v_ok = False

        # Richiamo export della tabella in excel
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            app = export_from_sqlite_to_excel(self.e_table_excel.GetValue(),
                                              self.e_sqlite_db.GetValue(),
                                              self.e_excel_file.GetValue(),
                                              self.modalita_test)
    
    def avvia_copy_from_oracle_to_sqlite(self, event):
        """
            esegue la procedura che copia una tabella di Oracle dentro un DB di SQLite
        """
        v_ok = True
        if self.e_dboracle.GetValue() == '':
            wx.MessageBox(message='Please enter a Oracle connection', caption='Error',style=wx.OK|wx.ICON_INFORMATION)            
            v_ok = False
        if self.e_sqlite_db.GetValue() == '':
            wx.MessageBox(message='Please enter a SQLite DB destination', caption='Error', style=wx.OK|wx.ICON_INFORMATION)
            v_ok = False
        if self.e_table_name.GetValue() == '':
            wx.MessageBox(message='Please enter a Table Name', caption='Error', style=wx.OK|wx.ICON_INFORMATION)
            v_ok = False

        # Richiamo copia della tabella
        if v_ok:
            # Scompongo la stringa di connessione in nome utente, password e indirizzo del server
            v_oracle_con = self.e_dboracle.GetValue()
            v_oracle_con = v_oracle_con.replace('/','@')
            v_oracle_con_result = v_oracle_con.split('@')
            app = copy_from_oracle_to_sqlite(v_oracle_con_result[0],
                                             v_oracle_con_result[1],
                                             v_oracle_con_result[2],
                                             self.e_table_name.GetValue(),
                                             self.e_where_cond.GetValue(), #Mettere None se non si passa alcun parametro!
                                             self.e_sqlite_db.GetValue(),
                                             self.o_preferenze.work_dir,
                                             self.modalita_test)            
            
    def folder_dialog(self, event):
        """
            apre la finestra di dialogo per selezionare un file
        """
        dlg = wx.FileDialog(self.panel, "Choose a SQLite file:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.e_sqlite_db.SetValue( dlg.GetPath() )
        dlg.Destroy()
        
    def b_excel_file_folder_dialog(self, event):
        """
            apre la finestra di dialogo per selezionare un file
        """
        dlg = wx.FileDialog(self.panel, "Choose a xlsx destination file:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.e_excel_file.SetValue( dlg.GetPath() )
        dlg.Destroy()        
            
    def b_csv_file_folder_dialog(self, event):
        """
            apre la finestra di dialogo per selezionare un file
        """
        dlg = wx.FileDialog(self.panel, "Choose a CSV file:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.e_csv_file.SetValue( dlg.GetPath() )
        dlg.Destroy()        
        
    def b_import_excel_folder_dialog(self, event):
        """
            apre la finestra di dialogo per selezionare un file
        """
        dlg = wx.FileDialog(self.panel, message="Choose a Excel file:",wildcard = "Excel XLSX |*.xlsx", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.e_import_excel.SetValue( dlg.GetPath() )
        dlg.Destroy()                
        
    def on_drop_down_combo_table_name(self, event):
        """
            carica la combobox delle tabelle di oracle SMILE
        """
        self.e_table_name.Clear()
        v_oracle_con = self.e_dboracle.GetValue()
        v_oracle_con = v_oracle_con.replace('/','@')
        v_oracle_con_result = v_oracle_con.split('@')        
        self.e_table_name.Append( estrae_elenco_tabelle_oracle( '1', v_oracle_con_result[0], v_oracle_con_result[1], v_oracle_con_result[2] ) )    

    def on_drop_down_combo_e_table_to_oracle(self, event):
        """
            carica la combobox tabelle per export in excel
        """
        if self.e_sqlite_db.GetValue() != '':
            self.e_table_to_oracle.Clear()
            self.e_table_to_oracle.Append( estrae_elenco_tabelle_sqlite('1', self.e_sqlite_db.GetValue()) )    
        
    def on_text_combo_table_name(self, event):        
        """
            rende maiuscolo il contenuto del campo di inserimento dato, mentre si scrive
        """
        value = self.e_table_name.GetValue().upper()
        self.e_table_name.ChangeValue(value)
        self.e_table_name.SetSelection(len(value), len(value))  
        
    def on_drop_down_combo_e_oracle_table(self, event):
        """
            carica la combobox delle tabelle di oracle SMILE
        """
        self.e_oracle_table.Clear()
        v_oracle_con = self.e_dboracle.GetValue()
        v_oracle_con = v_oracle_con.replace('/','@')
        v_oracle_con_result = v_oracle_con.split('@')        
        self.e_oracle_table.Append( estrae_elenco_tabelle_oracle( '1', v_oracle_con_result[0], v_oracle_con_result[1], v_oracle_con_result[2] ) )            
        
    def on_drop_down_combo_table_excel(self, event):
        """
            carica la combobox tabelle per export in excel
        """
        if self.e_sqlite_db.GetValue() != '':
            self.e_table_excel.Clear()
            self.e_table_excel.Append( estrae_elenco_tabelle_sqlite('1', self.e_sqlite_db.GetValue()) )
            
    def converte_clipboard_to_excel(self, event):
        """
          prende il contenuto degli appunti e
          lo converte in file excel
        """
        app = convert_csv_clipboard_to_excel(self.o_preferenze.work_dir, 
                                             self.e_csv_separator.GetValue(),
                                             self.modalita_test)        
        
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    # finestra di base madre di tutte le finestre
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)
                
    ###
    # test 
    ###
    test = tools_import_export(o_window_base, modalita_test=True)
        
    app.MainLoop()
