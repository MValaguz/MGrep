# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ricerca_stringhe_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.b_search = QtWidgets.QPushButton(self.centralwidget)
        self.b_search.setToolTip("")
        self.b_search.setStatusTip("")
        self.b_search.setWhatsThis("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search.setIcon(icon1)
        self.b_search.setObjectName("b_search")
        self.gridLayout.addWidget(self.b_search, 7, 5, 1, 1)
        self.b_pathname = QtWidgets.QPushButton(self.centralwidget)
        self.b_pathname.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_pathname.setIcon(icon2)
        self.b_pathname.setObjectName("b_pathname")
        self.gridLayout.addWidget(self.b_pathname, 1, 6, 1, 1)
        self.c_dbsearch = QtWidgets.QCheckBox(self.centralwidget)
        self.c_dbsearch.setObjectName("c_dbsearch")
        self.gridLayout.addWidget(self.c_dbsearch, 4, 1, 1, 1)
        self.b_excludepath = QtWidgets.QPushButton(self.centralwidget)
        self.b_excludepath.setText("")
        self.b_excludepath.setIcon(icon2)
        self.b_excludepath.setObjectName("b_excludepath")
        self.gridLayout.addWidget(self.b_excludepath, 3, 6, 1, 1)
        self.l_filter = QtWidgets.QLabel(self.centralwidget)
        self.l_filter.setObjectName("l_filter")
        self.gridLayout.addWidget(self.l_filter, 2, 2, 1, 1)
        self.b_add_line = QtWidgets.QPushButton(self.centralwidget)
        self.b_add_line.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/add.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_add_line.setIcon(icon3)
        self.b_add_line.setObjectName("b_add_line")
        self.gridLayout.addWidget(self.b_add_line, 7, 4, 1, 1)
        self.l_dboracle1 = QtWidgets.QLabel(self.centralwidget)
        self.l_dboracle1.setObjectName("l_dboracle1")
        self.gridLayout.addWidget(self.l_dboracle1, 4, 2, 1, 1)
        self.l_excludepath = QtWidgets.QLabel(self.centralwidget)
        self.l_excludepath.setObjectName("l_excludepath")
        self.gridLayout.addWidget(self.l_excludepath, 3, 2, 1, 1)
        self.l_dboracle2 = QtWidgets.QLabel(self.centralwidget)
        self.l_dboracle2.setObjectName("l_dboracle2")
        self.gridLayout.addWidget(self.l_dboracle2, 5, 2, 1, 1)
        self.e_stringa1 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_stringa1.setObjectName("e_stringa1")
        self.gridLayout.addWidget(self.e_stringa1, 0, 1, 1, 1)
        self.l_stringa1 = QtWidgets.QLabel(self.centralwidget)
        self.l_stringa1.setObjectName("l_stringa1")
        self.gridLayout.addWidget(self.l_stringa1, 0, 0, 1, 1)
        self.l_stringa2 = QtWidgets.QLabel(self.centralwidget)
        self.l_stringa2.setObjectName("l_stringa2")
        self.gridLayout.addWidget(self.l_stringa2, 0, 2, 1, 1)
        self.c_flsearch = QtWidgets.QCheckBox(self.centralwidget)
        self.c_flsearch.setObjectName("c_flsearch")
        self.gridLayout.addWidget(self.c_flsearch, 1, 1, 1, 1)
        self.l_dbapex = QtWidgets.QLabel(self.centralwidget)
        self.l_dbapex.setObjectName("l_dbapex")
        self.gridLayout.addWidget(self.l_dbapex, 6, 2, 1, 1)
        self.l_pathname = QtWidgets.QLabel(self.centralwidget)
        self.l_pathname.setObjectName("l_pathname")
        self.gridLayout.addWidget(self.l_pathname, 1, 2, 1, 1)
        self.c_apexsearch = QtWidgets.QCheckBox(self.centralwidget)
        self.c_apexsearch.setObjectName("c_apexsearch")
        self.gridLayout.addWidget(self.c_apexsearch, 6, 1, 1, 1)
        self.e_outputfile = QtWidgets.QLineEdit(self.centralwidget)
        self.e_outputfile.setObjectName("e_outputfile")
        self.gridLayout.addWidget(self.e_outputfile, 7, 1, 1, 1)
        self.o_lst1 = QtWidgets.QListView(self.centralwidget)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 8, 0, 1, 7)
        self.l_outputfile = QtWidgets.QLabel(self.centralwidget)
        self.l_outputfile.setObjectName("l_outputfile")
        self.gridLayout.addWidget(self.l_outputfile, 7, 0, 1, 1)
        self.b_save_pref = QtWidgets.QPushButton(self.centralwidget)
        self.b_save_pref.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_pref.setIcon(icon4)
        self.b_save_pref.setObjectName("b_save_pref")
        self.gridLayout.addWidget(self.b_save_pref, 7, 3, 1, 1)
        self.e_dbapex = QtWidgets.QLineEdit(self.centralwidget)
        self.e_dbapex.setObjectName("e_dbapex")
        self.gridLayout.addWidget(self.e_dbapex, 6, 3, 1, 3)
        self.e_dboracle2 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_dboracle2.setObjectName("e_dboracle2")
        self.gridLayout.addWidget(self.e_dboracle2, 5, 3, 1, 3)
        self.e_dboracle1 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_dboracle1.setObjectName("e_dboracle1")
        self.gridLayout.addWidget(self.e_dboracle1, 4, 3, 1, 3)
        self.e_excludepath = QtWidgets.QLineEdit(self.centralwidget)
        self.e_excludepath.setObjectName("e_excludepath")
        self.gridLayout.addWidget(self.e_excludepath, 3, 3, 1, 3)
        self.e_filter = QtWidgets.QLineEdit(self.centralwidget)
        self.e_filter.setObjectName("e_filter")
        self.gridLayout.addWidget(self.e_filter, 2, 3, 1, 3)
        self.e_pathname = QtWidgets.QLineEdit(self.centralwidget)
        self.e_pathname.setObjectName("e_pathname")
        self.gridLayout.addWidget(self.e_pathname, 1, 3, 1, 3)
        self.e_stringa2 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_stringa2.setObjectName("e_stringa2")
        self.gridLayout.addWidget(self.e_stringa2, 0, 3, 1, 3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.l_filter.setBuddy(self.e_filter)
        self.l_dboracle1.setBuddy(self.e_dboracle1)
        self.l_excludepath.setBuddy(self.e_excludepath)
        self.l_dboracle2.setBuddy(self.e_dboracle2)
        self.l_stringa1.setBuddy(self.e_stringa1)
        self.l_stringa2.setBuddy(self.e_stringa2)
        self.l_dbapex.setBuddy(self.e_dbapex)
        self.l_pathname.setBuddy(self.e_pathname)
        self.l_outputfile.setBuddy(self.e_outputfile)

        self.retranslateUi(MainWindow)
        self.b_pathname.clicked.connect(self.b_pathname_slot)
        self.b_excludepath.clicked.connect(self.b_excludepath_slot)
        self.b_save_pref.clicked.connect(self.b_save_slot)
        self.b_search.clicked.connect(self.b_search_slot)
        self.b_add_line.clicked.connect(self.b_add_line_slot)
        self.o_lst1.doubleClicked['QModelIndex'].connect(self.o_lst1_slot)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.e_stringa1, self.e_stringa2)
        MainWindow.setTabOrder(self.e_stringa2, self.c_flsearch)
        MainWindow.setTabOrder(self.c_flsearch, self.e_pathname)
        MainWindow.setTabOrder(self.e_pathname, self.b_pathname)
        MainWindow.setTabOrder(self.b_pathname, self.e_filter)
        MainWindow.setTabOrder(self.e_filter, self.e_excludepath)
        MainWindow.setTabOrder(self.e_excludepath, self.b_excludepath)
        MainWindow.setTabOrder(self.b_excludepath, self.c_dbsearch)
        MainWindow.setTabOrder(self.c_dbsearch, self.e_dboracle1)
        MainWindow.setTabOrder(self.e_dboracle1, self.e_dboracle2)
        MainWindow.setTabOrder(self.e_dboracle2, self.c_apexsearch)
        MainWindow.setTabOrder(self.c_apexsearch, self.e_dbapex)
        MainWindow.setTabOrder(self.e_dbapex, self.e_outputfile)
        MainWindow.setTabOrder(self.e_outputfile, self.b_save_pref)
        MainWindow.setTabOrder(self.b_save_pref, self.b_add_line)
        MainWindow.setTabOrder(self.b_add_line, self.b_search)
        MainWindow.setTabOrder(self.b_search, self.o_lst1)
        
        self.progressBar()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Search string in sources of Oracle Forms/Reports and Oracle Apex"))
        self.b_search.setText(_translate("MainWindow", "Start search"))
        self.c_dbsearch.setText(_translate("MainWindow", "Execute search in OracleDB"))
        self.l_filter.setText(_translate("MainWindow", "File filter"))
        self.b_add_line.setToolTip(_translate("MainWindow", "<html><head/><body><p>Add the selected line to \'My favorites files</p></body></html>"))
        self.l_dboracle1.setText(_translate("MainWindow", "Oracle connection1"))
        self.l_excludepath.setText(_translate("MainWindow", "Exclude directories"))
        self.l_dboracle2.setText(_translate("MainWindow", "Oracle connection2"))
        self.l_stringa1.setText(_translate("MainWindow", "Search string1"))
        self.l_stringa2.setText(_translate("MainWindow", "and Search string2"))
        self.c_flsearch.setText(_translate("MainWindow", "Execute search in folder"))
        self.l_dbapex.setText(_translate("MainWindow", "Apex oracle connection"))
        self.l_pathname.setText(_translate("MainWindow", "Folder name"))
        self.c_apexsearch.setText(_translate("MainWindow", "Execute search in Apex"))
        self.l_outputfile.setText(_translate("MainWindow", "Output file csv"))
        self.b_save_pref.setToolTip(_translate("MainWindow", "<html><head/><body><p>Save the search data in order to be retrieved at the next start of SmiGrep</p></body></html>"))

    def b_pathname_slot(self):
        pass
    
    def b_excludepath_slot(self):
        pass
    
    def b_save_slot(self):
        pass
    
    def b_search_slot(self):
        pass
    
    def b_add_line_slot(self):
        pass
    
    def o_lst1_slot(self):
        pass
    
    def progressBar(self):
        MainWindow = QtWidgets.QWidget()
        progress = QtWidgets.QProgressDialog("Please Wait!", "Cancel", 0, 0, MainWindow)        
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setAutoReset(True)
        progress.setAutoClose(True)
        #progress.setMinimum(0)
        #progress.setMaximum(0)
        progress.resize(400,100)
        progress.setWindowTitle("Loading....")
        progress.show()
        #progress.setValue(100)
        
        progress.setRange(0,0)
        
        for i in range(100):
            print(i)
            progress.setValue(i)
            time.sleep(1)            
            if progress.wasCanceled():
                break
            
        progress.hide()        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

