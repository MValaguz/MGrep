# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 20/07/2018
 Descrizione...: Programma per la gestione delle directory preferite
"""

#Librerie sistema
import os
#Librerie grafiche
import wx
#Librerie interne smigrep
from preferenze import preferenze
from test_app import Test_App
from utilita import pathname_icons

class my_drag_and_drop(wx.FileDropTarget):
    """
        classe pe il funzionamento del drag&drop su una lista
    """
    def __init__(self, p_obj):
        wx.FileDropTarget.__init__(self)
        self.my_obj = p_obj

    def OnDropFiles(self, x, y, filenames):
        txt = filenames
        self.my_obj.Append(txt)
        return True

class directory_preferite:
    """
        Programma per la gestione delle directory preferite
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
            if 'MyPrefDir' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))

        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"My favorites directories", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # azioni di lista
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"List actions:", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.b_open_folder = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "folder.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_open_folder.SetToolTip("Allows you to select a folder to add to favorites")

        self.b_insert_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "line.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_insert_line.SetToolTip("Insert an empty line into the list")

        self.b_sposta_su = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "up.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_sposta_su.SetToolTip("Shift up the selected line")

        self.b_sposta_giu = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "down.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_sposta_giu.SetToolTip("Shift down the selected line")

        self.b_delete_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "delete.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_delete_line.SetToolTip("Delete the selected line")

        self.b_clear = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "clear.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_clear.SetToolTip("Clear the list")

        self.b_save_list = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons()  + "disk.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_save_list.SetToolTip("Save the list")

        # lista dei file preferiti
        o_lst1Choices = []
        self.o_lst1 = wx.ListBox( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,-1), o_lst1Choices, style = wx.LB_SINGLE|wx.HSCROLL|wx.VSCROLL)
        # attivo il drag&drop sulla lista
        dt = my_drag_and_drop(self.o_lst1)
        self.o_lst1.SetDropTarget(dt)

        # collego gli eventi agli oggetti (pulsante di ricerca e tasto enter sulla campo ricerca)
        self.b_open_folder.Bind( wx.EVT_BUTTON, self.aggiunge_cartella )
        self.b_insert_line.Bind( wx.EVT_BUTTON, self.inserisce_riga )
        self.b_sposta_su.Bind( wx.EVT_BUTTON, self.sposta_su )
        self.b_sposta_giu.Bind( wx.EVT_BUTTON, self.sposta_giu )
        self.b_delete_line.Bind( wx.EVT_BUTTON, self.cancella_riga_ricerca )
        self.b_clear.Bind( wx.EVT_BUTTON, self.pulisce_lista )
        self.b_save_list.Bind( wx.EVT_BUTTON, self.salva_directories_preferite )
        self.o_lst1.Bind( wx.EVT_LISTBOX_DCLICK, self.doppio_click )

        ###
        # Impaginazione degli elementi
        ###
        # box padre
        bSizer_padre = wx.BoxSizer( wx.VERTICAL )

        # box figlio action list
        gbSizer1 = wx.GridBagSizer( 0, 0 )
        gbSizer1.SetFlexibleDirection( wx.BOTH )
        gbSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer1.Add( self.l_titolo1,     wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTER, 1 )
        gbSizer1.Add( self.b_open_folder, wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer1.Add( self.b_insert_line, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_sposta_su,   wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_sposta_giu,  wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_delete_line, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_clear,       wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer1.Add( self.b_save_list,   wx.GBPosition( 0, 7 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )

        # box lista risultati
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer2.Add( gbSizer1,  wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.o_lst1,  wx.GBPosition( 1, 0 ), wx.GBSpan( 1, 2 ), wx.ALL|wx.EXPAND, 1 )

        # indico che la colonna 1 (dove finisce la lista) e la riga sono flessibili
        gbSizer2.AddGrowableCol(1)
        gbSizer2.AddGrowableRow(1)

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer2, 1, wx.ALL | wx.EXPAND, 10 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()
        #self.my_window.Maximize()

        # carico la v_list_value
        self.carica_directories_preferite(None)

    def inserisce_riga(self, event):
        """
            inserisce una riga vuota all'interno della lista
        """
        try:
            v_index = self.o_lst1.GetSelection()
        except:
            v_index = -1
        # aggiungo la riga in fondo se nessun elemento della lista è stato selezionato
        if v_index < 0:
            self.o_lst1.Append('-'*100)
        # oppure alla posizione successiva se un elemento è stato selezionato
        else:
            self.o_lst1.Insert('-'*100, v_index+1)

    def sposta_su(self, event):
        """
            sposta verso l'alto la riga selezionata
        """
        try:
            v_index = self.o_lst1.GetSelection()
        except:
            return
        if v_index > 0:
            v_list_value = self.o_lst1.GetString(v_index)
            self.o_lst1.Delete(v_index)
            self.o_lst1.Insert(v_list_value,v_index-1)
            self.o_lst1.SetSelection(v_index-1)

    def sposta_giu(self, event):
        """
            sposta verso il basso la riga selezionata
        """
        try:
            v_index = self.o_lst1.GetSelection()
            v_tot = self.o_lst1.GetCount()
        except:
            return

        if v_index > 0 and v_index < v_tot-1:
            v_list_value = self.o_lst1.GetString(v_index)
            self.o_lst1.Delete(v_index)
            self.o_lst1.Insert(v_list_value, v_index+1)
            self.o_lst1.SetSelection(v_index+1)

    def doppio_click(self, event):
        """
            apre la cartella dove si trova il file selezionato nel tab3
        """
        v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        if v_seltext != '':
            try:
                # os.startfile(v_seltext[0:v_seltext.rfind('\\')])
                os.startfile(v_seltext)
            except:
                wx.MessageBox(message='Problem during open object folder!', caption='Error', style=wx.OK|wx.ICON_ERROR)

    def cancella_riga_ricerca(self, event):
        """
            cancella dalla lista dei risultati la riga attualmente selezionata
        """
        try:
            v_index = self.o_lst1.GetSelection()
            self.o_lst1.Delete(v_index)
        except:
            pass

    def pulisce_lista(self, event):
        """
            pulisce il contenuto della lista
        """
        if wx.MessageBox(message="Do you want to clear result list?", caption="Clear list", style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            self.o_lst1.Clear()

    def salva_directories_preferite(self, event):
        """
            salva la lista
        """
        f_output = open(self.o_preferenze.favorites_dirs, 'w')

        for v_index in range(0, self.o_lst1.GetCount()):
            f_output.write(self.o_lst1.GetString(v_index) + '\n')

        # chiudo il file dei risultati
        f_output.close()

    def carica_directories_preferite(self, event):
        """
            carica la lista
        """
        try:
            v_file = open(self.o_preferenze.favorites_dirs, 'r')
            v_stringa = v_file.readline()
            while v_stringa != '':
                # elimino dalla stringa il carattere di ritorno a capo
                v_stringa = v_stringa.rstrip('\n')
                self.o_lst1.Append(v_stringa)
                v_stringa = v_file.readline()
            v_file.close()
        except:
            pass

    def aggiunge_cartella(self):
        """
            permette di selezionare cartella da aggiungere a quelle dei preferiti
        """
        dlg = wx.DirDialog(self.my_window, "Choose a directory:",style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.o_lst1.Append( dlg.GetPath() )
            dlg.Destroy()

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    o_window_base = Test_App(None)
    o_window_base.Show(True)

    ###
    # test gestione directory preferite
    ###
    test = directory_preferite(o_window_base, modalita_test=True)

    app.MainLoop()
