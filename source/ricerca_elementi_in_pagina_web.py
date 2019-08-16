# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 10/07/2018
 Descrizione...: Ricerca immagini in pagina web.
                 Questa procedura è stata creata perché è sempre difficile capire quali sono le immagini presenti in una pagina di help di SMILE.
"""

#Librerie per leggere pagina web
from urllib import request
#Librerie grafiche
import  wx
#Librerie interne SmiGrep
from test_app import Test_App
from utilita import pathname_icons

class ricerca_elementi_in_pagina_web(wx.ScrolledWindow):
    """
        Apre una finestra dove richieste l'indirizzo web e ne analizza il contenuto
    """
    def __init__( self, o_window_base, modalita_test):
        # creo la finestra come figlia della finestra di partenza
        p_win = wx.MDIChildFrame(o_window_base, -1, u"Search images in web page", pos=(0,0))
        p_win.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        p_win.SetBackgroundColour(wx.WHITE)

        # creo il contenitore base
        gbSizer1 = wx.GridBagSizer( 0, 0 )

        self.l_url = wx.StaticText( p_win, wx.ID_ANY, u"Insert a valid URL:")
        gbSizer1.Add( self.l_url, wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.e_url = wx.TextCtrl( p_win, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), wx.TE_PROCESS_ENTER)
        gbSizer1.Add( self.e_url, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        self.b_url = wx.BitmapButton( p_win, wx.ID_ANY, wx.Bitmap( pathname_icons() + 'go.gif', wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        gbSizer1.Add( self.b_url, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        self.l_result = wx.StaticText( p_win, wx.ID_ANY, u"Result:", wx.DefaultPosition, wx.DefaultSize, 0 )
        gbSizer1.Add( self.l_result, wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 5 )

        o_lst1Choices = []
        self.o_lst1 = wx.ListBox( p_win, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,150), o_lst1Choices, style = wx.LB_SINGLE )
        gbSizer1.Add( self.o_lst1, wx.GBPosition( 2, 0 ), wx.GBSpan( 1, 3 ), wx.EXPAND, 5 )
        # indico la listbox è quella che si espande
        gbSizer1.AddGrowableRow(2)
        gbSizer1.AddGrowableCol(0)

        # creo un box che contiene il bag precedente e indico di riepire tutta la finestra
        box = wx.BoxSizer()
        box.Add(gbSizer1, 1, wx.EXPAND | wx.ALL, 10)

        p_win.SetSizerAndFit(box)

        # collego gli eventi agli oggetti
        self.b_url.Bind( wx.EVT_BUTTON, self.ricerca_elementi )
        self.e_url.Bind( wx.EVT_TEXT_ENTER, self.ricerca_elementi )

    def ricerca_elementi(self, event):        
        if self.e_url.GetLineText(0) == '':
            wx.MessageBox(message='Please insert a valid URL', caption='Error', style=wx.OK | wx.ICON_ERROR)
            return None
        # pulisce la lista
        self.o_lst1.Clear()

        # legge la pagina web
        try:
            v_pagina_web=request.urlopen(self.e_url.GetLineText(0))
        except:
            wx.MessageBox(message='Page not found or unknow error', caption='Error', style=wx.OK | wx.ICON_ERROR)
            return None
        v_contenuto=str(v_pagina_web.read())
        v_pos=v_contenuto.find('<img alt="')
        v_risultato=[]
        while v_pos > 0:
            v_pos_fin=v_contenuto.find('"',v_pos+10)
            v_risultato.append(v_contenuto[v_pos+10:v_pos_fin])
            v_pos=v_contenuto.find('<img alt="', v_pos+1)

        # carica la lista ordinando i risultati alfabeticamente
        v_risultato_ordinato=sorted(v_risultato)
        #for i in v_risultato_ordinato:
        self.o_lst1.InsertItems(v_risultato_ordinato,0)

# ----------------------------------------
# TESTING APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    # inizio test della procedura
    test = ricerca_elementi_in_pagina_web(o_window_base, modalita_test=True)

    app.MainLoop()
