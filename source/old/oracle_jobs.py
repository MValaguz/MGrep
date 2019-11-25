# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 18/09/2018
 Descrizione...: Programma per controllare i job di sistema
"""

#Librerie grafiche
import wx
#import wx.dataview
import wx.grid
import wx.lib.agw.pybusyinfo as PBI
#Librerie oracle
import cx_Oracle
#Librerie interne smigrep
from test_app import Test_App
from preferenze import preferenze
from utilita import pathname_icons

class oracle_jobs:
    """
        Programma per controllare lo stato dei job schedulati a sistema
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
            if 'OraJobsStatus' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))             
          
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"Oracle jobs", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon(pathname_icons()+ 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # selezione del server
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"Oracle name server:", wx.DefaultPosition, wx.DefaultSize, 0 )        
        self.e_server_name = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('ICOM_815','BACKUP_815','BACKUP_2_815'))        
        self.e_server_name.SetSelection(0)
        
        # selezione colonna di ordinamento
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, u"Order by column:", wx.DefaultPosition, wx.DefaultSize, 0 )        
        self.e_order_by = wx.Choice(self.panel, id=wx.ID_ANY, choices = ('Job name','Comments','Job action','Last start date','Next run date','Last status','Additional info'))        
        self.e_order_by.SetSelection(5)        
        
        # selezione per autosize sul contenuto della griglia
        self.c_autosize = wx.CheckBox( self.panel, wx.ID_ANY, u"Results auto size", wx.DefaultPosition, wx.DefaultSize, 0 )

        # elenco job        
        self.b_load_job_list = wx.BitmapButton(self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )        
        self.b_load_job_list.SetToolTip("Load scheduler job list")

        # collego gli eventi agli oggetti
        self.c_autosize.Bind( wx.EVT_CHECKBOX, self.on_click_autosize )                        
        self.b_load_job_list.Bind( wx.EVT_BUTTON, self.on_click_load_job_list )                        
                        
        ###########################################
        # creo la griglia che contiene i risultati
        ###########################################
        self.o_lst_job = wx.grid.Grid(self.panel, -1, size=(400,100) )
        
        # creo le colonne nella griglia
        self.o_lst_job.CreateGrid(0, 7)        
        self.o_lst_job.SetColLabelValue(0, 'Job name')                
        self.o_lst_job.SetColSize(0, 230)
        self.o_lst_job.SetColLabelValue(1, 'Comments')                
        self.o_lst_job.SetColSize(1, 250)
        self.o_lst_job.SetColLabelValue(2, 'Job action')                
        self.o_lst_job.SetColSize(2, 100)
        self.o_lst_job.SetColLabelValue(3, 'Last start date')                
        self.o_lst_job.SetColSize(3, 120)
        self.o_lst_job.SetColLabelValue(4, 'Next run date')                
        self.o_lst_job.SetColSize(4, 120)
        self.o_lst_job.SetColLabelValue(5, 'Last status')                
        self.o_lst_job.SetColSize(5, 100)
        self.o_lst_job.SetColLabelValue(6, 'Additional info')                
        self.o_lst_job.SetColSize(6, 200)
        
        self.o_lst_job.EnableDragGridSize( True )
        self.o_lst_job.EnableDragRowSize( True )        
        self.o_lst_job.EnableDragColMove( True )
        self.o_lst_job.EnableDragColSize( True )                        
        ###########################################

        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # sizer con titolo e combobox
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.Add( self.l_titolo1,        wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )
        gbSizer1.Add( self.e_server_name,    wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )        
        gbSizer1.Add( self.l_titolo2,        wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )        
        gbSizer1.Add( self.e_order_by,       wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )                
        gbSizer1.Add( self.c_autosize,       wx.GBPosition( 0, 9 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )                
        gbSizer1.Add( self.b_load_job_list,  wx.GBPosition( 0, 25), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL, 5 )        

        # sizer job list
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )        
                
        gbSizer2.Add( self.o_lst_job,  wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.AddGrowableCol(0)
        gbSizer2.AddGrowableRow(0)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer1, 1, wx.ALL, 5 )
        bSizer_padre.Add( gbSizer2, 100, wx.ALL | wx.EXPAND, 5 )
        
        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()
        
    def on_click_autosize(self, event):
        """
            imposta autosize sulla griglia dei risultati
        """
        if self.c_autosize.GetValue()==1:
            self.o_lst_job.AutoSize()     
            
        self.panel.Layout()
        self.panel.Show()        
                        
    def on_click_load_job_list(self, event):
        """
            visualizza elenco dei job per il database indicato
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
            wait_win = PBI.PyBusyInfo(message="Please wait a moment...", parent=None, title="Loading")
            
            # apro cursori
            v_cursor = v_connection.cursor()            

            # select per la ricerca degli oggetti invalidi
            v_order_by = 0
            v_order_by = self.e_order_by.GetSelection() + 1                                        
            v_select = """SELECT JOB_NAME, 
                                 COMMENTS,                                
                                 JOB_ACTION, 
                                 TO_CHAR(LAST_START_DATE,'DD/MM/YYYY HH24:MI:SS') LAST_START_DATE,
                                 TO_CHAR(NEXT_RUN_DATE,'DD/MM/YYYY HH24:MI:SS') NEXT_RUN_DATE, 
                                 (SELECT STATUS
                                  FROM   ALL_SCHEDULER_JOB_RUN_DETAILS 
                                  WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME
                                     AND ALL_SCHEDULER_JOB_RUN_DETAILS.LOG_DATE=(SELECT Max(LOG_DATE)
                                                                                 FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                                                                                 WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME)
                                 ) LAST_STATUS,
                                 (SELECT ADDITIONAL_INFO
                                  FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                                  WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME
                                     AND ALL_SCHEDULER_JOB_RUN_DETAILS.LOG_DATE=(SELECT Max(LOG_DATE)
                                                                                 FROM   ALL_SCHEDULER_JOB_RUN_DETAILS
                                                                                 WHERE  ALL_SCHEDULER_JOB_RUN_DETAILS.JOB_NAME=ALL_SCHEDULER_JOBS.JOB_NAME)
                                 ) ADDITIONAL_INFO
                          FROM   ALL_SCHEDULER_JOBS 
                          WHERE  ENABLED='TRUE'
                          ORDER BY """ + str(v_order_by)
            v_cursor.execute(v_select)
            # pulisce la lista di eventuali valori precedenti            
            if self.o_lst_job.GetNumberRows() > 0:
                self.o_lst_job.DeleteRows(pos=0, numRows=self.o_lst_job.GetNumberRows() )

            v_riga = 0
            for result in v_cursor:
                # carico la riga nella lista
                self.o_lst_job.AppendRows(1)
                self.o_lst_job.SetCellValue(v_riga, 0, str(result[0]) )
                self.o_lst_job.SetCellValue(v_riga, 1, str(result[1]) )
                self.o_lst_job.SetCellValue(v_riga, 2, str(result[2]) )
                self.o_lst_job.SetCellValue(v_riga, 3, str(result[3]) )
                self.o_lst_job.SetCellValue(v_riga, 4, str(result[4]) )
                self.o_lst_job.SetCellValue(v_riga, 5, str(result[5]) )
                self.o_lst_job.SetCellValue(v_riga, 6, str(result[6]) )
                if str(result[5]) == 'FAILED':
                    self.o_lst_job.SetCellBackgroundColour(v_riga, 5, wx.RED)
                    
                v_riga += 1

            v_cursor.close()
            v_connection.close()
            
            del wait_win            
            
            # rinfresco la griglia (se richiesto indico che vanno calcolate in automatico l'altezza e la larghezza delle celle
            self.on_click_autosize(None)

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
    test = oracle_jobs(o_window_base, modalita_test=True)

    app.MainLoop()
