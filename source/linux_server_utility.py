# -*- coding: UTF-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 19/06/2020
 Descrizione...: Set di utility per consultare situazione di un server linux dove installato DB Oracle                 
   
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file linux_server_ui.py è ricavato partendo da linux_server_ui.ui 
"""

#Librerie di data base
import  cx_Oracle
#Libreria sistema
import  os
import  sys
import  subprocess
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from linux_server_utility_ui import Ui_linux_server_window
#Librerie interne MGrep
from utilita import message_error, message_info, message_question_yes_no
from preferenze import preferenze

class linux_server_class(QtWidgets.QMainWindow, Ui_linux_server_window):
    """
       Situazione spazio disco di un server linux 
            p_ip_server      = Indirizzo IP del server
            p_pwd            = Password            
    """
    def __init__(self):                
        # incapsulo la classe grafica da qtdesigner
        super(linux_server_class, self).__init__()        
        self.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()        
                
    def slot_action_disc_usage(self):
        """
           Carica nelle varie sezioni lo spazio disco occupato
        """
        # attivo la clessidra sulla freccia del mouse
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))                
        
        # spazio disco icom_815
        self.e_icom_815.setText( self.spazio_disco("10.0.4.10", self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco backup_815
        self.e_backup_815.setText( self.spazio_disco("10.0.4.11", self.o_preferenze.v_server_password_DB) )
        
        # spazio disco backup_2_815
        self.e_backup_2_815.setText( self.spazio_disco("10.0.4.12", self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco ias_smile_reale
        self.e_ias_smile_reale.setText( self.spazio_disco("10.0.4.14", self.o_preferenze.v_server_password_iAS) )                
        
        # spazio disco ias_smile_backup
        self.e_ias_smile_backup.setText( self.spazio_disco("10.0.47.47", self.o_preferenze.v_server_password_iAS) )                        
        
        # spazio disco ias_smile_backup2
        self.e_ias_smile_backup2.setText( self.spazio_disco("10.0.47.45", self.o_preferenze.v_server_password_iAS) )                                
        
        QtWidgets.QApplication.restoreOverrideCursor()        
        
    def spazio_disco(self, p_ip_server, p_pwd):        
        """
           Funzione che esegue il comando "df -h" sul server indicato e lo restituisce come stringa di output
           Attenzione! Utente di collegamento è oracle
        """
        #imposto i nomi dei file su cui ridirigere output dei comandi (in questo modo non escono le brutte window di dos)
        v_sshoutput = open(os.path.join(self.o_preferenze.work_dir, 'sshoutput.txt'), 'w')
        v_sshoutputerror = open(os.path.join(self.o_preferenze.work_dir, 'sshoutputerror.txt'), 'w')
        v_sshinput = ''
                
        try:
            #spazio del disco. Il comando vero e proprio è "df -h"
            v_command = 'echo y | utility_prog\\plink -pw ' + p_pwd + ' oracle@' + p_ip_server + ' df -h '            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Plink command error on ' + p_ip_server + '!')
            return 'ko'
        
        # leggo il risultato e lo visualizzo 
        return open(self.o_preferenze.work_dir + '\\sshoutput.txt', 'r').read()    
    
    def slot_action_top_sessions(self):
        """               
           Carica nelle varie sezioni il risultato del comando top sessions
        """
        # attivo la clessidra sulla freccia del mouse
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))                
        
        # spazio disco icom_815
        self.e_icom_815.setText( self.top("10.0.4.10",self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco backup_815
        self.e_backup_815.setText( self.top("10.0.4.11",self.o_preferenze.v_server_password_DB) )
        
        # spazio disco backup_2_815
        self.e_backup_2_815.setText( self.top("10.0.4.12",self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco ias_smile_reale
        self.e_ias_smile_reale.setText( self.top("10.0.4.14",self.o_preferenze.v_server_password_iAS) )                
        
        # spazio disco ias_smile_backup
        self.e_ias_smile_backup.setText( self.top("10.0.47.47",self.o_preferenze.v_server_password_iAS) )                        
        
        # spazio disco ias_smile_backup2
        self.e_ias_smile_backup2.setText( self.top("10.0.47.45",self.o_preferenze.v_server_password_iAS) )                                
        
        QtWidgets.QApplication.restoreOverrideCursor()        
        
    def top(self, p_ip_server, p_pwd):        
        """
           Funzione che esegue il comando "top" sul server indicato e lo restituisce come stringa di output
           Nello specifico l'opzione -b indica di mandare l'output sul file e -n il numero di iterazioni da svolgere 
           Attenzione! Utente di collegamento è oracle
        """
        #imposto i nomi dei file su cui ridirigere output dei comandi (in questo modo non escono le brutte window di dos)
        v_sshoutput = open(os.path.join(self.o_preferenze.work_dir, 'sshoutput.txt'), 'w')
        v_sshoutputerror = open(os.path.join(self.o_preferenze.work_dir, 'sshoutputerror.txt'), 'w')
        v_sshinput = ''
                
        try:
            #comando top con opzione -b (esecuzione in batch) e iterazioni 1
            v_command = 'echo y | utility_prog\\plink -pw ' + p_pwd + ' oracle@' + p_ip_server + ' top -b -n 1 '            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Plink command error on ' + p_ip_server + '!')
            return 'ko'
        
        # leggo il risultato e lo visualizzo 
        return open(self.o_preferenze.work_dir + '\\sshoutput.txt', 'r').read()   
    
    def slot_show_folder_ora02(self):
        """
           Mostra il contenuto della cartella ora02 dove sono presenti i file di journaling che crea Oracle
           In realtà esiste anche la cartella gemella ora03
           Viene eseguito solo per i server dove montato Oracle DB
        """
        # attivo la clessidra sulla freccia del mouse
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))                
        
        # spazio disco icom_815
        self.e_icom_815.setText( self.folder_ora02("10.0.4.10",self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco backup_815
        self.e_backup_815.setText( self.folder_ora02("10.0.4.11",self.o_preferenze.v_server_password_DB) )
        
        # spazio disco backup_2_815
        self.e_backup_2_815.setText( self.folder_ora02("10.0.4.12",self.o_preferenze.v_server_password_DB) )        
        
        # spazio disco ias_smile_reale
        self.e_ias_smile_reale.setText( "" )                
        
        # spazio disco ias_smile_backup
        self.e_ias_smile_backup.setText( "" )                        
        
        # spazio disco ias_smile_backup2
        self.e_ias_smile_backup2.setText( "" )                                        
        
        QtWidgets.QApplication.restoreOverrideCursor()                
        
    def folder_ora02(self, p_ip_server, p_pwd):        
        """
           Funzione che esegue il comando "ls" sul server indicato e lo restituisce come stringa di output           
           Attenzione! Utente di collegamento è oracle
        """
        #imposto i nomi dei file su cui ridirigere output dei comandi (in questo modo non escono le brutte window di dos)
        v_sshoutput = open(os.path.join(self.o_preferenze.work_dir, 'sshoutput.txt'), 'w')
        v_sshoutputerror = open(os.path.join(self.o_preferenze.work_dir, 'sshoutputerror.txt'), 'w')
        v_sshinput = ''
                
        try:
            #comando list con opzione verticale (-l) e unità di misura megabyte (-h)
            v_command = 'echo y | utility_prog\\plink -pw ' + p_pwd + ' oracle@' + p_ip_server + ' ls -lh /ora02/arch/'            
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
        except:
            message_error('Plink command error on ' + p_ip_server + '!')
            return 'ko'
        
        # leggo il risultato e lo visualizzo 
        return open(self.o_preferenze.work_dir + '\\sshoutput.txt', 'r').read()                 

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    application = linux_server_class()    
    application.show()
    sys.exit(app.exec())         
    