# -*- coding: UTF-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 19/07/2018
 Descrizione...: Contiene la window base per eseguire i test delle singole procedure
"""

import wx

class Test_App(wx.MDIParentFrame):
    """
        creazione della finestra di base
    """
    def __init__( self, parent):

        wx.MDIParentFrame.__init__(self, None, -1, title = u"SmiGrep TEST!!!", size = wx.Size( 800,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # defizione status bar
        self.o_statusbar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )

        # definizione dei menu
        self.o_w1_menu_bar = wx.MenuBar( 0 )
        self.m_file = wx.Menu()

        self.m_exit = wx.MenuItem( self.m_file, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_file.Append( self.m_exit )

        self.o_w1_menu_bar.Append( self.m_file, u"File" )

        self.SetMenuBar( self.o_w1_menu_bar )

        # creazione della tool bar
        #self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY )
        #self.m_bpButton5 = wx.BitmapButton( self.m_toolBar1, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        #self.m_toolBar1.AddControl( self.m_bpButton5 )
        #self.m_toolBar1.Realize()

        # connessione degli eventi chiusura programma
        self.Bind(wx.EVT_CLOSE, self.chiusura_programma)
        self.Bind(wx.EVT_MENU, self.chiusura_programma, id = self.m_exit.GetId() )

        # centratura automatica della window
        self.Centre( wx.BOTH )

    def chiusura_programma(self, event):
        """
            chiude il programma 
        """
        self.Destroy()
