# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 11/12/2019
 Descrizione...: Classe per la gestione delle preferenze del programma MGrep
"""

import os
import platform
import base64

def cripta_testo(testo):
    """
       Cripta una stringa con la chiave mgrep. Il valore restituito è di tipo byte
    """
    key = 'mgrep_2020'
    enc = []
    for i in range(len(testo)):
        key_c = key[i % len(key)]
        enc_c = (ord(testo[i]) + ord(key_c)) % 256
        enc.append(enc_c)
    return base64.urlsafe_b64encode(bytes(enc))    

def decripta_testo(btesto):
    """
       decripta una serie di byte con la chiave mgrep. Il valore restituito è di tipo stringa
    """
    key = 'mgrep_2020'
    dec = []
    enc = base64.urlsafe_b64decode(btesto)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + enc[i] - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

class preferenze:
    def __init__(self):
        """
            Definizione delle proprietà della classe preferenze
        """
        # controllo su quale piattaforma viene eseguito il programma e identifico il prefisso
        if 'Windows' in platform.system():
            v_prefix = 'C:\\'
        else:
            v_prefix = ''
        
        # preferenze interne (da notare come tutti i nomi passano attraverso la funzione normpath 
        # che a seconda del sistema operativo normalizza i vari caratteri)
        self.work_dir = os.path.normpath(v_prefix + 'MGrep\\')
        self.name_file_for_db_cache = os.path.normpath(v_prefix + 'MGrep\\MGrep.db')
        self.favorites_file = os.path.normpath(v_prefix + 'MGrep\\favorites_files.txt')
        self.favorites_dirs = os.path.normpath(v_prefix + 'MGrep\\favorites_directories.txt')
        self.v_oracle_user_sys = 'SYS'
        
        # caricamento delle password da file criptati...se non trovate uscirà messaggio di avviso all'avvio di MGrep
        try:
            v_file = open('pwd\\mgrep_pwd_sys.pwd','r')
            v_pwd = decripta_testo( v_file.read() )
            self.v_oracle_password_sys = v_pwd
        except:
            self.v_oracle_password_sys = ''
        try:
            v_file = open('pwd\\mgrep_pwd_oracle_dba.pwd','r')
            v_pwd = decripta_testo( v_file.read() )
            self.v_server_password_DB = v_pwd
        except:
            self.v_server_password_DB = ''
        try:
            v_file = open('pwd\\mgrep_pwd_ias.pwd','r')
            v_pwd = decripta_testo( v_file.read() )        
            self.v_server_password_iAS = v_pwd
        except:
            self.v_server_password_iAS = ''

        # imposto default campi ricerca stringa
        self.stringa1 = ''
        self.stringa2 = ''
        self.pathname = 'W:/source'
        self.excludepath = '00-Standards e Guidelines,01-Moduli e Tabelle,02-Documentazione OLD,03-Template,04-FAQ,05-Manutenzioni e Trasferimenti DB,06-Aggiornamento_giornaliero,99-Prove,MO-SMILE Mobile'
        self.outputfile = os.path.normpath(v_prefix + 'MGrep\\MGrep_Result.csv')
        self.filter = '.fmb,.rdf'
        self.flsearch = True
        self.dboracle1 = 'SMILE/SMILE@BACKUP_815'
        self.dboracle2 = 'SMI/SMI@BACKUP_815'
        self.dbsearch = True
        # imposto default campi ricerca files
        self.filesearch = ''
        self.pathname2 = 'W:/source'
        self.excludepath2 = '00-Standards e Guidelines,01-Moduli e Tabelle,02-Documentazione OLD,03-Template,04-FAQ,05-Manutenzioni e Trasferimenti DB,06-Aggiornamento_giornaliero,99-Prove,MO-SMILE Mobile'
        self.filter2 = '.fmb,.rdf'
        # imposto default campi import-export
        self.table_name = ''
        self.dboracle = 'SMILE/SMILE@BACKUP_815'
        self.where_cond = ''
        self.sqlite_db = os.path.normpath(v_prefix + 'MGrep\\MGrepTransfer.db')
        self.table_excel = ''
        self.table_to_oracle = ''
        self.oracle_table = ''
        self.import_excel = ''
        self.excel_file = os.path.normpath(v_prefix + 'MGrep\\Exported_table.xlsx')
        self.csv_file = ''
        self.csv_separator = ';'        

        # preferenze posizione delle window
        self.l_windows_pos = []
        
        # preferenze elenco server
        self.elenco_server = ['ICOM_815','BACKUP_815','BACKUP_2_815']

    def carica(self):
        """
            carica le preferenze salvate dalla sessione precedente
        """

        def carica_riga_nel_campo():
            """
                legge la prossima riga del file e la carica nel campo ricevuto come oggetto ingresso
                il campo in ingresso è un widget di tipo testo
            """
            v_line = v_file.readline()
            v_line = v_line.rstrip('\n')
            return v_line

        # Crea la directory di lavoro dell'applicazione se non esiste: in essa verranno salvati i file delle preferenze
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        try:
            v_file = open(os.path.join(self.work_dir, 'MGrep.ini'), 'r')
            v_ok = True
        except:
            v_ok = False

        if v_ok:
            # --------------------------------
            #         RICERCA STRINGE
            # --------------------------------
            # stringa1
            self.stringa1 = carica_riga_nel_campo()
            # stringa2
            self.stringa2 = carica_riga_nel_campo()
            # pathname
            self.pathname = carica_riga_nel_campo()
            # output file
            self.outputfile = carica_riga_nel_campo()
            # db oracle1
            self.dboracle1 = carica_riga_nel_campo()
            # db oracle2
            self.dboracle2 = carica_riga_nel_campo()
            # file filter
            self.filter = carica_riga_nel_campo()
            # check box per esecuzione ricerche
            v_check = carica_riga_nel_campo()
            if v_check == '1':
                self.flsearch = True
            else:
                self.flsearch = False
            v_check = carica_riga_nel_campo()
            if v_check == '1':
                self.dbsearch = True
            else:
                self.dbsearch = False
            # dir escluse
            self.excludepath = carica_riga_nel_campo()
            # --------------------------------
            #       RICERCA FILES
            # --------------------------------
            # file
            self.filesearch = carica_riga_nel_campo()
            # pathname
            self.pathname2 = carica_riga_nel_campo()
            # file filter
            self.filter2 = carica_riga_nel_campo()
            # dir escluse
            self.excludepath2 = carica_riga_nel_campo()
            # --------------------------------
            #       IMPORT-EXPORT
            # --------------------------------
            # db oracle
            self.dboracle = carica_riga_nel_campo()
            # sqlite db name
            self.sqlite_db = carica_riga_nel_campo()
            # table name
            self.table_name = carica_riga_nel_campo()

            # where condition
            try:
                v_file_where = open(os.path.join(self.work_dir, 'where_condition.txt'), 'r')
                self.where_cond = v_file_where.read()
                v_file_where.close()
            except:
                pass

            # tabella
            self.table_excel = carica_riga_nel_campo()
            # foglio excel
            self.excel_file = carica_riga_nel_campo()
            # tabella oracle di destinazione
            self.table_to_oracle = carica_riga_nel_campo()
            # tabella oracle di partenza
            self.oracle_table = carica_riga_nel_campo()
            # foglio di excel di import
            self.import_excel = carica_riga_nel_campo()
            # csv file
            self.csv_file = carica_riga_nel_campo()
            # csv separatore
            self.csv_separator = carica_riga_nel_campo()
            
            # chiusura del file
            v_file.close()
        # --------------------------------
        #       CARICA I NOMI E LA POSIZIONE DELLE WINDOW PREFERITE
        # --------------------------------
        try:
            v_file = open(os.path.join(self.work_dir, 'favorites_window.txt'), 'r')
            v_ok = True
        except:
            v_ok = False

        if v_ok:
            for v_line in v_file:
                self.l_windows_pos.append( v_line.rstrip('\n').split() )
            v_file.close()

    def salva(self):
        """
            salva le preferenze della sessione
        """
        v_file = open(os.path.join(self.work_dir, 'MGrep.ini'), 'w')
        # --------------------------------
        #         RICERCA STRINGE
        # --------------------------------
        # stringa1
        v_file.write(self.stringa1 + '\n')
        # stringa2
        v_file.write(self.stringa2 + '\n')
        # pathname
        v_file.write(self.pathname + '\n')
        # output file
        v_file.write(self.outputfile + '\n')
        # db oracle1,2
        v_file.write(self.dboracle1 + '\n')
        v_file.write(self.dboracle2 + '\n')
        # filter file
        v_file.write(self.filter + '\n')
        # execute folder search
        if self.flsearch:
            v_file.write('1' + '\n')
        else:
            v_file.write('0' + '\n')
        # execute db search
        if self.dbsearch:
            v_file.write('1' + '\n')
        else:
            v_file.write('0' + '\n')
        # exclude dir
        v_file.write(self.excludepath + '\n')
        # --------------------------------
        #       RICERCA FILES
        # --------------------------------
        # file da ricercare
        v_file.write(self.filesearch + '\n')
        # pathname
        v_file.write(self.pathname2 + '\n')
        # filter file
        v_file.write(self.filter2 + '\n')
        # exclude dir
        v_file.write(self.excludepath2 + '\n')
        # --------------------------------
        #       IMPORT-EXPORT
        # --------------------------------
        v_file.write(self.dboracle + '\n')
        v_file.write(self.sqlite_db + '\n')
        v_file.write(self.table_name + '\n')

        # La where viene salvata in file a parte (in questo modo si preservano i caratteri di ritorno a capo)
        v_file_where = open(os.path.join(self.work_dir, 'where_condition.txt'), 'w')
        v_file_where.write(self.where_cond)

        v_file.write(self.table_excel + '\n')
        v_file.write(self.excel_file + '\n')

        v_file.write(self.table_to_oracle + '\n')
        v_file.write(self.oracle_table + '\n')

        v_file.write(self.import_excel + '\n')

        v_file.write(self.csv_file + '\n')
        v_file.write(self.csv_separator + '\n')        

        # Chiusura dei file
        v_file.close()
        v_file_where.close()
        
    def salva_pos_finestre(self):
        """
           Salva la dimensione e la posizione delle window
        """
        v_file = open(os.path.join(self.work_dir, 'favorites_window.txt'), 'w')
        for line in self.l_windows_pos:
            v_file.write(str(line) + '\n')
        v_file.close()

    def cancella_tutto():
        """
            cancella i files con le preferenze
        """
        def elimina_file(p_nome_file):
            try:
                os.remove(os.path.join(self.work_dir + '/' + p_nome_file))
            except:
                pass

        elimina_file('MGrep.ini')
        elimina_file('MGrep.db')
        elimina_file('temp_source_db.sql')
        elimina_file('where_condition.txt')
        elimina_file('favorites_files.txt')
        elimina_file('favorites_directories.txt')

# ------------------------
# test della classe
# ------------------------
if __name__ == "__main__":
    ###
    # Parte1 = Inizializzazione oggetto e stampa dei suoi default
    ###
    o_preferenze = preferenze()
    print('-'*100)
    print('Valori preferenze di default')
    print('-'*100)
    for index in o_preferenze.__dict__:
        print(index + ((40-len(index))*' ') + ' => ' + str(o_preferenze.__dict__[index]))
    ###
    # Parte2 = Caricamento dei valori attuali del file
    ###
    o_preferenze.carica()
    print('-'*100)
    print('Valori contenuti nel file preferenze')
    print('-'*100)
    for index in o_preferenze.__dict__:
        print(index + ((40-len(index))*' ') + ' => ' + str(o_preferenze.__dict__[index]))
    ###
    # Parte3 = Provo a salvare la dimensione delle windows
    ###
    #o_preferenze.l_windows_pos.append( ('My favorites files', 0, 5, 100, 200) )
    #o_preferenze.l_windows_pos.append( ('My favorites directories', 7, 10, 200, 300) )
    #o_preferenze.salva()
    #o_preferenze.carica()
    #print('-'*100)
    #print('Valori contenuti nel file preferenze')
    #print('-'*100)
    #for index in o_preferenze.__dict__:
    #    print(index + ((40-len(index))*' ') + ' => ' + str(o_preferenze.__dict__[index]))        
