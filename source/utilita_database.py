# -*- coding: utf-8 -*-

"""
  Creato da.....: Marco Valaguzza
  Piattaforma...: Python3.6 con libreria pyqt5
  Data..........: 01/10/2017
  Descrizione...: Libreria funzioni per estrazioni strutture ed altro dai DB Oracle e SQLite
"""

# Libreria sqlite
import sqlite3
# Libreria delle date
import datetime
# Libreria oracle
import cx_Oracle
#Librerie interne MGrep
from utilita import message_error, message_question_yes_no, message_info

def nomi_colonne_istruzione_sql(p_db_cursor):
    """
        Restituisce elenco delle colonne di una qualsiasi query sql
        p_db_cursor = cursore aperto ad un db             
    """
    v_tab = []
    for i in range(0, len(p_db_cursor.description)):
        v_tab.append(p_db_cursor.description[i][0])    
        
    return v_tab

def estrae_struttura_tabella_oracle(p_type,
                                    p_db_cursor,
                                    p_user_db,
                                    p_table_name):
    """
        Restituisce informazioni su tabelle DB in base al tipo di elaborazione richiesta
            p_type = 'c' --> restituisce ddl per create table
                   = 'i' --> restituisce insert senza values della table
                   = 's' --> restituisce select senza where
                   = 'b' --> restituisce una lista con i riferimenti posizionali alle colonne blob
                   = 'e' --> restituisce il riferimento alla colonna che contiene l'estensione dei file
            p_db_cursor = cursore aperto ad un db oracle
            p_user_db    = schema di riferimento (es. SMILE)
            p_table_name = nome della tabella da analizzare
    """
    def estrae_struttura():
        v_table_structure = 'CREATE TABLE ' + p_table_name + '('
        v_1a_volta=True
        for row in p_db_cursor:
            v_column_name = row[0]
            v_data_type = row[1]
            v_data_precision = row[2]
            v_data_scale = row[3]
            v_char_length = row[4]

            if v_1a_volta:
                v_1a_volta=False
            else:
                v_table_structure += ','

            v_table_structure += v_column_name + ' '
            if v_data_type == 'NUMBER':
                if v_data_precision is None:
                    v_table_structure += 'INTEGER'
                else:
                    v_table_structure += v_data_type + '(' + str(v_data_precision) + ',' + str(v_data_scale) + ')'
            elif v_data_type in ('DATE','CLOB','BLOB'):
                v_table_structure += v_data_type
            else:
                v_table_structure += v_data_type + '(' + str(v_char_length) + ')'
        v_table_structure += ')'

        return v_table_structure

    def estrae_select():
        v_select = 'SELECT '
        v_1a_volta=True
        for row in p_db_cursor:
            v_column_name = row[0]

            if v_1a_volta:
                v_1a_volta=False
            else:
                v_select += ','

            v_select += v_column_name + ' '

        v_select += ' FROM ' + p_table_name
        return v_select

    def estrae_insert():
        v_select = 'INSERT INTO ' + p_table_name + '('
        v_1a_volta=True
        for row in p_db_cursor:
            v_column_name = row[0]

            if v_1a_volta:
                v_1a_volta=False
            else:
                v_select += ','

            v_select += v_column_name + ' '

        v_select += ') VALUES('
        return v_select

    def ricerca_posizioni_blob():
        v_lista = []
        v_progressivo = 0
        for row in p_db_cursor:
            v_progressivo += 1
            if row[1] == 'BLOB':
                v_lista.append(v_progressivo)

        return v_lista

    def ricerca_campo_estensione_file():
        v_estensione = 0
        v_progressivo = 0
        for row in p_db_cursor:
            v_progressivo += 1
            if row[0] == 'EXTEN_CO':
                v_estensione = v_progressivo

        return v_estensione

    p_db_cursor.prepare('''SELECT COLUMN_NAME, DATA_TYPE, DATA_PRECISION , DATA_SCALE, CHAR_LENGTH
                           FROM   ALL_TAB_COLUMNS
                           WHERE  OWNER=:p_user_db AND TABLE_NAME=:p_table_name ORDER BY COLUMN_ID''')
    p_db_cursor.execute(None, {'p_user_db' : p_user_db, 'p_table_name' : p_table_name})

    #estre create table
    if p_type == 'c':
        return str(estrae_struttura())
    elif p_type == 's':
        return str(estrae_select())
    #estrae insert
    elif p_type == 'i':
        return str(estrae_insert())
    #estrae posizioni blob
    elif p_type == 'b':
        return ricerca_posizioni_blob()
    #estrae posizione del campo exten_co che contiene estensione del blob
    elif p_type == 'e':
        return ricerca_campo_estensione_file()

