# -*- coding: UTF-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 15/06/2018
 Descrizione...: Scopo dello script è prendere un file "Oracle form" o "Oracle report" e pubblicarlo sul server di SMILE
"""

#Librerie di data base
import  cx_Oracle
#Libreria sistema
import  os
import  sys
import  subprocess
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
#Librerie interne MGrep
from utilita import message_error, message_info, message_question_yes_no
from preferenze import preferenze

class pubblica_form_report(QtWidgets.QWidget):
    """
        Compila un oggetto form o report
        Va indicato attraverso l'avvio della procedura "pubblica":
            p_sorgente       = Path name completa del file sorgente
            p_work_dir       = Directory di lavoro
            p_tipo           = 1=SMILE, 2=ICOM
    """
    def __init__(self, p_sorgente, p_work_dir, p_tipo):        
        # rendo la mia classe una superclasse
        super(pubblica_form_report, self).__init__()        
          
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()                
                        
        # creazione della wait window
        self.v_progress_step = 0
        self.progress = QtWidgets.QProgressDialog(self)        
        self.progress.setMinimumDuration(0)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Pubblication on server iAS12g")                
        
        # icona di riferimento
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)        
        self.progress.setWindowIcon(icon)
        
        # imposto valore minimo e massimo a 0 in modo venga considerata una progress a tempo indefinito
        # Attenzione! dentro nel ciclo deve essere usata la funzione setvalue altrimenti non visualizza e non avanza nulla!
        self.progress.setMinimum(0)
        self.progress.setMaximum(100) 
        # creo un campo label che viene impostato con 100 caratteri in modo venga data una dimensione di base standard
        self.progress_label = QtWidgets.QLabel()            
        self.progress_label.setText('.'*100)
        # collego la label già presente nell'oggetto progress bar con la mia label 
        self.progress.setLabel(self.progress_label)                           
    
        #Compilazione su server 12g
        if self.compilazione('10.0.4.14', self.o_preferenze.v_server_password_iAS, p_sorgente, p_work_dir, p_tipo) == 'ok':
            message_info('Pubblication completed successful!')    
            
        self.progress.close()
        self.close()

    def compilazione(self,
                     p_ip,
                     p_pwd,
                     p_sorgente,
                     p_work_dir,
                     p_tipo):
        
        #Aggiorno informazioni di avanzamento
        self.avanza_progress('Copy source in server...')
        
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
        v_command = 'echo y | utility_prog\\pscp -pw ' + p_pwd + ' "' + p_sorgente + '" oracle@' + p_ip + ':/appl/incoming/' + v_nuovo_nome_file        
        try:            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)                                    
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Copy file in dir "Incoming" failed!')
            return 'ko'
        
        #Aggiorno informazioni di avanzamento
        self.avanza_progress('Compiling source in server...')        
        
        #eseguo la compilazione (il risultato della compilazione finisce in un file pcname_output.txt dove pcname è il nome del pc di esecuzione
        v_nome_pc = os.getenv('COMPUTERNAME').replace('-','_')
        v_nome_file_output = v_nome_pc + '_output.txt'
        try:
            if p_tipo == '1':
                v_utente_oracle = 'SMILE/SMILE@ICOM_815'
            else:
                v_utente_oracle = 'SMI/SMI@ICOM_815'
            #compilazione
            v_command = 'echo y | utility_prog\\plink -pw ' + p_pwd + ' oracle@' + p_ip + ' "/appl/incoming/./frmcmpl "' + v_nuovo_nome_file + '" ' + v_utente_oracle + ' ' + v_nome_file_output            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Plink command error!')
            return 'ko'

        #eseguo controllo se compilazione terminata con errore        
        self.avanza_progress('Analyze compile output...')        
        
        try:
            #scarico il file di output generato dal compilatore nella dir MGrep del disco c
            v_command = 'echo y | utility_prog\\pscp -pw ' + p_pwd + ' oracle@' + p_ip + ':/appl/incoming/' + v_nome_file_output + ' ' + os.path.join(p_work_dir, v_nome_file_output)            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Error to download ' + v_nome_file_output + '!')
            return 'ko'

        #leggo il file di output e controllo se contiene la stringa che indica che è andato tutto ok
        v_tutto_ok = False
        with open(os.path.join(p_work_dir, v_nome_file_output),'r') as v_file:
            for v_line in v_file:
                if 'Compilation' in v_line and 'successful.' in v_line:
                    v_tutto_ok = True

        #compilazione ko...
        if not v_tutto_ok:
            message_error('There are errors in form/report!')
            return 'ko'

        #Se la fase di compilazione è andata a buon fine --> mi collego al DB Oracle e segno i dati di utente e data ultima modifica
        try:
            self.v_oracle_db = cx_Oracle.connect(user='SMILE', password='SMILE', dsn='ICOM_815')
        except:
            message_error('Connecting problems to Oracle DB!')
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
    
    def avanza_progress(self, p_msg):
        """
           Visualizza prossimo avanzamento sulla progress bar. Per una ragione al momento sconosciuta
           ho dovuto fare un doppio giro per effettuasse il refresh a video!
        """
        self.v_progress_step += 1
        self.progress.setValue(self.v_progress_step);                                        
        self.progress_label.setText(p_msg)
        self.progress.setLabel(self.progress_label)             
        self.v_progress_step += 32
        if self.v_progress_step > 90:
            self.v_progress_step = 100
        self.progress.setValue(self.v_progress_step);                                        
        self.progress_label.setText(p_msg)
        self.progress.setLabel(self.progress_label)                     

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    pubblica_form_report("W:\\source\\DO-Documenti SMILE\\Sviluppo\\Form\\DO3000401F-Gestione documento.fmb",
                         "C:\\MGrep\\",
                         "1")        