# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 26/03/2018
 Descrizione...: Scopo del programma è prendere un file CSV e convertirlo nel rispettivo formato di Excel

 Modificato da.: Marco Valaguzza
 Data..........: 25/07/2018
 Motivo........: Inserita conversione automatica delle celle numeriche (attenzione! Non conversione di colonne ma di celle!)
"""
#Librerie di sistema
import  os
#Librerie grafiche
import  wx
#Libreria per export in excel
from    xlsxwriter.workbook import Workbook
#Librerie interne SmiGrep
from utilita import pathname_icons

def check_campo_numerico(valore):
    v_ok = True
    try:
        numero = float(valore.replace(',','.'))
    except:
        v_ok = False
    return v_ok

def campo_numerico(valore):
    return float(valore.replace(',','.'))

class convert_csv_to_excel:
    """
        Converte file csv in formato excel
        Va indicato attraverso l'instanziazione della classe:
            p_csv_file  = Nome del file csv
            p_separator = Carattere di separatore dei campi
    """
    def __init__(self,
                 p_csv_name,
                 p_csv_separator,
                 p_modalita_test):

        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.Frame(None, title = u"Convert CSV file format in Excel file format", size=(400,120))
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
        
        #Spezzo il nome del file per ricavare il nome di destinazione e controllo che la destinazione non esista
        v_solo_nome_file = os.path.split(p_csv_name)[1]
        v_solo_directory = os.path.split(p_csv_name)[0]
        v_solo_nome_file_senza_suffisso = os.path.splitext(v_solo_nome_file)[0]
        v_suffisso_nome_file = os.path.splitext(v_solo_nome_file)[1]
        v_xls_name = v_solo_directory + '//' + v_solo_nome_file_senza_suffisso + '.xlsx'
        if os.path.isfile(v_xls_name):
            if wx.MessageBox(message="Destination file already exists. Do you to replace it?", caption='Notice', style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
                self.my_window.SetFocus()
            else:
                # esco dalla procedura perché utente ha deciso di non preseguire
                return None

        #Apro il file e conto le righe
        v_total_rows = 0
        with open(p_csv_name, encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_total_rows += 1

        #Calcolo l'1% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100
        self.label_1.SetLabel( 'Total records number...' + str(v_total_rows) )
        self.panel.Layout()
        self.panel.Update()

        #Creazione del file excel
        workbook = Workbook(v_xls_name)
        worksheet = workbook.add_worksheet()

        #Rileggo il file e converto da un formato all'altro
        v_progress = 0
        v_y = 0
        with open(p_csv_name,  encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_valori = v_line.split(p_csv_separator)
                v_x = 0
                for campo in v_valori:
                    if check_campo_numerico(campo):
                        worksheet.write(v_y, v_x, campo_numerico(campo))
                    else:
                        worksheet.write(v_y, v_x, campo)
                    v_x += 1
                v_y += 1
                #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
                if v_total_rows > 100:
                    v_progress += 1
                    if v_progress % v_rif_percent == 0:
                        self.gauge_1.SetValue( (v_progress*100//v_total_rows)+1 )
                        self.label_2.SetValue( 'Converting...' + str((v_progress*100//v_total_rows)+1) + '%' )
                        self.panel.Layout()
                        self.panel.Update()

        #Chiusura del file e del db
        self.label_2.SetLabel('Finalizing process...')
        self.panel.Layout()
        self.panel.Update()
        workbook.close()
        #Messaggio finale
        wx.MessageBox(message='File conversion completed!', caption='Info', style=wx.OK|wx.ICON_INFORMATION)

        self.my_window.Close()
        return None

class convert_csv_clipboard_to_excel:
    """
        Converte il testo contenuto nella clipboard (appunti) nel formato di excel
        Va indicato attraverso l'instanziazione della classe:
            p_work_dir = Directory di lavoro
            p_separator = Carattere di separatore dei campi
    """
    def __init__(self,
                 p_work_dir,
                 p_csv_separator,
                 p_modalita_test):

        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.Frame(None, title = u"Convert clipboard to Excel", size=(400,120))
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

        # nome file di lavoro
        v_nome_file_di_lavoro = p_work_dir + '\\clipboard.csv'

        # definizione del file di destinazione (apertura della finestra di dialogo e richiesta del file di arrivo)
        #v_xls_name = p_work_dir + '\\clipboard.xlsx'        
        dlg = wx.FileDialog(self.panel, message="Save a Excel file",wildcard = "Excel XLSX |*.xlsx", style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            v_xls_name = dlg.GetPath()
        else:
            wx.MessageBox(message="Not a valid file name is selected", caption='Error', style=wx.OK|wx.ICON_ERROR)
            return None            
        dlg.Destroy()                                
            
        #Forzo il fuoco sulla window
        self.my_window.SetFocus()

        ###############################################
        # lettura della clipboard e scrittura in file
        ###############################################
        import ctypes

        CF_TEXT = 1

        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            file = open(v_nome_file_di_lavoro, 'wb')
            file.write(text.value)
            file.close()
            kernel32.GlobalUnlock(data_locked)
        else:
            wx.MessageBox(message="Clipboard not contains csv format text", caption='Error', style=wx.OK|wx.ICON_ERROR)
            return None

        user32.CloseClipboard()
        ########################################

        #Apro il file e conto le righe
        v_total_rows = 0
        with open(v_nome_file_di_lavoro, encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_total_rows += 1

        #Calcolo l'1% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100
        self.label_2.SetLabel('Total records number...' + str(v_total_rows))
        self.panel.Layout()
        self.panel.Update()

        #Creazione del file excel
        workbook = Workbook(v_xls_name)
        worksheet = workbook.add_worksheet()

        #Rileggo il file e converto da un formato all'altro
        v_progress = 0
        v_y = 0
        with open(v_nome_file_di_lavoro,  encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_valori = v_line.split(p_csv_separator)
                v_x = 0
                for campo in v_valori:
                    if check_campo_numerico(campo):
                        worksheet.write(v_y, v_x, campo_numerico(campo))
                    else:
                        worksheet.write(v_y, v_x, campo)
                    v_x += 1
                v_y += 1
                #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
                if v_total_rows > 100:
                    v_progress += 1
                    if v_progress % v_rif_percent == 0:
                        self.gauge_1.SetValue( (v_progress*100//v_total_rows)+1 )
                        self.label_2.SetLabel( 'Converting...' + str((v_progress*100//v_total_rows)+1) + '%' )
                        self.panel.Layout()
                        self.panel.Update()

        #Chiusura del file e del db
        self.label_2.SetLabel('Finalizing process...')
        self.panel.Layout()
        self.panel.Update()
        workbook.close()
        #Messaggio finale
        wx.MessageBox(message='File ' + v_xls_name + ' created!', caption='Info', style=wx.OK|wx.ICON_INFORMATION)

        #Il file di lavoro viene eliminatao
        os.remove(os.path.join(v_nome_file_di_lavoro))
 
        self.my_window.Close()
        return None

# Eseguo applicazione d'esempio se non richiamato da altro programma
if __name__ == "__main__":
    app = wx.App()
    """
    app = convert_csv_to_excel("C:/Users/mvalaguz/Desktop/Script1.csv",
                               "|",
                               True)
    """
    app = convert_csv_clipboard_to_excel("C:/Users/mvalaguz/Desktop/",
                                         "|",
                                         True)
