# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 23/04/2020
 Descrizione...: Programma per visualizzare elenco delle percentuali sessioni occupate.
                 Il funzionamento è il seguente:
                 - Viene caricata nella tabella UT_REPORT del DB di formato SQLite la situazione iniziale delle sessioni attive
                 - All'atto della richiesta di calcolo, viene caricato l'elenco delle sessioni attive in una nuova pagina
                   e viene svolto un confronto con la precedente, calcolando la differenza in termini di tempo di CPU occupata 
                   e traducendo questa differenza in percentuale. 
                 - Ogni volta che viene richiesto un ricalcolo, la pagina di partenza viene sostituita dalla pagina precedente in modo
                   che nella pagina1 ci sia sempre un punto di confronto.
                 Attenzione! Non vengono estratte tutte le sessioni perché ci sono processi oracle che non interessano.
                  
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_top_sessions_ui.py è ricavato partendo da oracle_top_sessions_ui.ui 
"""

#Librerie sistema
import sys
import os
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets
from oracle_top_sessions_ui import Ui_oracle_top_sessions_window
#Librerie interne MGrep
from utilita_database import ut_report_class
from preferenze import preferenze
from utilita import message_error, message_info

class oracle_top_sessions_class(QtWidgets.QMainWindow):
    """
        Oracle session 
    """       
    def __init__(self):
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # apro ut_report (due pagine)
        self.ut_report = ut_report_class(self.o_preferenze.name_file_for_db_cache)
        self.page1 = self.ut_report.new_page()
        self.page2 = self.ut_report.new_page()
        
        # incapsulo la classe grafica da qtdesigner        
        super(oracle_top_sessions_class, self).__init__()
        self.ui = Ui_oracle_top_sessions_window()
        self.ui.setupUi(self)        
        
        # siccome il successivo carico delle poplist fa scattare l'evento di change con conseguente ricarico delle tabelle, 
        # la seguente variabile indica che siamo in fase di partenza del form
        self.v_load_form = True
        
        # carico la lista dei parametri di metrica disponibili 
        # (attenzione! le metriche vengono cercate per descrizione quindi attenzione a come si modificano)
        self.ui.e_parameter.addItem('CPU used by this session')
        self.ui.e_parameter.addItem('physical reads')
        self.ui.e_parameter.addItem('db block gets')
        self.ui.e_parameter.addItem('recursive calls')        
        self.ui.e_parameter.addItem('consistent gets')        
        self.ui.e_parameter.addItem('redo size')
        self.ui.e_parameter.addItem('bytes sent via SQL*Net to client')
        self.ui.e_parameter.addItem('bytes received via SQL*Net from client')
        self.ui.e_parameter.addItem('SQL*Net roundtrips to/from client')
        self.ui.e_parameter.addItem('sorts (memory)')
        self.ui.e_parameter.addItem('sorts (disk)')
                
        # carico elenco dei server prendendolo dalle preferenze         
        for nome in self.o_preferenze.elenco_server:
            self.ui.e_server_name.addItem(nome)
            
        # eseguo il carico della prima pagina
        self.starter()        
        
        # reimposto la var che indica il termine del caricamento del form
        self.v_load_form = False
        
        # imposto un flag per indicare all'esterno che questa classe è in esecuzione. 
        # siccome sul DB non viene mai fatta una commit, esso rimane bloccato fino all'uscita del form
        self.v_app_top_session_open = True
                                                
    def starter(self):
        """
           Caricamento della pagina iniziale
        """    
        # cancello per sicurezza le pagine
        self.ut_report.delete_page(self.page1)
        self.ut_report.delete_page(self.page2)
        
        # carico in pagina1 di ut_report, il punto di partenza della situazione sessioni         
        self.load_from_oracle_top_sessions(self.page1)
        
        # visualizzo il contenuto della pagina1
        self.load_screen(self.page1)
        
        # setto la variabile di primo ciclo
        self.v_1a_volta = True        
                                                                
    def load_from_oracle_top_sessions(self, p_page):
        """
            Carica nella pagina di ut_report indicata da p_page la query delle sessioni 
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.ui.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []

        # apro cursori
        v_cursor = v_connection.cursor()
        
        # select per la ricerca degli oggetti invalidi        
        v_select = """select se.sid,
                             username,
                             status,
                             logon_time,
                             round ((sysdate-logon_time)*1440*60) logon_SECS,                             
                             value,
                             nvl(se.module, se.program) module_info,
                             se.sql_id,
                             (SELECT Min(sql_text) from V$SQL WHERE sql_id=se.sql_id) sql_text
                      from   v$session se,
                             v$sesstat ss,
                             v$statname sn
                      where  username IS NOT NULL
                        and  se.sid=ss.sid
                        and  sn.statistic#=ss.statistic#
                        and  sn.name in ('""" + self.ui.e_parameter.currentText() + """')
                   """        
                
        v_cursor.execute(v_select)        
        
        # salvo in ut_report 
        v_row = []
        for result in v_cursor:
            self.ut_report.insert(p_page_nu=p_page, 
                                  p_campo1=result[0], 
                                  p_campo2=result[1],
                                  p_campo3=result[2], 
                                  p_campo4=result[3], 
                                  p_campo5=result[4], 
                                  p_campo6=result[5], 
                                  p_campo7=result[6], 
                                  p_campo8=result[7], 
                                  p_campo9=result[8]) 
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
    def load_screen(self, p_page):            
        """
            Carica a video la pagina di ut_report indicata 
        """
        # carico in una tupla i dati
        self.ut_report.curs.execute("""SELECT CAMPO22, CAMPO1, CAMPO2, CAMPO3, CAMPO4, CAMPO6, CAMPO10, ROUND(CAMPO21,1), CAMPO5, CAMPO7, CAMPO8, CAMPO9
                                       FROM   UT_REPORT
                                       WHERE  PAGE_NU = ?
                                         AND  POSIZ_NU > 0
                                       ORDER BY CAMPO22 DESC, CAMPO3""", 
                                    [p_page])
        matrice_dati = self.ut_report.curs.fetchall()
        
        # lista contenente le intestazioni
        intestazioni = ['%','Sid','User name','Status','Logon','Value Now','Value Old','Variance','Logon Time','Module','SQL Id','SQL Text']                        
        # creo un oggetto modello-matrice che va ad agganciarsi all'oggetto grafico lista        
        self.lista_risultati = QtGui.QStandardItemModel()
        # carico nel modello la lista delle intestazioni
        self.lista_risultati.setHorizontalHeaderLabels(intestazioni)        
        # creo le colonne per contenere i dati
        self.lista_risultati.setColumnCount(len(intestazioni))        
        # creo le righe per contenere i dati
        self.lista_risultati.setRowCount(len(matrice_dati))        
        y =0
        # carico i dati presi dal db dentro il modello
        for row in matrice_dati:            
            x = 0                            
            for field in row:
                q_item = QtGui.QStandardItem()
                q_item.setText( str(field) )
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        # carico il modello nel widget        
        self.ui.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.ui.o_lst1.resizeColumnsToContents()   
    
    def calc_differenze(self):
        """
           Calcolo differenze tra pagina2 e pagina1
        """
        v_totale = 0 
        v_diffe = 0
        # scorro tutti i record presenti nella pagina2 estraendo le colonne SID e SESS_CPU_SECS (numero di secondi occupati)
        self.ut_report.curs.execute("""SELECT CAMPO1 VAL0, 
                                              CAMPO2 VAL1, 
                                              CAMPO6 VAL2, 
                                              POSIZ_NU VAL3 
                                        FROM  UT_REPORT 
                                        WHERE PAGE_NU = ? 
                                          AND POSIZ_NU> 0""", [self.page2])
        tabella = self.ut_report.curs.fetchall()    
        for row in tabella:
            # ricerco se presente nella pagina1 (elaborazione precedente) la stessa sessione con lo stesso username 
            self.ut_report.curs.execute("""SELECT POSIZ_NU VAL0, 
                                                  CAMPO6 VAL1 
                                           FROM   UT_REPORT 
                                           WHERE  PAGE_NU= ? 
                                             AND  CAMPO1 = ? 
                                             AND  CAMPO2 = ?""", (self.page1, row[0], row[1]) )
            rec = self.ut_report.curs.fetchone()
            if rec != None:
                # eseguo la differenza tra tempo attuale e tempo precedente
                v_diffe  = float(row[2]) - float(rec[1]);
                v_totale += v_diffe;
            
                # aggiorno la colonna10 della pagina2 che contiene il vecchio valore e la colonna21 che contiene la differenza
                self.ut_report.curs.execute("""UPDATE UT_REPORT 
                                               SET    CAMPO10 = ?, 
                                                      CAMPO21 = ? 
                                               WHERE  PAGE_NU = ? 
                                                 AND  POSIZ_NU= ?""", (rec[1], v_diffe, self.page2, row[3]) )
                
        # calcolo le percentuali rispetto al totale
        self.ut_report.curs.execute("""UPDATE UT_REPORT 
                                       SET    CAMPO22 = ROUND(CAMPO21 * 100 / ?,1) 
                                       WHERE  PAGE_NU = ?""", (v_totale, self.page2) )                                
            
    def slot_calculate(self):            
        """
            Eseguo il calcolo
            Il calcolo consiste nello:
               - spostare eventuale pagina2 dentro la pagina1, in modo da avere sempre nella pagina1 la situazione precedente
               - caricare la pagina2
               - confrontare la pagina2 con la pagina1, calcolando le differenze
               - visualizzare la pagina2            
        """
        # cancello la pagina1 e rinomino la pagina2 come se fosse pagina1
        if not self.v_1a_volta:            
            self.ut_report.delete_page(self.page1)
            self.ut_report.curs.execute('UPDATE UT_REPORT SET PAGE_NU=? WHERE PAGE_NU=?', (self.page1, self.page2) )
        
        # carico la nuova situazione delle sessioni dentro la pagina2
        self.load_from_oracle_top_sessions(self.page2)
        
        # calcolo la differenza tra la pagina2 e la pagina1
        self.calc_differenze()
        
        # visualizzo il risultato della pagina2
        self.load_screen(self.page2)
        
        # disattivo il flag di primo ciclo
        if self.v_1a_volta:
            self.v_1a_volta = False
                        
    def slot_change_server(self):            
        """
           E' stato cambiato il server di riferimento e quindi va caricato tutto da capo
        """    
        if not self.v_load_form:            
            self.starter() 
            
    def closeEvent(self, event):
        """
           Questo metodo si sovrappone al metoro interno della chiusura della finestra
        """        
        # indico tramite variabile globale che l'applicazione viene chiusa 
        # (questo perché se richiamata dall'esterno può girare solo un'istanza per volta)        
        self.v_app_top_session_open = False
        # chiudo il DB sqlite senza commit
        self.ut_report.close(False)
        # chiudo la finestra
        event.accept()
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_top_sessions_class() 
    application.show()
    sys.exit(app.exec())        