# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 26/07/2018
 Descrizione...: Gestione della finestra console dove vengono indirizzati gli output della console di Python
"""

#Librerie grafiche
import  wx
#Libreria di sistema
import sys
#Librerie interne SmiGrep
from test_app import Test_App
from utilita import pathname_icons

class console:
    """
        Viene creata una finestra console, nascosta, che viene visualizzata con apposita richiesta
        Tale finestra prende i reindirizzamenti degli stantard input output e error di Python
    """
    class RedirectText(object):
        """
            super classe per visualizzare testo
        """
        def __init__(self, aWxTextCtrl):
            self.out = aWxTextCtrl

        def flush(self, s):
            self.out.WriteText(s)

        def write(self,s):
            self.out.WriteText(s)

    def __init__(self, o_window_base, modalita_test):

        # creo la finestra come figlia della finestra di partenza
        self.win = wx.MDIChildFrame(o_window_base, -1, u"Console (in this window you can see any internal error of SmiGrep)", size=(780,510),pos=(0,0))
        self.win.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        self.panel = wx.Panel(self.win, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # creo un campo testo avanzato che ha al suo intento il metodo flush
        self.o_console = wx.TextCtrl(self.panel, wx.ID_ANY, size=(300,100), style= wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # formatto il layout
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(self.o_console, 7, wx.ALL|wx.EXPAND, 5)

        self.panel.SetSizer( bSizer1)
        self.panel.Layout()

        # reindirizzo l'output sul pannello
        sys.stdout=self.RedirectText(self.o_console)
        sys.stderr=self.RedirectText(self.o_console)

        # nascondo la console
        self.hide_console(None)
        # indico che l'evento di chiusura della finestra deve richiamare la procedura che in realtà la nasconde
        self.win.Bind(wx.EVT_CLOSE, self.hide_console)

        # se modalità test creo un pulsante per fare il testo
        if modalita_test:
            self.b_button = wx.Button( self.panel, wx.ID_ANY, u"Click me for run a test", wx.DefaultPosition, wx.DefaultSize, 0 )
            self.b_button.Bind( wx.EVT_BUTTON, self.crea_errore )
            bSizer1.Add(self.b_button, 1, wx.ALL|wx.EXPAND, 5)
            self.panel.Layout()

    def view_console(self):
        """
            rende visibile la console
        """
        self.win.Show(True)

    def hide_console(self, event):
        """
            rende invisibile la console
        """
        self.win.Show(False)

    def crea_errore(self, event):
        """
            crea un errore interno
        """
        print('------ istruzioni print -------')
        # prova di output
        for i in range(1,10):
            print(str(i) + 'Prova di indirizzamento')
        print('------ istruzione che generare errore interno -------')
        print('ciao' + 10)

# ----------------------------------------
# TESTING APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(redirect=False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)
    test = console(o_window_base, modalita_test=True)
    test.view_console()
    app.MainLoop()