def estrae_struttura_tabella_sqlite(p_type,
                                    p_sqlite_cur,
                                    p_table_name):
    """
        Restituisce informazioni su tabelle DB SQLite in base al tipo di elaborazione richiesta
            p_type = 'c' --> restituisce ddl per create table
                   = 's' --> restituisce select senza where
                   = 'i' --> restituisce insert senza values della table
                   = 'h' --> restituisce insert con parametri di values (es. insert into cancellami100(AZIEN_CO, DATA_DA) VALUES(:1,TO_DATE(:2,'RRRR-MM-DD HH24:MI:SS'))
                   = 'd' --> restituisce una lista con i riferimenti posizionali alle colonne di tipo data
                   = '1' --> restituisce una lista con elenco delle colonne
            p_sqlite_cur = cursore aperto ad un db sqlite
            p_table_name = nome della tabella da analizzare
    """

    #restituisce ddl create table
    if p_type == 'c':
        p_sqlite_cur.execute("SELECT sql FROM sqlite_master WHERE name='" + p_table_name + "'")
        return str(p_sqlite_cur.fetchone()[0])
    #restituisce una select con i nomi di campi di tabella ma senza where
    elif p_type == 's':
        p_sqlite_cur.execute("SELECT * FROM " + p_table_name + " WHERE 1=0")
        v_select = 'SELECT '
        v_1a_volta = True
        for member in p_sqlite_cur.description:
            if v_1a_volta:
                v_1a_volta = False
            else:
                v_select += ','
            v_select += member[0]

        v_select += ' FROM ' + p_table_name
        return v_select
    #restituisce insert senza values della table
    elif p_type == 'i':
        p_sqlite_cur.execute("SELECT * FROM " + p_table_name + " WHERE 1=0")
        v_select = 'INSERT INTO ' + p_table_name + '('
        v_1a_volta = True
        for member in p_sqlite_cur.description:
            if v_1a_volta:
                v_1a_volta = False
            else:
                v_select += ','
            v_select += member[0]

        v_select += ') VALUES('
        return v_select
    #restituisce una lista con i nomi di tutte le colonne della tabella
    elif p_type == '1':
        p_sqlite_cur.execute("SELECT * FROM " + p_table_name + " WHERE 1=0")
        v_lista = []
        for member in p_sqlite_cur.description:
            v_lista.append(member[0])

        return v_lista
    #restituisce una lista con le posizioni dei campi di tipo Data
    elif p_type == 'd':
        p_sqlite_cur.execute("pragma table_info('" + p_table_name + "')")
        v_lista = []
        v_progressivo = 0
        for row in p_sqlite_cur:
            if row[2] == 'DATE':
                v_lista.append(v_progressivo)
            v_progressivo += 1

        return v_lista
    #restituisce una stringa di insert con la sezione values compilata a parametri
    elif p_type == 'h':
        p_sqlite_cur.execute("pragma table_info('" + p_table_name + "')")
        #v_insert conterrà la prima parte con nomi dei campi
        v_insert = 'INSERT INTO ' + p_table_name + '('
        #v_values conterrà la parte con tutti i parametri; i campi dati vengono formattati con la to_date
        v_values = ') VALUES('
        v_progressivo = 1
        v_1a_volta = True
        for row in p_sqlite_cur:
            if v_1a_volta:
                v_1a_volta = False
            else:
                v_insert += ','
                v_values += ','

            v_insert += row[1]

            if row[2] == 'DATE':
                v_values += "TO_DATE(:" + str(v_progressivo) + ",'RRRR-MM-DD HH24:MI:SS')"
            else:
                v_values += ':' + str(v_progressivo)

            v_progressivo += 1

        return v_insert + v_values + ')'

