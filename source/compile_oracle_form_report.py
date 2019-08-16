# -*- coding: UTF-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 15/06/2018
 Descrizione...: Scopo dello script è prendere un file "Oracle form" o "Oracle report" e pubblicarlo sul server di SMILE
"""

import wx
#Librerie di data base
import  cx_Oracle
#Libreria sistema
import  os
import  sys
import  subprocess
#Librerie interne SmiGrep
from utilita import pathname_icons

class pubblica_form_report(wx.Frame):
    """
        Compila un oggetto form o report
        Va indicato attraverso l'instanziazione della classe:
            p_sorgente       = Path name completa del file sorgente
            p_work_dir       = Directory di lavoro
            p_tipo           = 1=SMILE, 2=ICOM
    """
    def __init__(self,
                 p_sorgente,
                 p_work_dir,
                 p_tipo):
        
        # creo la finestra come figlia della finestra di partenza
        self.my_window = wx.Frame(None, title = u"Compiling Oracle forms e Oracle reports", size=(400,120))
        self.my_window.SetIcon(wx.Icon(pathname_icons() + 'search.ico', wx.BITMAP_TYPE_ICO))
        # creo un pannello contenitore
        self.panel = wx.Panel(self.my_window, wx.ID_ANY)
        self.panel.SetBackgroundColour("WHITE")

        self.label_1 = wx.StaticText(self.panel, wx.ID_ANY, "Publication on Server iAS12g")
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

        #Compilazione su server 12g
        if self.compilazione('10.0.4.14', 'fmw12Oracle_01', p_sorgente, p_work_dir, p_tipo) == 'ok':
            wx.MessageBox(message='Compilation completed successful!', caption='Compile process', style=wx.OK | wx.ICON_INFORMATION)

        self.my_window.Close()
        return None

    def compilazione(self,
                     p_ip,
                     p_pwd,
                     p_sorgente,
                     p_work_dir,
                     p_tipo):

        #Aggiorno informazioni di avanzamento
        self.label_2.SetLabel('Copy source in server...')
        self.panel.Layout()
        self.gauge_1.SetValue(33)
        self.panel.Update()

        v_solo_nome_file = os.path.split(p_sorgente)[1]
        v_solo_nome_file_senza_suffisso = os.path.splitext(v_solo_nome_file)[0]
        v_suffisso_nome_file = os.path.splitext(v_solo_nome_file)[1]

        #controllo se il nome del file contiene un trattino (vuol dire che va troncato perché è stata stabilita questa convenzione)
        #esempio PM3000101F-PREVENTIVI LAVORAZIONE MECCANICHE.fmb
        if '-' in v_solo_nome_file_senza_suffisso:
            v_solo_nome_file_senza_suffisso = v_solo_nome_file_senza_suffisso[0:v_solo_nome_file_senza_suffisso.find('-')]

        #ricavo il nuovo nome del file (es. PM3000101F.fmb)
        v_nuovo_nome_file = v_solo_nome_file_senza_suffisso + v_suffisso_nome_file

        #imposto i nomi dei file su cui ridirigere output dei comandi (in questo modo non escono le brutte window di dos)
        v_sshoutput = open(os.path.join(p_work_dir, 'sshoutput.txt'), 'w')
        v_sshoutputerror = open(os.path.join(p_work_dir, 'sshoutputerror.txt'), 'w')
        v_sshinput = ''

        #tramite il comando pscp (che deve essere copiato nella directory dell'eseguibile, copio il file nella cartella incoming)
        v_command = 'echo y | risorse\\pscp -pw ' + p_pwd + ' "' + p_sorgente + '" oracle@' + p_ip + ':/appl/incoming/' + v_nuovo_nome_file
        try:
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)                                    
            v_ssh.communicate(v_sshinput)
        except:
            wx.MessageBox(message='Copy file in dir "Incoming" failed!', caption='Compile process', style=wx.OK | wx.ICON_ERROR)
            return 'ko'

        self.label_2.SetLabel('Compiling source in server...')
        self.panel.Layout()
        self.gauge_1.SetValue(66)
        self.panel.Update()
        
        #eseguo la compilazione (il risultato della compilazione finisce in un file pcname_output.txt dove pcname è il nome del pc di esecuzione
        v_nome_pc = os.getenv('COMPUTERNAME').replace('-','_')
        v_nome_file_output = v_nome_pc + '_output.txt'
        try:
            if p_tipo == '1':
                v_utente_oracle = 'SMILE/SMILE@ICOM_815'
            else:
                v_utente_oracle = 'SMI/SMI@ICOM_815'
            #compilazione
            v_command = 'echo y | risorse\\plink -pw ' + p_pwd + ' oracle@' + p_ip + ' "/appl/incoming/./frmcmpl "' + v_nuovo_nome_file + '" ' + v_utente_oracle + ' ' + v_nome_file_output
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            wx.MessageBox(message='Plink command error!', caption='Compile process', style=wx.OK | wx.ICON_ERROR)
            return 'ko'

        #eseguo controllo se compilazione terminata con errore
        self.label_2.SetLabel('Analyze compile output...')
        self.panel.Layout()
        self.gauge_1.SetValue(100)
        self.panel.Update()        
        try:
            #scarico il file di output generato dal compilatore nella dir smigrep del disco c
            v_command = 'echo y | risorse\\pscp -pw ' + p_pwd + ' oracle@' + p_ip + ':/appl/incoming/' + v_nome_file_output + ' ' + os.path.join(p_work_dir, v_nome_file_output)
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            wx.MessageBox(message='Error to download ' + v_nome_file_output + '!', caption='Compile process', style=wx.OK | wx.ICON_ERROR)
            return 'ko'

        #leggo il file di output e controllo se contiene la stringa che indica che è andato tutto ok
        v_tutto_ok = False
        with open(os.path.join(p_work_dir, v_nome_file_output),'r') as v_file:
            for v_line in v_file:
                if 'Compilation' in v_line and 'successful.' in v_line:
                    v_tutto_ok = True

        #compilazione ko...
        if not v_tutto_ok:
            wx.MessageBox(message='There are errors in form/report!', caption='Compile process', style=wx.OK | wx.ICON_ERROR)
            return 'ko'

        #Se la fase di compilazione è andata a buon fine --> mi collego al DB Oracle e segno i dati di utente e data ultima modifica
        try:
            self.v_oracle_db = cx_Oracle.connect(user='SMILE', password='SMILE', dsn='ICOM_815')
        except:
            wx.MessageBox(message='Connecting problems to Oracle DB!', caption='Compile process', style=wx.OK | wx.ICON_ERROR)
            return 'ko'

        self.v_oracle_cursor = self.v_oracle_db.cursor()

        #aggiorno la tabella con i dati dell'ultima compilazione
        v_user_name = v_nome_pc[v_nome_pc.find('_')+1:len(v_nome_pc)]
        v_query = "update ta_prog set utmod_co = '" + v_user_name + "', mod_da = sysdate where prog_co = '" + v_solo_nome_file_senza_suffisso + "'"
        self.v_oracle_cursor.execute(v_query)
        self.v_oracle_db.commit()
        self.v_oracle_db.close()

        v_sshoutput.close()
        v_sshoutputerror.close()

        #fine tutto ok
        return 'ok'

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = wx.App()
    test = pubblica_form_report("W:\\source\\MA-Magazzino\\Sviluppo\\Form\\MA2000701F-ANAGRAFICA ARTICOLI.fmb",
                                "C:\\SMIGREP\\",
                                "1")
    app.MainLoop()
