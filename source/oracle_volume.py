# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 19/12/2019
 Descrizione...: Programma che visualizza volume occupato dalle tabelle di oracle
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file oracle_volume_ui.py è ricavato partendo da oracle_volume_ui.ui 
"""

#Librerie sistema
import sys
import os
#Amplifico la pathname dell'applicazione in modo veda il contenuto della directory qtdesigner dove sono contenuti i layout
sys.path.append('qtdesigner')
#Librerie di data base
import cx_Oracle
#Librerie grafiche
from PyQt5 import QtCore, QtGui, QtWidgets, QtChart
from oracle_volume_ui import Ui_oracle_volume_window
# Libreria per la corretta formattazione dei numeri
import locale
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
       
class oracle_volume_class(QtWidgets.QMainWindow, Ui_oracle_volume_window):
    """
        Visualizza volume occupato dal DB oracle
    """       
    def __init__(self):
        # incapsulo la classe grafica da qtdesigner
        super(oracle_volume_class, self).__init__()        
        self.setupUi(self)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # carico elenco dei server prendendolo dalle preferenze
        for nome in self.o_preferenze.elenco_server:
            self.e_server_name.addItem(nome)
            
        # aggiungo un'area grafica accanto alla lista che servirà alla visualizzazione del grafico
        self.o_chart_view = QtChart.QChartView()
        self.o_chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.gridLayout.addWidget(self.o_chart_view, 10, 4, 2, 3)        
        
        self.o_chart = QtChart.QChart()
        self.o_chart_view.setChart(self.o_chart)        
        self.o_chart.setTitle('PIECHART TABLE SIZE')        
        
        # carico nel grafico dei dati di base
        self.o_chart.addSeries(self.get_serie_di_base())

    def get_serie_di_base(self):
        """
           Imposta la serie di base 100%
        """
        series = QtChart.QPieSeries()
        slice0 = series.append('100%', 1)        
        slice0.setColor(QtGui.QColor(0, 160, 0, 100))        
        
        return series
    
    def get_lista_volumi(self):
        """
            Restituisce in una tupla elenco delle tabelle con relativa occupazione
        """
        try:
            # connessione al DB come amministratore
            v_connection = cx_Oracle.connect(user=self.o_preferenze.v_oracle_user_sys,
                                             password=self.o_preferenze.v_oracle_password_sys,
                                             dsn=self.e_server_name.currentText(),
                                             mode=cx_Oracle.SYSDBA)            
        except:
            message_error('Connection to oracle rejected. Please control login information.')
            return []

        # apro cursori
        v_cursor = v_connection.cursor()

        v_table = ""
        # ricerca parziale su nome utente
        if self.e_table_name.displayText() != '':
            v_table += " AND Upper(table_name) LIKE '%" + self.e_table_name.displayText().upper() + "%' "            
                        
        # select per la ricerca degli oggetti invalidi
        v_select = '''SELECT table_name, 
                             sum(bytes)/1024/1024 MB
                      FROM   (SELECT segment_name table_name, owner, bytes
                              FROM   dba_segments
                              WHERE  segment_type = 'TABLE'
                              
                              UNION  ALL
                              
                              SELECT i.table_name, i.owner, s.bytes
                              FROM   dba_indexes i, 
                                     dba_segments s
                              WHERE  s.segment_name = i.index_name
                                AND  s.owner = i.owner
                                AND  s.segment_type = 'INDEX'
                              
                              UNION ALL
                           
                              SELECT l.table_name, l.owner, s.bytes
                              FROM   dba_lobs l, 
                                     dba_segments s
                              WHERE  s.segment_name = l.segment_name
                                AND  s.owner = l.owner
                                AND  s.segment_type = 'LOBSEGMENT'
                              
                              UNION ALL
                      
                              SELECT l.table_name, l.owner, s.bytes
                              FROM   dba_lobs l, 
                                     dba_segments s
                              WHERE  s.segment_name = l.index_name
                                AND  s.owner = l.owner
                                AND  s.segment_type = 'LOBINDEX')
                              
                      WHERE owner = UPPER('SMILE')
                        AND table_name NOT LIKE '%$%'
                   ''' + v_table + '''     
                      GROUP BY table_name, owner
                      ORDER BY SUM(bytes) desc 
                   '''
        
        v_cursor.execute(v_select)        
        
        # integro i risultati della prima select con altri dati e li carico in una tupla
        v_row = []
        for result in v_cursor:
            # carico la riga nella tupla (notare le doppie parentesi iniziali che servono per inserire nella tupla una lista :-))
            v_row.append( ( result[0], result[1] ) )            
                  
        # chiudo sessione
        v_cursor.close()
        v_connection.close()
        
        # restituisco tupla delle righe
        return v_row
        
    def slot_start_search(self):            
        """
            Calcola il volume
        """        
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
        matrice_dati = self.get_lista_volumi()   
        QtWidgets.QApplication.restoreOverrideCursor()        
        # se la matrice è vuota esco
        if len(matrice_dati) == 0:
            return None
        # lista contenente le intestazioni
        intestazioni = ['Table name','Megabyte']                        
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
                self.lista_risultati.setItem(y, x, QtGui.QStandardItem(str(field)) )
                x += 1
            y += 1
        # carico il modello nel widget        
        self.o_lst1.setModel(self.lista_risultati)                                   
        # indico di calcolare automaticamente la larghezza delle colonne
        #self.o_lst1.resizeColumnsToContents()
        
        # calcolo totali e li visualizzo nelle varie unità di misura
        v_total_size = 0
        for row in matrice_dati:
            v_total_size += row[1]
        self.l_tot_megabyte.setText( locale.format_string('%.2f', v_total_size, grouping=True) )
        self.l_tot_gigabyte.setText( locale.format_string('%.2f', v_total_size/1000, grouping=True) )
        self.l_tot_terabyte.setText( locale.format_string('%.2f', v_total_size/1000/1000, grouping=True) )                                       
        
        # creo lista di 3 elementi dove i primi due sono le due tabelle più grandi e la terza è lo spazio di tutto il resto        
        if len(matrice_dati) > 2:                        
            v_name_tabel_1 = matrice_dati[0][0]
            v_size_tabel_1 = matrice_dati[0][1]
            v_name_tabel_2 = matrice_dati[1][0]
            v_size_tabel_2 = matrice_dati[1][1]           
            v_name_tabel_3 = 'Other'
            v_size_tabel_3 = v_total_size - matrice_dati[0][1] - matrice_dati[1][1]           
            
        # carico il grafico a torta con le tre fette calcolate sopra        
        self.o_chart.removeAllSeries()
        series = QtChart.QPieSeries()        
        series.append(v_name_tabel_1, v_size_tabel_1)
        series.append(v_name_tabel_2, v_size_tabel_2)        
        series.append(v_name_tabel_3, v_size_tabel_3)        
        series.setLabelsVisible()        
        self.o_chart.addSeries(series)                                                                                           
            
# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    application = oracle_volume_class() 
    application.show()
    sys.exit(app.exec())        