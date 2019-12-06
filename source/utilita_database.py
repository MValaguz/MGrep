# -*- coding: utf-8 -*-

"""
  Creato da.....: Marco Valaguzza
  Piattaforma...: Python3.6 con libreria pyqt5
  Data..........: 01/10/2017
  Descrizione...: Libreria funzioni per estrazioni strutture ed altro dai DB Oracle e SQLite
"""

# Libreria sqlite
import sqlite3
# Libreria oracle
import cx_Oracle
#Librerie interne MGrep
from utilita import message_error, message_question_yes_no, message_info

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


#test per la funzione di estrazione ddl tabella
if __name__ == "__main__":
    #test funzione elenco tabelle oracle
    v_sqlite_conn = sqlite3.connect(database='C:\MGrep\MGrepTransfer.db')
    #Indico al db di funzionare in modalità byte altrimenti ci sono problemi nel gestire utf-8
    v_sqlite_conn.text_factory = str
    v_sqlite_cur = v_sqlite_conn.cursor()
    #Lettura del contenuto della tabella
    print('Istruzione insert con parametri da tabella SQLite ')
    print(estrae_struttura_tabella_sqlite('h', v_sqlite_cur, 'CANCELLAMI100'))
    v_sqlite_conn.close()
