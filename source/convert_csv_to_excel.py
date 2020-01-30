# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 24/01/2020
 Descrizione...: Scopo del programma è prendere un file CSV e convertirlo nel rispettivo formato di Excel

 Note! Inserita conversione automatica delle celle numeriche (attenzione! Non conversione di colonne ma di celle!)
"""
#Librerie di sistema
import  os
import sys
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
#Libreria per export in excel
from    xlsxwriter.workbook import Workbook
#Moduli di progetto
from utilita import message_error, message_info, message_question_yes_no

def check_campo_numerico(valore):
    v_ok = True
    try:
        numero = float(valore.replace(',','.'))
    except:
        v_ok = False
    return v_ok

def campo_numerico(valore):
    return float(valore.replace(',','.'))

class convert_csv_to_excel(QtWidgets.QWidget):
    """
        Converte file csv in formato excel
        Va indicato attraverso l'instanziazione della classe:
            p_csv_file  = Nome del file csv
            p_separator = Carattere di separatore dei campi
    """
    def __init__(self,
                 p_csv_name,
                 p_csv_separator,
                 p_modalita_test):
        
        # rendo la mia classe una superclasse
        super(convert_csv_to_excel, self).__init__()                
        
        # creazione della wait window
        self.v_progress_step = 0
        self.progress = QtWidgets.QProgressDialog(self)        
        self.progress.setMinimumDuration(0)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Copy...")                
        
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
        
        # controllo sia stato indicato il separatore csv
        if p_csv_separator == '':
            message_error( 'Insert a csv separator!')
            return None
                
        #Spezzo il nome del file per ricavare il nome di destinazione e controllo che la destinazione non esista
        v_solo_nome_file = os.path.split(p_csv_name)[1]
        v_solo_directory = os.path.split(p_csv_name)[0]
        v_solo_nome_file_senza_suffisso = os.path.splitext(v_solo_nome_file)[0]
        v_suffisso_nome_file = os.path.splitext(v_solo_nome_file)[1]
        v_xls_name = v_solo_directory + '//' + v_solo_nome_file_senza_suffisso + '.xlsx'
        if os.path.isfile(v_xls_name):
            if message_question_yes_no("Destination file already exists. Do you to replace it?") == 'No':
                # esco dalla procedura perché utente ha deciso di non preseguire
                return None
            
        #Apro il file e conto le righe
        v_total_rows = 0
        with open(p_csv_name, encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_total_rows += 1

        #Calcolo l'1% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100

        #Creazione del file excel
        workbook = Workbook(v_xls_name)
        worksheet = workbook.add_worksheet()

        #Rileggo il file e converto da un formato all'altro
        v_progress = 0
        v_y = 0
        with open(p_csv_name,  encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_valori = v_line.split(p_csv_separator)
                v_x = 0
                for campo in v_valori:
                    if check_campo_numerico(campo):
                        worksheet.write(v_y, v_x, campo_numerico(campo))
                    else:
                        worksheet.write(v_y, v_x, campo)
                    v_x += 1
                v_y += 1
                #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
                if v_total_rows > 100:
                    v_progress += 1
                    if v_progress % v_rif_percent == 0:
                        self.avanza_progress( 'Total record to copy: ' + str(v_total_rows) )
                        
        #Chiusura del file e del db
        self.avanza_progress('Finalizing process...')
        workbook.close()
        #Messaggio finale
        message_info('File conversion completed!')
        
        return None
    
    def avanza_progress(self, p_msg):
        """
           Visualizza prossimo avanzamento sulla progress bar
        """
        self.v_progress_step += 1
        if self.v_progress_step <= 100:
            self.progress.setValue(self.v_progress_step);                                        
            self.progress_label.setText(p_msg)            

class convert_csv_clipboard_to_excel(QtWidgets.QWidget):
    """
        Converte il testo contenuto nella clipboard (appunti) nel formato di excel
        Va indicato attraverso l'instanziazione della classe:
            p_work_dir = Directory di lavoro
            p_separator = Carattere di separatore dei campi
    """
    def __init__(self,
                 p_work_dir,
                 p_csv_separator,
                 p_modalita_test):

        # rendo la mia classe una superclasse
        super(convert_csv_clipboard_to_excel, self).__init__()                
                
        # controllo sia stato indicato il separatore csv
        if p_csv_separator == '':
            message_error( 'Insert a csv separator!')
            return None

        # nome file di lavoro
        v_nome_file_di_lavoro = p_work_dir + '\\clipboard.csv'

        # definizione del file di destinazione (apertura della finestra di dialogo e richiesta del file di arrivo)
        #v_xls_name = p_work_dir + '\\clipboard.xlsx'        
        v_xls_name = QtWidgets.QFileDialog.getSaveFileName(self, "Save a Excel file","export.xlsx","XLSX (*.xlsx)") [0]                  
        if v_xls_name == "":            
            message_error("Not a valid file name is selected")
            return None    
        
        # creazione della wait window
        self.v_progress_step = 0
        self.progress = QtWidgets.QProgressDialog(self)        
        self.progress.setMinimumDuration(0)
        self.progress.setWindowModality(QtCore.Qt.WindowModal)
        self.progress.setWindowTitle("Copy...")                
        
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
            
        ###############################################
        # lettura della clipboard e scrittura in file
        ###############################################
        import ctypes

        CF_TEXT = 1

        kernel32 = ctypes.windll.kernel32
        user32 = ctypes.windll.user32

        user32.OpenClipboard(0)
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            file = open(v_nome_file_di_lavoro, 'wb')
            file.write(text.value)
            file.close()
            kernel32.GlobalUnlock(data_locked)
        else:
            message_error("Clipboard not contains csv format text")
            return None

        user32.CloseClipboard()
        ########################################

        #Apro il file e conto le righe
        v_total_rows = 0
        with open(v_nome_file_di_lavoro, encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_total_rows += 1

        #Calcolo l'1% che rappresenta lo spostamento della progress bar
        v_rif_percent = 0
        if v_total_rows > 100:
            v_rif_percent = v_total_rows // 100
        
        #Creazione del file excel
        workbook = Workbook(v_xls_name)
        worksheet = workbook.add_worksheet()

        #Rileggo il file e converto da un formato all'altro
        v_progress = 0
        v_y = 0
        with open(v_nome_file_di_lavoro,  encoding='latin-1', mode='r') as v_file:
            for v_line in v_file:
                v_valori = v_line.split(p_csv_separator)
                v_x = 0
                for campo in v_valori:
                    if check_campo_numerico(campo):
                        worksheet.write(v_y, v_x, campo_numerico(campo))
                    else:
                        worksheet.write(v_y, v_x, campo)
                    v_x += 1
                v_y += 1
                #Emetto percentuale di avanzamento ma solo se righe maggiori di 100
                if v_total_rows > 100:
                    v_progress += 1
                    if v_progress % v_rif_percent == 0:
                        self.avanza_progress( 'Total record to copy: ' + str(v_total_rows), False )                        

        #Chiusura del file e del db          
        self.avanza_progress('Finalizing process...',True)
        self.avanza_progress('Finalizing process...',True)
        workbook.close()
        #Messaggio finale
        message_info('File ' + v_xls_name + ' created!')

        #Il file di lavoro viene eliminatao
        os.remove(os.path.join(v_nome_file_di_lavoro))
         
        return None
    
    def avanza_progress(self, p_msg, p_final):
        """
           Visualizza prossimo avanzamento sulla progress bar
        """        
        if p_final:
            self.v_progress_step += 1
        else:
            if self.v_progress_step < 97:
                self.v_progress_step += 1
                
        self.progress.setValue(self.v_progress_step);                                        
        self.progress_label.setText(p_msg)               
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)    
    
    """
    app = convert_csv_to_excel("C:/MGrep/dualuse.csv",
                               ";",
                               True)                            
    """
    app = convert_csv_clipboard_to_excel("C:/Users/mvalaguz/Desktop/",
                                         "|",
                                         True)
