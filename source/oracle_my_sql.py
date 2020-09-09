# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6 con libreria pyqt5
 Data..........: 01/09/2020
 Descrizione...: Mini programma che simula in parte il funzionamento di sql tools
                  
 Note..........: Il layout è tutto creato manualmente in quanto è la composizione di un editor e poi c'è la gestione dello splitter tra 
                 editor di testo e gestione risultati che non si riusciva a gestire tramite qtdesigner
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
from PyQt5 import QtCore, QtGui, QtWidgets
import resource_rc
#from oracle_my_sql_ui import Ui_oracle_my_sql_window
#Librerie interne MGrep
from preferenze import preferenze
from utilita import message_error, message_info
from utilita_database import nomi_colonne_istruzione_sql

lineBarColor = QtGui.QColor("lightGray")
lineHighlightColor  = QtGui.QColor("red")

# classe per gestire i numeri di riga sull'editor
class NumberBar(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(NumberBar, self).__init__(parent)
        self.editor = parent
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.editor.blockCountChanged.connect(self.update_width)
        self.editor.updateRequest.connect(self.update_on_scroll)
        self.update_width('1')

    def update_on_scroll(self, rect, scroll):
        if self.isVisible():
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update()

    def update_width(self, string):
        width = self.fontMetrics().width(str(string)) + 10
        if self.width() != width:
            self.setFixedWidth(width)

    def paintEvent(self, event):
        if self.isVisible():
            block = self.editor.firstVisibleBlock()
            height = self.fontMetrics().height()
            number = block.blockNumber()
            painter = QtGui.QPainter(self)
            painter.fillRect(event.rect(), lineBarColor)
            painter.drawRect(0, 0, event.rect().width() - 1, event.rect().height() - 1)
            font = painter.font()

            current_block = self.editor.textCursor().block().blockNumber() + 1

            condition = True
            while block.isValid() and condition:
                block_geometry = self.editor.blockBoundingGeometry(block)
                offset = self.editor.contentOffset()
                block_top = block_geometry.translated(offset).top()
                number += 1

                rect = QtCore.QRect(0, block_top, self.width() - 5, height)

                if number == current_block:
                    font.setBold(True)
                else:
                    font.setBold(False)

                painter.setFont(font)
                painter.drawText(rect, QtCore.Qt.AlignRight, '%i'%number)

                if block_top > event.rect().bottom():
                    condition = False

                block = block.next()

            painter.end()

# classe principale       
class oracle_my_sql_class(object):
    """
        Oracle My Sql
    """       
    # Definizione interfaccia
    def setupUi(self, oracle_my_sql_window):        
        # Dimensioni della window e icona di riferimento
        oracle_my_sql_window.resize(748, 635)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_my_sql_window.setWindowIcon(icon)
        
        # Status bar (dove escono messaggi di errore sql)
        self.statusBar = QtWidgets.QStatusBar(oracle_my_sql_window)
        self.statusBar.setEnabled(True)
        self.statusBar.setSizeGripEnabled(True)        
        oracle_my_sql_window.setStatusBar(self.statusBar)
                
        # Editor sql (definizione dell'oggetto con tipo di font, ecc)
        self.e_sql = QtWidgets.QPlainTextEdit()
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_sql.setFont(font)
        
        # Editor --> definizione dell'oggetto che riporta i numeri di riga lateralmente
        self.e_sql_num_riga = NumberBar(self.e_sql)
        #layoutH = QtWidgets.QHBoxLayout()
        #layoutH.setSpacing(1.5)
        #layoutH.addWidget(self.e_sql_num_riga)
        #layoutH.addWidget(self.e_sql)
                
        # Oggetto dove escono i risultati dell'sql
        self.o_table = QtWidgets.QTableWidget()
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #sizePolicy.setHorizontalStretch(0)
        #sizePolicy.setVerticalStretch(20)
        #sizePolicy.setHeightForWidth(self.o_table.sizePolicy().hasHeightForWidth())
        #self.o_table.setSizePolicy(sizePolicy)
        self.o_table.setAlternatingRowColors(True)
        self.o_table.setGridStyle(QtCore.Qt.SolidLine)        
        self.o_table.setColumnCount(0)
        self.o_table.setRowCount(0)
        self.o_table.horizontalHeader().setSortIndicatorShown(True)
        self.o_table.setSortingEnabled(True)
        
        # Definizione della toolbar per caricamento e salvataggio
        self.toolBar = QtWidgets.QToolBar(oracle_my_sql_window)        
        oracle_my_sql_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)        
        self.actionLoad_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_sql.setIcon(icon1)
        self.actionLoad_sql.setText("Load sql")
        self.actionLoad_sql.setToolTip("Load a file sql")
        self.actionSave_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_sql.setIcon(icon2)
        self.actionSave_sql.setText("Save sql")
        self.actionSave_sql.setToolTip("Save sql into a file")
        self.actionExecute_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExecute_sql.setIcon(icon3)
        self.actionExecute_sql.setText("Execute sql")
        self.actionExecute_sql.setToolTip("Execute de sql statement")
        self.actionExecute_sql.setShortcut("F5")
        self.actionCommit = QtWidgets.QAction(oracle_my_sql_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/confirm.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCommit.setIcon(icon4)
        self.actionCommit.setText("Commit changes")
        self.actionCommit.setToolTip("Commit the changes on the sql results")        
        self.toolBar.addAction(self.actionLoad_sql)
        self.toolBar.addAction(self.actionSave_sql)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExecute_sql)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCommit)
        
        self.actionLoad_sql.triggered.connect(self.openFile)
        self.actionSave_sql.triggered.connect(self.fileSave)
        self.actionExecute_sql.triggered.connect(self.slot_execute)
        self.actionCommit.triggered.connect(self.slot_commit)
        QtCore.QMetaObject.connectSlotsByName(oracle_my_sql_window)
        
        # carico le preferenze
        self.o_preferenze = preferenze()    
        self.o_preferenze.carica()
        
        # aggiungo alla toolbar la label e la combobox della scelta del server
        # Label server
        self.l_server_name = QtWidgets.QLabel()                
        self.l_server_name.setText("Oracle name server:")
        
        # Combobox con elenco dei server
        self.e_server_name = QtWidgets.QComboBox()
                
        # Fissa i pulsanti nella toolbar
        self.toolBar.addSeparator()
        self.toolBar.addWidget(self.l_server_name)   
        self.toolBar.addWidget(self.e_server_name)   
                       
        # carico elenco dei server prendendolo dalle preferenze 
        # Attenzione! Verrà richiamato in automatico l'evento di connessione a oracle
        self.v_connesso = False
        for nome in self.o_preferenze.elenco_server:
            self.e_server_name.addItem(nome)
            
        # collego alla combobox l'azione         
        self.e_server_name.currentIndexChanged['int'].connect(self.slot_connect)
        # eseguo la connessione 
        self.slot_connect()        
        
        # Definizio della toolbar di trova e sostituisci
        self.tbf = QtWidgets.QToolBar(oracle_my_sql_window)
        oracle_my_sql_window.addToolBar(QtCore.Qt.TopToolBarArea, self.tbf)
        self.tbf.setWindowTitle("Find Toolbar")   
        self.findfield = QtWidgets.QLineEdit()
        self.findfield.addAction(QtGui.QIcon.fromTheme("edit-find"), QtWidgets.QLineEdit.LeadingPosition)
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(150)
        self.findfield.setPlaceholderText("find")
        self.findfield.setToolTip("press RETURN to find")
        self.findfield.setText("")
        ft = self.findfield.text()
        self.findfield.returnPressed.connect(self.findText)
        self.tbf.addWidget(self.findfield)
        self.replacefield = QtWidgets.QLineEdit()
        self.replacefield.addAction(QtGui.QIcon.fromTheme("edit-find-and-replace"), QtWidgets.QLineEdit.LeadingPosition)
        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(150)
        self.replacefield.setPlaceholderText("replace with")
        self.replacefield.setToolTip("press RETURN to replace the first")
        self.replacefield.returnPressed.connect(self.replaceOne)
        self.tbf.addSeparator() 
        self.tbf.addWidget(self.replacefield)
        self.tbf.addSeparator()        
                
        #----------------------------------------
        # Inizio Impaginazione di tutti gli oggetti
        # In pratica creo un primo layout dove inserisco l'oggetto che visualizza il numero di riga
        # e l'editor sql. Questo layout lo inserisco in un frame (questo perché lo splitter può essere solo
        # tra due widget e non tra due layout)
        # Creo un secondo layout dove inserisco il risultato sql, lo inserisco in un altro frame
        # Inserisco i due frame dentro uno splitter indicando che deve essere visualizzato in verticale
        # con una proporzione 1-2 
        layoutH = QtWidgets.QHBoxLayout()
        layoutH.setSpacing(1.5)
        layoutH.addWidget(self.e_sql_num_riga)
        layoutH.addWidget(self.e_sql)
        
        my_frame = QtWidgets.QFrame()
        my_frame.setLayout(layoutH)
        
        layoutV = QtWidgets.QVBoxLayout()
        layoutV.addWidget(self.o_table)
        
        my_frame1 = QtWidgets.QFrame()
        my_frame1.setLayout(layoutV)
        
        sizePolicy = QtWidgets.QSizePolicy()
        sizePolicy.setVerticalStretch(1)
        
        my_frame.setSizePolicy(sizePolicy)
        
        sizePolicy.setVerticalStretch(2)
        my_frame1.setSizePolicy(sizePolicy)
        
        splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(my_frame)
        splitter.addWidget(my_frame1)

        oracle_my_sql_window.setCentralWidget(splitter)                
        # Fine Impaginazione di tutti gli oggetti
        #----------------------------------------
                            
        # sql di prova        
        self.e_sql.setPlainText("SELECT * FROM TA_AZIEN")
        
        self.o_table.itemChanged.connect(self.log_change)
                        
        # Contiene il nome del file in elaborazione
        self.filename = ''
                
        """
        ###
        # IMPORT DELL'EDITOR
        ###
        # Editor Widget ...
        QIcon.setThemeName('Faenza-Dark')
        self.editor = QPlainTextEdit() 
        # imposto il font 
        font = QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.editor.setFont(font)        
        #self.editor.setStyleSheet(stylesheet2(self))
        self.editor.setFrameStyle(QFrame.NoFrame)
        self.editor.setTabStopWidth(14)
        self.extra_selections = []
        self.fname = ""
        self.filename = ""
        # Line Numbers ...
        self.numbers = NumberBar(self.editor)

        self.createActions()
        # Laying out...
        layoutH = QHBoxLayout()
        layoutH.setSpacing(1.5)
        layoutH.addWidget(self.numbers)
        layoutH.addWidget(self.editor)

        ### begin toolbar
        self.newAct = QAction("&New", self, shortcut=QKeySequence.New,
                              statusTip="Create a new file", triggered=self.newFile)
        self.newAct.setIcon(QIcon.fromTheme("document-new"))

        self.openAct = QAction("&Open", self, shortcut=QKeySequence.Open,
                               statusTip="open file", triggered=self.openFile)
        self.openAct.setIcon(QIcon.fromTheme("document-open"))

        self.saveAct = QAction("&Save", self, shortcut=QKeySequence.Save,
                               statusTip="save file", triggered=self.fileSave)
        self.saveAct.setIcon(QIcon.fromTheme("document-save"))

        self.saveAsAct = QAction("&Save as ...", self, shortcut=QKeySequence.SaveAs,
                                 statusTip="save file as ...", triggered=self.fileSaveAs)
        self.saveAsAct.setIcon(QIcon.fromTheme("document-save-as"))

        self.exitAct = QAction("Exit", self, shortcut=QKeySequence.Quit,
                               toolTip="Exit", triggered=self.handleQuit)
        self.exitAct.setIcon(QIcon.fromTheme("application-exit"))
        
        ### find / replace toolbar
        self.tbf = QToolBar(self)
        self.tbf.setWindowTitle("Find Toolbar")   
        self.findfield = QLineEdit()
        self.findfield.addAction(QIcon.fromTheme("edit-find"), QLineEdit.LeadingPosition)
        self.findfield.setClearButtonEnabled(True)
        self.findfield.setFixedWidth(150)
        self.findfield.setPlaceholderText("find")
        self.findfield.setToolTip("press RETURN to find")
        self.findfield.setText("")
        ft = self.findfield.text()
        self.findfield.returnPressed.connect(self.findText)
        self.tbf.addWidget(self.findfield)
        self.replacefield = QLineEdit()
        self.replacefield.addAction(QIcon.fromTheme("edit-find-and-replace"), QLineEdit.LeadingPosition)
        self.replacefield.setClearButtonEnabled(True)
        self.replacefield.setFixedWidth(150)
        self.replacefield.setPlaceholderText("replace with")
        self.replacefield.setToolTip("press RETURN to replace the first")
        self.replacefield.returnPressed.connect(self.replaceOne)
        self.tbf.addSeparator() 
        self.tbf.addWidget(self.replacefield)
        self.tbf.addSeparator()

        self.tbf.addAction("replace all", self.replaceAll)
        self.tbf.addSeparator()

        layoutV = QVBoxLayout()

        bar=self.menuBar()

        self.filemenu=bar.addMenu("File")
        self.separatorAct = self.filemenu.addSeparator()
        self.filemenu.addAction(self.newAct)
        self.filemenu.addAction(self.openAct)
        self.filemenu.addAction(self.saveAct)
        self.filemenu.addAction(self.saveAsAct)
        self.filemenu.addSeparator()
        for i in range(self.MaxRecentFiles):
            self.filemenu.addAction(self.recentFileActs[i])
        #self.updateRecentFileActions()
        self.filemenu.addSeparator()
        self.filemenu.addAction(self.exitAct)
        #bar.setStyleSheet(stylesheet2(self))
        editmenu = bar.addMenu("Edit")
        editmenu.addAction(QAction(QIcon.fromTheme('edit-copy'), "Copy", self, triggered = self.editor.copy, shortcut = QKeySequence.Copy))
        editmenu.addAction(QAction(QIcon.fromTheme('edit-cut'), "Cut", self, triggered = self.editor.cut, shortcut = QKeySequence.Cut))
        editmenu.addAction(QAction(QIcon.fromTheme('edit-paste'), "Paste", self, triggered = self.editor.paste, shortcut = QKeySequence.Paste))
        editmenu.addAction(QAction(QIcon.fromTheme('edit-delete'), "Delete", self, triggered = self.editor.cut, shortcut = QKeySequence.Delete))
        editmenu.addSeparator()
        editmenu.addAction(QAction(QIcon.fromTheme('edit-select-all'), "Select All", self, triggered = self.editor.selectAll, shortcut = QKeySequence.SelectAll))

        layoutV.addWidget(bar)      
        layoutV.addWidget(self.tbf)
        layoutV.addLayout(layoutH)

        ### main window
        mq = QWidget(self)
        mq.setLayout(layoutV)
        self.setCentralWidget(mq)

        # Event Filter ...
        self.installEventFilter(self)
        self.editor.setFocus()
        self.cursor = QTextCursor()
        self.editor.setPlainText("hello")
        self.editor.moveCursor(self.cursor.End)
        self.editor.document().modificationChanged.connect(self.setWindowModified)

        # Brackets ExtraSelection ...
        self.left_selected_bracket  = QTextEdit.ExtraSelection()
        self.right_selected_bracket = QTextEdit.ExtraSelection()
        """
        
    def log_change(self, item):
        print(item)
                                        
    def slot_connect(self):
        """
           Esegue connessione a Oracle
        """
        try:
            # chiudo eventuale connessione già aperta 
            if self.v_connesso:
                self.v_cursor.close()
            # connessione al DB come smile
            self.v_connection = cx_Oracle.connect(user='SMILE', password='SMILE', dsn=self.e_server_name.currentText())            
            # apro cursore
            self.v_cursor = self.v_connection.cursor()                
            # imposto var che indica la connesione a oracle
            self.v_connesso = True
        except:
            message_error('Error to oracle connection!')                                             
                
    def slot_execute(self):
        """
           Esegue statement sql
        """
        if self.v_connesso:
            self.o_table.clear()
            # sostituisce la freccia del mouse con icona "clessidra"
            QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))        
            
            # esecuzione dell'sql contenuto nel campo a video            
            v_ok = True
            try:
                self.v_cursor.execute( self.e_sql.toPlainText() )                            
            # se riscontrato errore --> emetto sia codice che messaggio
            except cx_Oracle.Error as e:                
                v_ok = False
                errorObj, = e.args                
                #self.statusBar.showMessage("Error Code: " + str(errorObj.code) + "Error Message: " + errorObj.message)                 
                self.statusBar.showMessage("Error: " + errorObj.message)                 
            
            if v_ok:
                # lista contenente le intestazioni (tramite apposita funzione si ricavano i nomi delle colonne dall'sql che si intende eseguire)
                intestazioni = nomi_colonne_istruzione_sql(self.v_cursor)                        
                # carico i dati in una matrice e identifico il numero di righe e di colonne della tabella
                matrice_dati = self.v_cursor.fetchall()
                self.o_table.setColumnCount(len(intestazioni))            
                self.o_table.setRowCount(len(matrice_dati))                        
                # setto le intestazioni....va fatta dopo che sono state indicate le righe e colonne altrimenti non funziona
                self.o_table.setHorizontalHeaderLabels(intestazioni)
                y =0
                # carico i dati presi dal db dentro il modello
                for row in matrice_dati:            
                    x = 0                            
                    for field in row:                                        
                        # campo numerico (se non funziona provare con i cx_Oracle type
                        if isinstance(field, float) or isinstance(field, int):                           
                            self.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( '{:10.0f}'.format(field) ) )
                        # campo nullo
                        elif field == None:                                                
                            self.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( "" ) )                
                        # se il contenuto è un clob...utilizzo il metodo read sul campo field, poi lo inserisco in una immagine
                        # che poi carico una label e finisce dentro la cella a video
                        elif self.v_cursor.description[x][1] == cx_Oracle.BLOB:                                                                            
                            qimg = QtGui.QImage.fromData(field.read())
                            pixmap = QtGui.QPixmap.fromImage(qimg)   
                            label = QtWidgets.QLabel()
                            label.setPixmap(pixmap)                        
                            self.o_table.setCellWidget(y, x, label )                
                        # campo data
                        elif self.v_cursor.description[x][1] == cx_Oracle.DATETIME:                                                                            
                            self.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( str(field) ) )       
                        # campo stringa
                        else:                                                 
                            self.o_table.setItem(y, x, QtWidgets.QTableWidgetItem( field ) )                
                        x += 1
                    y += 1
                # indico di calcolare automaticamente la larghezza delle colonne
                self.o_table.resizeColumnsToContents()
                
            # Ripristino icona freccia del mouse
            QtWidgets.QApplication.restoreOverrideCursor()                        
        
    def slot_commit(self):
        """
           Salva eventuali modifiche di tabella
        """
        
    ###
    # CODICE GESTIONE EDITOR
    ###
    #def createActions(self):
        #for i in range(self.MaxRecentFiles):
            #self.recentFileActs.append(
                #QAction(self, visible=False,
                           #triggered=self.openRecentFile))


    #def openRecentFile(self):
        #action = self.sender()
        #if action:
            #if (self.maybeSave()):
                #self.openFileOnStart(action.data())

        #### New File
    #def newFile(self):
        #if self.maybeSave():
            #self.editor.clear()
            #self.editor.setPlainText("")
            #self.filename = ""
            #self.setModified(False)
            #self.editor.moveCursor(self.cursor.End)

        ### open File
    #def openFileOnStart(self, path=None):
        #if path:
            #inFile = QFile(path)
            #if inFile.open(QFile.ReadWrite | QFile.Text):
                #text = inFile.readAll()

                #try:
                        ## Python v3.
                    #text = str(text, encoding = 'utf8')
                #except TypeError:
                        ## Python v2.
                    #text = str(text)
                #self.editor.setPlainText(text)
                #self.filename = path
                #self.setModified(False)
                #self.fname = QFileInfo(path).fileName() 
                #self.setWindowTitle(self.fname + "[*]")
                #self.document = self.editor.document()
                #self.setCurrentFile(self.filename)

        ### open File
    def openFile(self):
        if self.maybeSave():            
            fileName = QtWidgets.QFileDialog.getOpenFileName(oracle_my_sql_window, "Open File", QtCore.QDir.homePath() + "/Documents/","SQL Files (*.sql);;All Files (*.*)")                
            if fileName[0] != "":
                try:             
                    v_file = open(fileName[0],'r')
                    self.e_sql.clear()                        
                    self.e_sql.setPlainText( v_file.read() )
                    self.filename = fileName
                    self.setModified(False)
                    self.fname = QtCore.QFileInfo(fileName[0]).fileName() 
                    oracle_my_sql_window.setWindowTitle(self.fname + "[*]")
                    self.document = self.e_sql.document()                        
                except:
                    message_error('Error to opened the file')

    def fileSave(self):
        if (self.filename != ""):
            file = QtCore.QFile(self.filename)            
            if not file.open( QtCore.QFile.WriteOnly | QtCore.QFile.Text):
                message_error("Cannot write file %s:\n%s." % (self.filename, file.errorString()))
                return

            outstr = QtCore.QTextStream(file)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            outstr << self.e_sql.toPlainText()
            QtWidgets.QApplication.restoreOverrideCursor()                
            self.setModified(False)
            self.fname = QtCore.QFileInfo(self.filename).fileName() 
            oracle_my_sql_window.setWindowTitle(self.fname + "[*]")            

        else:
            self.fileSaveAs()

            ### save File
    def fileSaveAs(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(oracle_my_sql_window, "Save as...", self.filename,"SQL files (*.sql)")

        if not fn:
            message_error('Error saving')
            return False

        lfn = fn.lower()
        if not lfn.endswith('.sql'):
            fn += '.sql'

        self.filename = fn
        self.fname = os.path.splitext(str(fn))[0].split("/")[-1]
        return self.fileSave()

    def closeEvent(self, e):
        if self.maybeSave():
            e.accept()
        else:
            e.ignore()

    ### ask to save
    def maybeSave(self):
        if not self.isModified():
            return True

        if self.filename.startswith(':/'):
            return True

        ret = QMessageBox.question(self, "Message",
                                   "<h4><p>The document was modified.</p>\n" \
                "<p>Do you want to save changes?</p></h4>",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

        if ret == QMessageBox.Yes:
            if self.filename == "":
                self.fileSaveAs()
                return False
            else:
                self.fileSave()
                return True

        if ret == QMessageBox.Cancel:
            return False

        return True   

    def findText(self):
        ft = self.findfield.text()
        if self.e_sql.find(ft):
            return
        else:
            self.e_sql.moveCursor(1)
            if self.e_sql.find(ft):
                self.e_sql.moveCursor(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)

    #def handleQuit(self):
        #print("Goodbye ...")
        #app.quit()

    #def set_numbers_visible(self, value = True):
        #self.numbers.setVisible(False)

    def match_left(self, block, character, start, found):
        map = {'{': '}', '(': ')', '[': ']'}

        while block.isValid():
            data = block.userData()
            if data is not None:
                braces = data.braces
                N = len(braces)

                for k in range(start, N):
                    if braces[k].character == character:
                        found += 1

                    if braces[k].character == map[character]:
                        if not found:
                            return braces[k].position + block.position()
                        else:
                            found -= 1

                block = block.next()
                start = 0

    def match_right(self, block, character, start, found):
        map = {'}': '{', ')': '(', ']': '['}

        while block.isValid():
            data = block.userData()

            if data is not None:
                braces = data.braces

                if start is None:
                    start = len(braces)
                for k in range(start - 1, -1, -1):
                    if braces[k].character == character:
                        found += 1
                    if braces[k].character == map[character]:
                        if found == 0:
                            return braces[k].position + block.position()
                        else:
                            found -= 1
            block = block.previous()
            start = None
#    '''

        cursor = self.editor.textCursor()
        block = cursor.block()
        data = block.userData()
        previous, next = None, None

        if data is not None:
            position = cursor.position()
            block_position = cursor.block().position()
            braces = data.braces
            N = len(braces)

            for k in range(0, N):
                if braces[k].position == position - block_position or braces[k].position == position - block_position - 1:
                    previous = braces[k].position + block_position
                    if braces[k].character in ['{', '(', '[']:
                        next = self.match_left(block,
                                               braces[k].character,
                                               k + 1, 0)
                    elif braces[k].character in ['}', ')', ']']:
                        next = self.match_right(block,
                                                braces[k].character,
                                                k, 0)
                    if next is None:
                        next = -1

        if next is not None and next > 0:
            if next == 0 and next >= 0:
                format = QTextCharFormat()

            cursor.setPosition(previous)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setBackground(QColor('white'))
            self.left_selected_bracket.format = format
            self.left_selected_bracket.cursor = cursor

            cursor.setPosition(next)
            cursor.movePosition(QTextCursor.NextCharacter,
                                QTextCursor.KeepAnchor)

            format.setBackground(QColor('white'))
            self.right_selected_bracket.format = format
            self.right_selected_bracket.cursor = cursor
#            '''
    def paintEvent(self, event):
        highlighted_line = QTextEdit.ExtraSelection()
        highlighted_line.format.setBackground(lineHighlightColor)
        highlighted_line.format.setProperty(QTextFormat
                                            .FullWidthSelection,
                                                 QVariant(True))
        highlighted_line.cursor = self.editor.textCursor()
        highlighted_line.cursor.clearSelection()
        self.editor.setExtraSelections([highlighted_line,
                                        self.left_selected_bracket,
                                      self.right_selected_bracket])

    def document(self):
        return self.editor.document

    def isModified(self):
        return self.e_sql.document().isModified()

    def setModified(self, modified):
        self.e_sql.document().setModified(modified)

    def setLineWrapMode(self, mode):
        self.e_sql.setLineWrapMode(mode)

    def clear(self):
        self.e_sql.clear()

    def setPlainText(self, *args, **kwargs):
        self.editor.setPlainText(*args, **kwargs)

    #def setDocumentTitle(self, *args, **kwargs):
    #    self.editor.setDocumentTitle(*args, **kwargs)

    #def set_number_bar_visible(self, value):
    #    self.numbers.setVisible(value)

    def replaceAll(self):
        print("replacing all")
        oldtext = self.editor.document().toPlainText()
        newtext = oldtext.replace(self.findfield.text(), self.replacefield.text())
        self.editor.setPlainText(newtext)
        self.setModified(True)

    def replaceOne(self):
        print("replacing all")
        oldtext = self.editor.document().toPlainText()
        newtext = oldtext.replace(self.findfield.text(), self.replacefield.text(), 1)
        self.editor.setPlainText(newtext)
        self.setModified(True)    

# ----------------------------------------
# TEST APPLICAZIONE
# ----------------------------------------
if __name__ == "__main__":    
    app = QtWidgets.QApplication([])    
    oracle_my_sql_window = QtWidgets.QMainWindow()
    oracle_my_sql_window.setWindowTitle("Oracle My Sql")
    application = oracle_my_sql_class()
    application.setupUi(oracle_my_sql_window)
    oracle_my_sql_window.showMaximized()
    sys.exit(app.exec())   