def estrae_elenco_tabelle_oracle(p_type,
                                 p_user_db,
                                 p_password_db,
                                 p_dsn_db):
    """
        Restituisce una lista delle tabelle contenute in un DB Oracle
            p_type = '1' --> restituisce lista tabelle
            p_sqlite_db_name = nome file del DB SQLite
    """
    v_oracle_db = cx_Oracle.connect(user=p_user_db, password=p_password_db, dsn=p_dsn_db)
    v_oracle_cursor = v_oracle_db.cursor()

    v_lista = []
    for row in v_oracle_cursor.execute("SELECT TABLE_NAME FROM ALL_TABLES WHERE OWNER='" + p_user_db + "' ORDER BY TABLE_NAME"):
        v_lista.append(row[0])

    #Chiuso la connessione
    v_oracle_cursor.close()
    #Restituisco la lista
    return v_lista

def killa_sessione(p_sid,
                   p_serial,
                   p_oracle_user_sys,
                   p_oracle_password_sys,
                   p_oracle_dsn_real):
    """
        killa la sessione oracle dalla coppia p_sid e p_serial
    """
    if message_question_yes_no("Do you want to kill the selected session?") == 'Yes':
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=p_oracle_user_sys, password=p_oracle_password_sys, dsn=p_oracle_dsn_real, mode=cx_Oracle.SYSDBA)
            v_ok = True
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            v_ok = False

        if v_ok:
            v_cursor = v_connection.cursor()
            v_cursor.execute("ALTER SYSTEM KILL SESSION '" + str(p_sid).strip() + "," + str(p_serial).strip() + "'")
            v_cursor.close()
            v_connection.close()
            message_info('The session is being closed.')

def estrae_elenco_tabelle_sqlite(p_type,
                                 p_sqlite_db_name):
    """
        Restituisce una lista delle tabelle contenute in un SQLite DB
            p_type = '1' --> restituisce lista tabelle
            p_sqlite_db_name = nome file del DB SQLite
    """
    v_sqlite_conn = sqlite3.connect(database=p_sqlite_db_name)
    v_sqlite_cur = v_sqlite_conn.cursor()

    v_lista = []
    for row in v_sqlite_cur.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        v_lista.append(row[0])

    #Chiuso la connessione
    v_sqlite_conn.close()
    #Restituisco la lista
    return v_lista

