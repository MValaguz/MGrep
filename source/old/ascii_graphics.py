# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 06/11/2019
 Descrizione...: Dato un testo, lo converte in big text
"""

# Libreria di sistema
import os
#Librerie per convertire caratteri ascii in big text
import pyfiglet 
#Librerie grafiche
import  wx
#Librerie interne SmiGrep
from test_app import Test_App
from utilita import pathname_icons
from utilita import file_in_directory

class ascii_to_graphics(wx.ScrolledWindow):
    """
        Apre una finestra dove richiede un testo e lo trasforma in big text
    """
    def __init__( self, o_window_base, modalita_test):
        # creo la finestra come figlia della finestra di partenza
        p_win = wx.MDIChildFrame(o_window_base, -1, u"Ascii Graphics Generator", pos=(0,0))
        p_win.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        p_win.SetBackgroundColour(wx.WHITE)
                        
        self.l_fonts_lst = wx.StaticText( p_win, wx.ID_ANY, u"Ascii Graphics fonts available:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.e_fonts_lst = wx.Choice(p_win, id=wx.ID_ANY, choices = self.carica_lista_fonts() )        
        self.l_testo = wx.StaticText( p_win, wx.ID_ANY, u"Insert a text to convert:")               
        self.e_testo = wx.TextCtrl( p_win, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), wx.TE_PROCESS_ENTER)        
        self.b_converte = wx.BitmapButton( p_win, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )        
        self.l_result = wx.StaticText( p_win, wx.ID_ANY, u"Result:", wx.DefaultPosition, wx.DefaultSize, 0 )                
        self.e_result = wx.TextCtrl( p_win, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 700,300 ), wx.TE_MULTILINE|wx.TE_RICH2)        
        
        # posiziono gli oggetti sulla finestra
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.Add( self.l_fonts_lst, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        gbSizer1.Add( self.e_fonts_lst, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        gbSizer1.Add( self.l_testo, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        gbSizer1.Add( self.e_testo, wx.GBPosition( 1, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        gbSizer1.Add( self.b_converte, wx.GBPosition( 1, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        gbSizer1.Add( self.l_result, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )
        gbSizer1.Add( self.e_result, wx.GBPosition( 3, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
        # indico che il campo risultato è quello che si espande
        gbSizer1.AddGrowableRow(2)
        gbSizer1.AddGrowableCol(0)

        # creo un box che contiene il box precedente e indico di riepire tutta la finestra
        box = wx.BoxSizer()
        box.Add(gbSizer1, 1, wx.EXPAND | wx.ALL, 10)

        p_win.SetSizerAndFit(box)

        # collego gli eventi agli oggetti
        self.b_converte.Bind( wx.EVT_BUTTON, self.converte_ascii )
        self.e_testo.Bind( wx.EVT_TEXT_ENTER, self.converte_ascii )
        
    def carica_lista_fonts(self):
        '''
           Carica la listbox con elenco dei fonts (in pratica i files contenuti nella directory fonts)
           Ci sono due modalità di esecuzione. Una quando il programma è in fase di sviluppo per cui la directory fonts è annegate dentro le dir di sistema 
           e una modalità quando viene "compilato" dove la dir fonts è sotto la tabella pyfiglet. Per entrambe le situazioni il costrutto __file__ sembra andare bene!!
        '''         
        v_pyfiglet_fonts_dir = pyfiglet.__file__
        v_pyfiglet_fonts_dir = os.path.dirname(v_pyfiglet_fonts_dir)
        v_root_node = v_pyfiglet_fonts_dir + '\\fonts'        
        v_elenco_file = file_in_directory(v_root_node)
        v_lista_finale = []
        #v_lista_finale.append(v_root_node) questa è una riga utile per eventuale debug in quanto inserisce come primo elemento il nome della cartella dove va a cercare i font
        for nome_file in v_elenco_file:
            # filtro l'elenco dei file prendendo solo quelli con il suffisso .flf che sono quelli dei font disponibili
            if nome_file.find('.flf')>0:                
                # estrae solo il nome del file dalla stringa
                v_solo_nome_file = os.path.basename(nome_file)                
                # nella lista aggiunge solo la parte del nome senza il suffisso
                v_lista_finale.append(os.path.splitext(v_solo_nome_file)[0])
        return v_lista_finale
        
    def converte_ascii(self, event):        
        ''' 
           Esegue la conversione del testo semplice in testo graphics ascii
        '''
        if self.e_testo.GetLineText(0) == '':
            wx.MessageBox(message='Please insert a text', caption='Error', style=wx.OK | wx.ICON_ERROR)
            return None
        # pulisce il risultato
        self.e_result.Clear()                
        # il risultato viene impostato con il font richiesto (da non confondersi con il font con cui viene visualizzato)
        if self.e_fonts_lst.GetString(self.e_fonts_lst.GetSelection()) != '':
            risultato = pyfiglet.figlet_format(self.e_testo.GetLineText(0), font=self.e_fonts_lst.GetString(self.e_fonts_lst.GetSelection()))         
        # se però non è stato indicato alcun fonts, lascio il default
        else:
            risultato = pyfiglet.figlet_format(self.e_testo.GetLineText(0))         
        # imposto il risultato nella textbox
        self.e_result.SetValue(risultato)
        # il risultato lo visualizzo sempre usando il form COURIER NEW
        self.f_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "COURIER")        
        self.e_result.SetStyle(1,len(risultato),wx.TextAttr("BLACK", wx.NullColour, self.f_font))                       

# ----------------------------------------
# TESTING APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    # inizio test della procedura
    test = ascii_to_graphics(o_window_base, modalita_test=True)

    app.MainLoop()
