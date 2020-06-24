# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 31/01/2020
 Descrizione...: Programma che scarica dal server iAS12g Oracle un sorgente form-report in una specifica directory
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file download_from_server_ui.py è ricavato partendo da download_from_server_ui.ui 
"""

#Librerie sistema
import sys
import os
import subprocess
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from download_from_server_ui import Ui_download_from_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
       
class download_from_server_class(QtWidgets.QMainWindow):
    """
        Esegue download oggetto da iAS12g
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(download_from_server_class, self).__init__()
        self.ui = Ui_download_from_window()
        self.ui.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()        
                            
    def slot_b_destination_dir(self):
        """
          selezione della directory di destinazione
        """        
        dirName = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory")
        if dirName != "":
            self.ui.e_destination_dir.setText( dirName )    
            
    def slot_b_start_download(self):
        """
           esegue il download dell'oggetto indicato
        """
        if self.ui.e_source.displayText() == '':
            message_error('You must enter a source file name with suffix!')
            return None
        
        if self.ui.e_destination_dir.displayText() == '':
            message_error('You must enter a destination dir!')
            return None 
        
        # controllo che il file di destinazione non esista; questo perché al termine del download solo controllando la presenza del file
        # potrò dire che il download è stato correttamente eseguito        
        v_sorgente = self.ui.e_source.displayText()            
        v_destinazione = os.path.join(self.ui.e_destination_dir.displayText() + '/' + v_sorgente)        
        if os.path.isfile(v_destinazione):
            message_error("Destination file already exists!")                
            return None        
        
        #imposto i nomi dei file su cui ridirigere output dei comandi (in questo modo non escono le brutte window di dos)
        v_sshoutput = open(os.path.join(self.o_preferenze.work_dir, 'sshoutput.txt'), 'w')
        v_sshoutputerror = open(os.path.join(self.o_preferenze.work_dir, 'sshoutputerror.txt'), 'w')
        v_sshinput = ''
        
        # eseguo il download
        try:
            # scarico il file nella directory indicata            
            v_ip = '10.0.4.14'
            v_pwd = self.o_preferenze.v_server_password_iAS
            v_command = 'echo y | utility_prog\\pscp -pw ' + v_pwd + ' oracle@' + v_ip + ':/appl/source/' + v_sorgente + ' ' + v_destinazione                    
            v_ssh = subprocess.Popen(v_command, shell=True, stdin=subprocess.PIPE, stdout=v_sshoutput, stderr=v_sshoutputerror)
            v_ssh.communicate(v_sshinput)
            # controllo se il file è stato effettivamente scaricato
            if os.path.isfile(v_destinazione):                
                message_info('Download finished!')
            else:
                message_error('Error to download ' + self.ui.e_source.displayText() + '!')
        except:
            message_error('Error to download ' + self.ui.e_source.displayText() + '!')
            return None
                                                                                
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = download_from_server_class() 
    application.show()
    sys.exit(app.exec())        