class t_report_class():
    """
       Classe per la gestione di ut_repor in database sqlite 
    """    
    def __init__(self, p_db_name):
        """
           Creo se non presente la tabella ut_repor nel db p_db_name
        """
        if p_db_name == 'MEMORY':
            self.conn = sqlite3.connect(':memory:')
        else:
            self.conn = sqlite3.connect(database=p_db_name)
        self.curs = self.conn.cursor()
        self.curs.execute("""CREATE TABLE IF NOT EXISTS 
                             UT_REPORT (FNAME_CO TEXT NOT NULL,
                                        PAGE_NU  NUMBER NOT NULL,
                                        POSIZ_NU NUMBER NOT NULL,
                                        CREAZ_DA DATETIME,
                                        CAMPO1   TEXT, 
                                        CAMPO2   TEXT,
                                        CAMPO3   TEXT,
                                        CAMPO4   TEXT,
                                        CAMPO5   TEXT,
                                        CAMPO6   TEXT,
                                        CAMPO7   TEXT,
                                        CAMPO8   TEXT,
                                        CAMPO9   TEXT,
                                        CAMPO10  TEXT,
                                        CAMPO11  TEXT,
                                        CAMPO12  TEXT,
                                        CAMPO13  TEXT,
                                        CAMPO14  TEXT,
                                        CAMPO15  TEXT,
                                        CAMPO16  TEXT,
                                        CAMPO17  TEXT,
                                        CAMPO18  TEXT,
                                        CAMPO19  TEXT,
                                        CAMPO20  TEXT,
                                        CAMPO21  REAL,
                                        CAMPO22  REAL,
                                        CAMPO23  REAL,
                                        CAMPO24  REAL,
                                        CAMPO25  REAL,
                                        CAMPO26  REAL,
                                        CAMPO27  REAL,
                                        CAMPO28  REAL,
                                        CAMPO29  REAL,
                                        CAMPO30  REAL,
                                        
                                        PRIMARY KEY(FNAME_CO, PAGE_NU, POSIZ_NU)
                          )""")
        
        # creo una lista con i nomi delle colonne di tabella. Essa mi servirà per costriure il dizionario
        # contentente il record in formato mnemonico letto dalla tabella
        self.struct = estrae_struttura_tabella_sqlite('1', self.curs, 'UT_REPORT')
        
    def execute(self, p_sql_command, p_parameter):
        """
           Esegue un comando sql 
        """
        self.curs.execute(p_sql_command, p_parameter)
        
    def commit(self):
        """
           Esegue la commit
        """
        self.curs.execute('COMMIT')
    
    def decode(self, p_row):
        """
           In input riceve il record di ut_report e restituisce un 
           dizionario con nome campo e valore
        """
        if p_row != None:
            x = 0
            # pulisco il dizionario
            v_rec = {}
            # carico il dizionario con il contenuto del record
            for field in p_row:
                v_rec[self.struct[x]] = field
                x += 1
            # restituisco il dizionario    
            return v_rec
        else:
            return None
    
    def new_page(self, p_fname_co):
        """
           Crea e restituisce id di una nuova pagna
        """
        self.curs.execute('SELECT IFNULL(MAX(PAGE_NU),0) + 1 FROM UT_REPORT WHERE FNAME_CO = ?', [p_fname_co])
        v_new_page = self.curs.fetchone()[0]
        v_data_sistema = datetime.datetime.now()
        self.curs.execute('INSERT INTO UT_REPORT(FNAME_CO, PAGE_NU, POSIZ_NU, CREAZ_DA) VALUES(?, ?, ?, ?)', (p_fname_co, v_new_page, 0, v_data_sistema) )
        return v_new_page
    
    def delete_page(self, p_fname_co, p_page_nu):
        """
           Cancella una pagina
        """
        self.curs.execute('DELETE FROM UT_REPORT WHERE FNAME_CO = ? AND PAGE_NU=?', (p_fname_co, p_page_nu) )
        
    def insert(self, p_commit, p_fname_co, p_page_nu, 
                     p_campo1=None, p_campo2=None, p_campo3=None, p_campo4=None, p_campo5=None, p_campo6=None, p_campo7=None, p_campo8=None, p_campo9=None,p_campo10=None,
                     p_campo11=None,p_campo12=None,p_campo13=None,p_campo14=None,p_campo15=None,p_campo16=None,p_campo17=None,p_campo18=None,p_campo19=None,p_campo20=None,
                     p_campo21=None,p_campo22=None,p_campo23=None,p_campo24=None,p_campo25=None,p_campo26=None,p_campo27=None,p_campo28=None,p_campo29=None,p_campo30=None):
        """
           Inserisce nuova riga nel report
        """
        self.curs.execute('SELECT IFNULL(MAX(POSIZ_NU),0) + 1 FROM UT_REPORT WHERE FNAME_CO = ? AND PAGE_NU=?', (p_fname_co,p_page_nu))
        v_new_posiz = self.curs.fetchone()[0]
        v_data_sistema = datetime.datetime.now()
        self.curs.execute("""INSERT INTO UT_REPORT(FNAME_CO, PAGE_NU, POSIZ_NU, CREAZ_DA,
                                                   CAMPO1, CAMPO2, CAMPO3, CAMPO4, CAMPO5, CAMPO6, CAMPO7, CAMPO8, CAMPO9, CAMPO10,
                                                   CAMPO11,CAMPO12,CAMPO13,CAMPO14,CAMPO15,CAMPO16,CAMPO17,CAMPO18,CAMPO19,CAMPO20,
                                                   CAMPO21,CAMPO22,CAMPO23,CAMPO24,CAMPO25,CAMPO26,CAMPO27,CAMPO28,CAMPO29,CAMPO30)
                                            VALUES(?, ?, ?, ?,
                                                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                                                   ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)       
                          """, (p_fname_co, p_page_nu, v_new_posiz, v_data_sistema, 
                                p_campo1, p_campo2, p_campo3, p_campo4, p_campo5, p_campo6, p_campo7, p_campo8, p_campo9,p_campo10,
                                p_campo11,p_campo12,p_campo13,p_campo14,p_campo15,p_campo16,p_campo17,p_campo18,p_campo19,p_campo20,
                                p_campo21,p_campo22,p_campo23,p_campo24,p_campo25,p_campo26,p_campo27,p_campo28,p_campo29,p_campo30 ) ) 
        
        if p_commit:
            self.commit()
        
    def copy_page_to_new_page(self, p_fname_co, p_from_page, p_to_page):
        """
           Copia una pagina di UT_REPORT dentro un'altra. La pagina di arrivo deve avere il numero già staccato
        """
        self.curs.execute("""INSERT INTO UT_REPORT
                             SELECT ?, ?, POSIZ_NU, CREAZ_DA,
                                    CAMPO1, CAMPO2, CAMPO3, CAMPO4, CAMPO5, CAMPO6, CAMPO7, CAMPO8, CAMPO9, CAMPO10,
                                    CAMPO11,CAMPO12,CAMPO13,CAMPO14,CAMPO15,CAMPO16,CAMPO17,CAMPO18,CAMPO19,CAMPO20,
                                    CAMPO21,CAMPO22,CAMPO23,CAMPO24,CAMPO25,CAMPO26,CAMPO27,CAMPO28,CAMPO29,CAMPO30                       
                             FROM   UT_REPORT
                             WHERE  PAGE_NU = ?
                               AND  POSIZ_NU > 0
                          """, (p_fname_co, p_to_page, p_from_page) )    
    
    def count_row(self, p_fname_co, p_page):
        """
           Restituisce il numero di righe valide (con posiz_nu > 0) presenti in una pagina 
        """
        self.curs.execute('SELECT COUNT(*) FROM UT_REPORT WHERE FNAME_CO = ? AND PAGE_NU=?', (p_fname_co, p_page))
        return self.curs.fetchone()[0]
        
    def drop(self):
        """
           Droppo UT_REPORT dal database
        """
        self.curs.execute('DROP TABLE UT_REPORT');
        
    def close(self, p_commit):
        """
           Chiudo cursore e connessione. Se p_commit=True --> esegue la commit
        """
        if p_commit:
            self.curs.execute('COMMIT')
            
        self.curs.close()
        self.conn.close()
        

#test per la funzione di estrazione ddl tabella
if __name__ == "__main__":
    #
    # test ut_repor
    #
    # droppo la tabella
    #t_report = t_report_class('test.db')
    #t_report.drop()
    #del t_report
    # apro t_report in memoria
    #t_report = t_report_class("file::memory:?cache=shared")
    t_report = t_report_class('MEMORY')
    #print(t_report.new_page())
    #t_report.delete_page(2)
    # creo una nuova pagina della sezione 'prova'
    v_page = t_report.new_page('prova')
    # inserisco un record con relativa commit
    t_report.insert(True, 'prova', v_page, p_campo1='1', p_campo21=10)
    # leggo tutti i record caricati in t_report. Il dizionario "rec" contiene il record letto
    t_report.execute('SELECT * FROM UT_REPORT', '')
    v_matrice = t_report.curs.fetchall()
    for v_row in v_matrice:
        v_record = t_report.decode(v_row)
        print(v_record['FNAME_CO'] + ',' + str(v_record['PAGE_NU']) + ',' + str(v_record['POSIZ_NU']))
        
    # attendo la pressione del tasto "q"
    """
    while True:
        a = input()
        if a == 'q':
            break
    """
    # chiudo t_report senza commit    
    t_report.close(False)