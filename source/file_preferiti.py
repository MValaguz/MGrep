# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria wxpython 4.0
 Data..........: 18/07/2018
 Descrizione...: Programma per la gestione dei file preferiti
"""

#Librerie sistema
import os
#Librerie grafiche
import wx
#Libreria per gestione zip
import zipfile
#Libreria per gestione date
import datetime
#Librerie interne smigrep
from preferenze import preferenze
from compile_oracle_form_report import pubblica_form_report
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

class file_preferiti:
    """
        Programma per la gestione dei file preferiti
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
            if 'MyPrefFile' in my_window_pos:
                win_pos =  (int(my_window_pos[1]), int(my_window_pos[2]))
                win_size = (int(my_window_pos[3]), int(my_window_pos[4]))                

        self.my_window = wx.MDIChildFrame(o_window_base, -1, u"My favorites files", size=win_size, pos=win_pos)
        self.my_window.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))

        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        # azioni di lista
        self.l_titolo1 = wx.StaticText( self.panel, wx.ID_ANY, u"List actions:", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.b_refresh = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "refresh.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_refresh.SetToolTip("Reload the list")

        self.b_insert_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "line.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_insert_line.SetToolTip("Insert an empty line into the list")

        self.b_sposta_su = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "up.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_sposta_su.SetToolTip("Shift up the selected line")

        self.b_sposta_giu = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "down.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_sposta_giu.SetToolTip("Shift down the selected line")

        self.b_delete_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "delete.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_delete_line.SetToolTip("Delete the selected line")

        self.b_clear = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "clear.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_clear.SetToolTip("Clear the list")

        self.b_save = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "disk.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_save.SetToolTip("Save the list")

        # azioni di item
        self.l_titolo2 = wx.StaticText( self.panel, wx.ID_ANY, u"Item actions:", wx.DefaultPosition, wx.DefaultSize, 0 )

        self.b_open_folder = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "folder.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_open_folder.SetToolTip('Open the directory from the selected line')

        self.b_backup_line = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "zip.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_backup_line.SetToolTip("It takes the source and copies it into the zip file named Old in the same folder as the file")

        self.b_pubblica_smile = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "plane.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_pubblica_smile.SetToolTip("Publish source of Oracle Form or Report Form on real servers (compiling as SMILE user)")

        self.b_pubblica_icom = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "car.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_pubblica_icom.SetToolTip("Publish source of Oracle Form or Report Form on real servers (compiling as ICOM user)")

        self.b_compile_icom = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "icom.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_compile_icom.SetToolTip("Compile form as ICOM user")
        
        self.b_compile_backup2 = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "gears2.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_compile_backup2.SetToolTip("Compile form as SMILE user on BACKUP_2")
        
        self.b_compile = wx.BitmapButton( self.panel, wx.ID_ANY, wx.Bitmap( pathname_icons() + "gears.gif", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW )
        self.b_compile.SetToolTip("Compile form as SMILE user")

        # lista dei file preferiti
        o_lst1Choices = []
        self.o_lst1 = wx.ListBox( self.panel, wx.ID_ANY, wx.DefaultPosition, wx.Size(-1,300), o_lst1Choices, style = wx.LB_SINGLE|wx.HSCROLL|wx.VSCROLL)
        # attivo il drag&drop sulla lista
        dt = my_drag_and_drop(self.o_lst1)
        self.o_lst1.SetDropTarget(dt)

        # collego gli eventi agli oggetti (pulsante di ricerca e tasto enter sulla campo ricerca)
        self.b_refresh.Bind( wx.EVT_BUTTON, self.carica_files_preferiti )
        self.b_insert_line.Bind( wx.EVT_BUTTON, self.inserisce_riga )
        self.b_sposta_su.Bind( wx.EVT_BUTTON, self.sposta_su )
        self.b_sposta_giu.Bind( wx.EVT_BUTTON, self.sposta_giu )
        self.b_delete_line.Bind( wx.EVT_BUTTON, self.cancella_riga_ricerca )
        self.b_clear.Bind( wx.EVT_BUTTON, self.pulisce_lista )
        self.b_save.Bind( wx.EVT_BUTTON, self.salva_files_preferiti )
        self.b_open_folder.Bind( wx.EVT_BUTTON, self.apre_cartella )
        self.b_backup_line.Bind( wx.EVT_BUTTON, self.backup_file_into_zip )
        self.b_pubblica_smile.Bind( wx.EVT_BUTTON, self.pubblica_smile )
        self.b_pubblica_icom.Bind( wx.EVT_BUTTON, self.pubblica_icom )
        self.b_compile_icom.Bind( wx.EVT_BUTTON, self.compila_oggetto_icom )
        self.b_compile_backup2.Bind( wx.EVT_BUTTON, self.compila_oggetto_backup2 )
        self.b_compile.Bind( wx.EVT_BUTTON, self.compila_oggetto_smile )
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
        gbSizer1.Add( self.l_titolo1,     wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTRE, 1 )
        gbSizer1.Add( self.b_refresh,     wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_insert_line, wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_sposta_su,   wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_sposta_giu,  wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_delete_line, wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer1.Add( self.b_clear,       wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer1.Add( self.b_save,        wx.GBPosition( 0, 7 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )

        # box figlio item list
        gbSizer2 = wx.GridBagSizer( 0, 0 )
        gbSizer2.SetFlexibleDirection( wx.BOTH )
        gbSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer2.Add( self.l_titolo2,        wx.GBPosition( 0, 0 ), wx.GBSpan( 1, 1 ), wx.ALIGN_CENTRE, 1 )
        gbSizer2.Add( self.b_open_folder,    wx.GBPosition( 0, 1 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.Add( self.b_backup_line,    wx.GBPosition( 0, 2 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.b_pubblica_smile, wx.GBPosition( 0, 3 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.Add( self.b_pubblica_icom,  wx.GBPosition( 0, 4 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.b_compile_icom,   wx.GBPosition( 0, 5 ), wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer2.Add( self.b_compile_backup2,wx.GBPosition( 0, 6 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )
        gbSizer2.Add( self.b_compile,        wx.GBPosition( 0, 7 ), wx.GBSpan( 1, 1 ), wx.ALL|wx.EXPAND, 1 )

        # box lista risultati
        gbSizer3 = wx.GridBagSizer( 0, 0 )
        gbSizer3.SetFlexibleDirection( wx.BOTH )
        gbSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        gbSizer3.Add( gbSizer1,     wx.GBPosition( 0, 0 ),  wx.GBSpan( 1, 1 ), wx.ALL, 1 )
        gbSizer3.Add( gbSizer2,     wx.GBPosition( 0, 24 ), wx.GBSpan( 1, 1 ), wx.ALIGN_RIGHT, 1 )

        # inserisco i figli dentro il padre
        bSizer_padre.Add( gbSizer3,      1, wx.TOP | wx.LEFT, 10 )
        bSizer_padre.Add( self.o_lst1, 100, wx.ALL | wx.EXPAND, 10 )

        # visualizzo il pannello
        self.panel.SetSizer( bSizer_padre)
        self.panel.Layout()

        # carico la lista dei file preferiti
        self.carica_files_preferiti(None)

    def doppio_click(self, event):
        """
            doppio click su listbox
        """
        v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        if v_seltext != '':
            try:
                os.startfile(v_seltext)
            except:
                wx.MessageBox(text='File not found or problem during open application!', caption = 'Error', style = ex.OK | wx.ICON_ERROR)

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

    def backup_file_into_zip(self, event):
        """
            copia il file indicato all'interno di un file zip di nome Old, presente nella medesima
            cartella del file di partenza. Se il file zip non esiste, viene creato. Se esiste il file
            indicato viene accodato
        """
        if wx.MessageBox(message="Do you want to backup file into old.zip?", caption="Backup file", style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
            #scompongo l'intera pathname in tutte le sue componenti (directory, nome file, suffisso)
            v_directory = os.path.split(v_seltext)[0]
            v_solo_nome_file = os.path.split(v_seltext)[1]
            v_solo_nome_file_senza_suffisso = os.path.splitext(v_solo_nome_file)[0]
            v_suffisso_nome_file = os.path.splitext(v_solo_nome_file)[1]
            #prendo la data di sistema che servirà per dare un suffisso al nome del file che viene zippato
            v_system_date = datetime.datetime.now()
            v_str_data  = '_' + str(v_system_date.year) + '_' + str(v_system_date.month) + '_' + str(v_system_date.day)
            if v_directory != '':
                try:
                    #apro il file zip (se non esiste lo creo)
                    v_zip = zipfile.ZipFile(v_directory + '\\old.zip','a')
                    #accodo il file indicato allo zip (il nome di arrivo è il nome del file più suffisso data)
                    v_zip.write(v_seltext, v_solo_nome_file_senza_suffisso + v_str_data + '.' + v_suffisso_nome_file)
                    #chiudo lo zip e emetto messaggio che procedura terminata
                    v_zip.close()
                    wx.MessageBox(message='The file ' + v_solo_nome_file + ' is been copied into Old.zip', caption='Backup file', style=wx.OK|wx.ICON_INFORMATION)
                except:
                    wx.MessageBox(message='Error to copy the file into Old zip!', caption='Backup file', style=wx.OK|wx.ICON_ERROR)

    def pubblica_smile(self, event):
        """
            pubblica il file Oracle Form o Oracle Report nei server indicati (come SMILE)
        """
        v_file = ''
        try:
            #estraggo l'intera pathname del file, file compreso
            v_file = v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        except:
            pass
        #se è stato selezionato qualcosa
        if v_file != '' and wx.MessageBox(message="Do you want to compile the file " + chr(10) + v_file + chr(10) + "and post it in SMILE system?", caption="Compile process", style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            #sono ammessi solo file con suffissi specifici
            if '.fmb' not in v_file and '.rdf' not in v_file:
                wx.MessageBox(message='File is not in format "Oracle Form" or "Oracle Report"!', caption='Compile process', style=wx.OK|wx.ICON_ERROR)
            else:
                # apro una nuova finestra figlia della principale
                canvas = pubblica_form_report(v_file, 
                                              self.o_preferenze.work_dir, 
                                              '1')

    def pubblica_icom(self, event):
        """
            pubblica il file Oracle Form o Oracle Report nei server indicati (come SMILE)
        """
        v_file = ''
        try:
            #estraggo l'intera pathname del file, file compreso
            v_file = v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
        except:
            pass
        #se è stato selezionato qualcosa
        if v_file != '' and wx.MessageBox(message="Do you want to compile the file " + chr(10) + v_file + chr(10) + "and post it in ICOM system?", caption="Compile process", style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            #sono ammessi solo file con suffissi specifici
            if '.fmb' not in v_file and '.rdf' not in v_file:
                wx.MessageBox(message='File is not in format "Oracle Form" or "Oracle Report"!', caption='Compile process', style=wx.OK|wx.ICON_ERROR)
            else:
                # apro una nuova finestra figlia della principale
                canvas = pubblica_form_report(v_file, self.o_preferenze.work_dir, '2')

    def pulisce_lista(self, event):
        """
            pulisce il contenuto della lista
        """
        if wx.MessageBox(message="Do you want to clear result list?", caption="Clear list", style=wx.YES_NO|wx.ICON_INFORMATION) == wx.YES:
            self.o_lst1.Clear()

    def cancella_riga_ricerca(self, event):
        """
            cancella dalla lista dei risultati la riga attualmente selezionata
        """
        try:
            v_index = self.o_lst1.GetSelection()
            self.o_lst1.Delete(v_index)
        except:
            pass

    def carica_files_preferiti(self, event):
        """
            carica quanto presente nel file dei risultati
        """
        self.o_lst1.Clear()
        try:
            v_file = open(self.o_preferenze.favorites_file, 'r')
            v_stringa = v_file.readline()
            while v_stringa != '':
                # elimino dalla stringa il carattere di ritorno a capo
                v_stringa = v_stringa.rstrip('\n')
                self.o_lst1.Append(v_stringa)
                v_stringa = v_file.readline()
            v_file.close()
        except:
            pass

    def salva_files_preferiti(self, event):
        """
            salva elenco lista file preferiti
        """
        f_output = open(self.o_preferenze.favorites_file, 'w')

        for v_index in range(0, self.o_lst1.GetCount()):
            f_output.write(self.o_lst1.GetString(v_index) + '\n')

        # chiudo il file dei risultati
        f_output.close()

    def compila_oggetto_icom(self, event):
        """
            compila l'oggetto selezionato sul tab3 come backup_815
        """
        try:
            v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
            if v_seltext != '':
                try:
                    os.system('c:\ITCCONF\compilaauto.bat "' + v_seltext + '" smi/smi@backup_815')
                except:
                    wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)
        except:
            wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)

    def compila_oggetto_smile(self, event):
        """
            compila l'oggetto selezionato sul tab3 come backup_815
        """
        try:
            v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
            if v_seltext != '':
                try:
                    os.system('c:\ITCCONF\compilaauto.bat "' + v_seltext + '" smile/smile@backup_815')
                except:
                    wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)
        except:
            wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)
            
    def compila_oggetto_backup2(self, event):
        """
            compila l'oggetto selezionato sul tab3 come backup_815_2
        """
        try:
            v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
            if v_seltext != '':
                try:
                    os.system('c:\ITCCONF\compilaauto.bat "' + v_seltext + '" smile/smile@backup_2_815')
                except:
                    wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)
        except:
            wx.MessageBox(message='Problem during object compile!', caption='Error', style=wx.OK|wx.ICON_ERROR)    

    def apre_cartella(self, event):
        """
            apre la cartella dove si trova il file selezionato
        """
        try:
            v_seltext = self.o_lst1.GetString(self.o_lst1.GetSelection())
            if v_seltext != '':
                try:
                    os.startfile(v_seltext[0:v_seltext.rfind('\\')])
                except:
                    wx.MessageBox(message='Problem during open object folder!', caption='Error', style=wx.OK|wx.ICON_ERROR)
        except:
            wx.MessageBox(message='Problem during open object folder!', caption='Error', style=wx.OK|wx.ICON_ERROR)


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
    test = file_preferiti(o_window_base, modalita_test=True)

    app.MainLoop()
