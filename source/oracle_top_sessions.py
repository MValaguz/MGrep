# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 23/04/2020
 Descrizione...: Programma per visualizzare il carico del DB Oracle in termini di CPU ecc.
                 Contrariamente a quanto si possa immaginare, ottenere queste informazioni non è facile.
                 Le metriche che Oracle rende disponibili tramite la vista v$sesstat sono comulative, nel senso
                 che fanno riferimento al momento in cui vengono lette rispetto alla data-ora di accensione del sistema.
                 Se ad esempio leggo la metrica relativa all'occupazione della CPU (da non intendersi come CPU fisica ma
                 del motore di DB) della sessione MVALAGUZ in questo momento ottengo 10 come valore. Questo valore 
                 indica l'occupazione da parte della sessione da quando si è collegata.
                 Quindi il programma è stato impostato in questo modo:
                 - Vengono utilizzate 2 pagine di UT_REPORT (nel DB locale SQLITE) dove:
                   1a pagina - Alla prima esecuzione contiene la situazione di partenza (inizio monitoraggio)
                   2a pagina - Contiene la situazione al momento del campionamento successivo
                 - Dopo aver effettuato il campionamento nella pagina2, essa viene confrontata con la pagina1 e 
                   la pagina1 viene aggiornata con i nuovi valori (sessioni sparite, sessioni nuove, valori nuovi).
                   Sempre sulla pagina1 viene poi eseguito il calcolo della percentuale di valore
                 Attenzione! Non vengono estratte tutte le sessioni perché ci sono processi oracle che non interessano.
                  
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_top_sessions_ui.py è ricavato partendo da oracle_top_sessions_ui.ui 
"""

#Librerie sistema
import sys
import os
import datetime
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from oracle_top_sessions_ui import Ui_oracle_top_sessions_window
#Librerie interne MGrep
from utilita_database import t_report_class
from preferenze import preferenze
from utilita import message_error, message_info

class oracle_top_sessions_class(QtWidgets.QMainWindow, Ui_oracle_top_sessions_window):
    """
        Oracle session 
    """       
    def __init__(self):
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # apro t_report (tre pagine) tutte in memoria RAM
        self.fname = 'TOP_SESSIONS'
        self.t_report = t_report_class('MEMORY')
        self.page1 = self.t_report.new_page(self.fname)
        self.page2 = self.t_report.new_page(self.fname)
        
        # incapsulo la classe grafica da qtdesigner        
        super(oracle_top_sessions_class, self).__init__()        
        self.setupUi(self)       
        
        """
        # aggiungo un'area grafica accanto alla lista che servirà alla visualizzazione del grafico
        self.o_chart_view = QtChart.QChartView()
        self.o_chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gridLayout.addWidget(self.o_chart_view, 7, 0, 1, 4)        
        
        self.o_chart = QtChart.QChart()
        self.o_chart_view.setChart(self.o_chart)        
        self.o_chart.setTitle('TOP SESSIONS')        
        """
                
        # siccome il successivo carico delle poplist fa scattare l'evento di change con conseguente ricarico delle tabelle, 
        # la seguente variabile indica che siamo in fase di partenza del form
        self.v_load_form = True
        
        # carico la lista dei parametri di metrica disponibili 
        # (attenzione! le metriche vengono cercate per descrizione quindi attenzione a come si modificano)
        self.e_parameter.addItem('CPU used by this session')
        self.e_parameter.addItem('physical reads')
        self.e_parameter.addItem('db block gets')
        self.e_parameter.addItem('recursive calls')        
        self.e_parameter.addItem('consistent gets')        
        self.e_parameter.addItem('redo size')
        self.e_parameter.addItem('bytes sent via SQL*Net to client')
        self.e_parameter.addItem('bytes received via SQL*Net from client')
        self.e_parameter.addItem('SQL*Net roundtrips to/from client')
        self.e_parameter.addItem('sorts (memory)')
        self.e_parameter.addItem('sorts (disk)')
                
        # carico elenco dei server prendendolo dalle preferenze         
        for nome in self.o_preferenze.elenco_server:
            self.e_server_name.addItem(nome)
            
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
        # connessione al DB come amministratore
        try:
            self.oracle_con = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                                password=self.o_preferenze.v_oracle_password_sys,
                                                dsn=self.e_server_name.currentText(),
                                                mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return None
        
        # cambio la label del pulsante di calcoloo in modo sia riportata l'ora di riferimento
        self.b_calculate.setText("Compute difference from " + str(datetime.datetime.now().strftime('%H:%M:%S') ) )
        
        # cancello il contenuto delle pagine di ut_report (tranne record posizione 0)
        self.t_report.delete_page(self.fname, self.page1)
        
        # carico in pagina1 di ut_report, il punto di partenza della situazione sessioni         
        self.load_from_oracle_top_sessions(self.page1)
        
        # visualizzo il contenuto della pagina3
        self.load_screen(self.page1)
                                                                
    def load_from_oracle_top_sessions(self, p_page):
        """
            Carica nella pagina di ut_report indicata da p_page la query delle sessioni Oracle
        """
        # pulisco la pagina
        self.t_report.delete_page(self.fname, p_page)
        
        # apro cursore oracle
        v_cursor = self.oracle_con.cursor()
        
        # select per la ricerca degli oggetti invalidi        
        v_select = """select se.sid,
                             username,
                             status,
                             logon_time,
                             round ((sysdate-logon_time)*1440*60) logon_secs,                                                          
                             nvl(se.module, se.program) module_info,
                             se.sql_id,
                             (select min(sql_text) from V$SQL WHERE sql_id=se.sql_id) sql_text,
                             value
                      from   v$session se,
                             v$sesstat ss,
                             v$statname sn
                      where  username is not null
                        and  se.sid=ss.sid
                        and  sn.statistic#=ss.statistic#
                        and  sn.name in ('""" + self.e_parameter.currentText() + """')
                   """        
                
        v_cursor.execute(v_select)        
        
        # salvo in t_report 
        v_row = []
        for result in v_cursor:
            self.t_report.insert(p_commit=True,
                                 p_fname_co=self.fname, 
                                 p_page_nu=p_page, 
                                 p_campo25=result[0], 
                                 p_campo2=result[1],
                                 p_campo3=result[2], 
                                 p_campo4=result[3], 
                                 p_campo26=result[4],                                   
                                 p_campo6=result[5], 
                                 p_campo7=result[6], 
                                 p_campo8=result[7],
                                 p_campo21=result[8]) 
                  
        # chiudo cursore oracle
        v_cursor.close()
        
    def load_screen(self, p_page):            
        """
            Carica a video la pagina di ut_report indicata
        """
        # carico in una tupla i dati
        self.t_report.execute("""SELECT IFNULL(CAMPO24,''),
                                        IFNULL(CAMPO25,''),
                                        IFNULL(CAMPO2,''),
                                        IFNULL(CAMPO3,''),
                                        IFNULL(CAMPO4,''),
                                        IFNULL(CAMPO22,''),
                                        IFNULL(CAMPO21,''),
                                        IFNULL(CAMPO23,''), 
                                        IFNULL(CAMPO26,''),
                                        IFNULL(CAMPO6,''),
                                        IFNULL(CAMPO7,''),
                                        IFNULL(CAMPO8,'')
                                FROM   UT_REPORT
                                WHERE  FNAME_CO = ?
                                  AND  PAGE_NU = ?
                                  AND  POSIZ_NU > 0
                                ORDER BY CAMPO24 DESC, CAMPO3""", 
                            (self.fname, p_page))
        
        matrice_dati = self.t_report.curs.fetchall()
        
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
                # imposto il dato. E' stato usato il metodo setData perché in questo modo ho visto che i campi numerici 
                # si riescono poi ad ordinare correttamente.                 
                # Se il campo è numerico --> formatto e allineo a destra               
                if isinstance(field, float) or isinstance(field, int):                    
                    q_item.setData( '{:10.0f}'.format(field), QtCore.Qt.EditRole )                           
                    q_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                # altrimenti formatto automaticamente (EditRole) e allineo a sinistra
                else:
                    q_item.setData( field, QtCore.Qt.EditRole )                           
                    q_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)                    
                # carico l'item nella matrice-modello    
                self.lista_risultati.setItem(y, x, q_item )                
                x += 1
            y += 1
        # carico il modello nel widget        
        self.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        self.o_lst1.resizeColumnsToContents()   
        # imposto la label con il numero totale di sessioni
        self.l_total_sessions.setText('Number of sessions : ' + str(y))
    
    def calc_differenze(self):
        """
           Questo è di fatto il cuore del programma!
           Calcolo differenze tra pagina2 e pagina1 e il risultato lo metto nella pagina1
           
           Schema utilizzo dei campi di UT_REPORT 
           CAMPO25 = SID
           CAMPO2  = USERNAME
           CAMPO3  = STATUS
           CAMPO4  = LOGON_TIME (data e ora di logon della sessione)
           CAMPO26 = LOGON_SECS (tempo di connessione in secondi)           
           CAMPO6  = MODULE_INFO
           CAMPO7  = SQL_ID
           CAMPO8  = SQL_TEXT
           CAMPO21 = VALORE OLD DELLA METRICA (es. cpu)
           CAMPO22 = VALORE NOW DELLA METRICA (es. cpu)
           CAMPO23 = DIFFERENZA TRA VALORE OLD E VALORE NOW
           CAMPO24 = PERCENTUALE 
        """
        # carico la nuova situazione delle sessioni dentro la pagina2
        self.load_from_oracle_top_sessions(self.page2)
        
        #--
        # Attenzione! Essendoci un solo cursore aperto e dovendo fare una lettura di più tabelle incrociate, si caricano
        # i dati in matrici
        #-- 
        
        #--
        # STEP1 - elimino dalla pagina1 tutte quelle sessioni che NON sono presenti nella2. Vuol dire che nel frattempo 
        #         sono state chiuse
        #--
        self.t_report.execute("""SELECT * 
                                 FROM  UT_REPORT 
                                 WHERE FNAME_CO = ?
                                   AND PAGE_NU  = ? 
                                   AND POSIZ_NU > 0""", (self.fname, self.page1))
        # leggo tutta la pagina1
        tabella = self.t_report.curs.fetchall()
        for riga_pag1 in tabella:
            # decodifico la riga in modo sia un dizionario "parlante"
            v_rec_pag1 = self.t_report.decode(riga_pag1)
            # controllo se la sessione è ancora presente nella nuova situazione
            self.t_report.execute("""SELECT COUNT(*)
                                     FROM   UT_REPORT
                                     WHERE  FNAME_CO = ?
                                       AND  PAGE_NU  = ?
                                       AND  CAMPO25   = ?
                                       AND  CAMPO2   = ?""", (self.fname, self.page2, v_rec_pag1['CAMPO25'], v_rec_pag1['CAMPO2']) )
            v_count = self.t_report.curs.fetchone()[0]
            
            #print(v_rec_pag1['CAMPO25'] + ' utente ' + v_rec_pag1['CAMPO2'] + ' ' + str(v_count))
            # se la sessione non è presente --> la cancello dalla pagina1
            if v_count == 0:
                print('Sessione eliminata ' + str(v_rec_pag1['CAMPO25']) + ' utente ' + v_rec_pag1['CAMPO2'])
                self.t_report.execute("""DELETE 
                                         FROM   UT_REPORT
                                         WHERE  FNAME_CO = ?
                                           AND  PAGE_NU  = ?
                                           AND  CAMPO25   = ?
                                           AND  CAMPO2   = ?""", (self.fname, self.page1, v_rec_pag1['CAMPO25'], v_rec_pag1['CAMPO2']) )                
            
        #--
        # STEP2 - Partendo dalla pagina2, carico nella pagina1 tutte le nuove sessioni, 
        #--        
        self.t_report.execute("""SELECT * 
                                 FROM  UT_REPORT 
                                 WHERE FNAME_CO = ?
                                   AND PAGE_NU  = ? 
                                   AND POSIZ_NU> 0""", (self.fname, self.page2))
        tabella = self.t_report.curs.fetchall()    
        for riga_pag2 in tabella:
            # decodifico la riga in modo sia un dizionario "parlante"
            v_rec_pag2 = self.t_report.decode(riga_pag2)
            # ricerco se presente nella pagina1 (elaborazione precedente) la stessa sessione con lo stesso username 
            self.t_report.execute("""SELECT * 
                                     FROM   UT_REPORT 
                                     WHERE  FNAME_CO = ?
                                       AND  PAGE_NU= ? 
                                       AND  CAMPO25 = ? 
                                       AND  CAMPO2 = ?""", (self.fname, self.page1, v_rec_pag2['CAMPO25'], v_rec_pag2['CAMPO2']) )
            riga_pag1 = self.t_report.curs.fetchone()
            if riga_pag1 != None:
                # decodifico la riga in modo sia un dizionario "parlante"
                v_rec_pag1 = self.t_report.decode(riga_pag1)                
                # aggiorno la colonna22 della pagina1 che contiene il NUOVO valore. Inoltre aggiorno anche SQL_ID e SQL_Text 
                # in quanto potrebbero essere cambiati
                self.t_report.execute("""UPDATE UT_REPORT 
                                         SET    CAMPO22 = ?,
                                                CAMPO7 = ?,
                                                CAMPO8 = ?
                                         WHERE  FNAME_CO = ?
                                           AND  PAGE_NU = ? 
                                           AND  POSIZ_NU= ?""", 
                                        (v_rec_pag2['CAMPO21'], 
                                         v_rec_pag2['CAMPO7'], 
                                         v_rec_pag2['CAMPO8'], 
                                         v_rec_pag1['FNAME_CO'], 
                                         v_rec_pag1['PAGE_NU'], 
                                         v_rec_pag1['POSIZ_NU']) )
            else:
                # sessione non trovata, vuol dire che è stata aperta nel frattempo
                print('Nuova sessione ' + str(v_rec_pag2['CAMPO25']) + ' utente ' + v_rec_pag2['CAMPO2'])
                self.t_report.insert(p_commit  = True,
                                     p_fname_co= self.fname, 
                                     p_page_nu = self.page1, 
                                     p_campo25 = v_rec_pag2['CAMPO25'], 
                                     p_campo2  = v_rec_pag2['CAMPO2'],
                                     p_campo3  = v_rec_pag2['CAMPO3'], 
                                     p_campo4  = v_rec_pag2['CAMPO4'], 
                                     p_campo26 = v_rec_pag2['CAMPO26'],                                 
                                     p_campo6  = v_rec_pag2['CAMPO6'], 
                                     p_campo7  = v_rec_pag2['CAMPO7'], 
                                     p_campo8  = v_rec_pag2['CAMPO8'],
                                     p_campo21 = v_rec_pag2['CAMPO21']) 
        #--
        # STEP3 - In pagina1 calcolo la differenza tra il nuovo e il vecchio valore
        #--        
        self.t_report.execute("""UPDATE UT_REPORT 
                                 SET    CAMPO23 = ROUND(CAMPO22 - CAMPO21,0) 
                                 WHERE  FNAME_CO = ? 
                                   AND  PAGE_NU = ?""", (self.fname, self.page1) )  
        
        # calcolo il totale
        self.t_report.execute("""SELECT SUM(CAMPO23)
                                 FROM   UT_REPORT
                                 WHERE  FNAME_CO = ?
                                   AND  PAGE_NU  = ?""", (self.fname, self.page1) )
        v_totale = self.t_report.curs.fetchone()[0]
        
        # calcolo le percentuali rispetto al totale 
        self.t_report.execute("""UPDATE UT_REPORT 
                                 SET    CAMPO24 = ROUND(CAMPO23 * 100 / ?,1) 
                                 WHERE  FNAME_CO = ? 
                                   AND  PAGE_NU = ?""", (v_totale, self.fname, self.page1) )                            
            
    def slot_calculate(self):            
        """
            Lancio il calcolo          
        """        
        # calcolo la differenza tra la pagina2 e la pagina1 e il risultato lo metto nella pagina 3
        # la pagina1 viene constestualmente aggiornata togliendo le sessioni chiuse e inserendo quelle nuove
        self.calc_differenze()
        
        # visualizzo il risultato della pagina1
        self.load_screen(self.page1)
                        
    def slot_change_server(self):            
        """
           E' stato cambiato il server di riferimento e quindi va caricato tutto da capo
        """    
        if not self.v_load_form:            
            self.starter() 
            
    def slot_help(self):
        """
           Visualizza help specifico per le metriche
        """
        os.system("start help\\MGrep_top_sessions_help.html")
                        
    def closeEvent(self, event):
        """
           Questo metodo si sovrappone al metodo interno della chiusura della finestra
        """        
        # chiudo sessione Oracle
        self.oracle_con.close()
        # indico tramite variabile globale che l'applicazione viene chiusa 
        # (questo perché se richiamata dall'esterno può girare solo un'istanza per volta)        
        self.v_app_top_session_open = False
        # chiudo il DB sqlite senza commit
        self.t_report.close(False)
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