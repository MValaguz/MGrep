# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ricerca_stringhe_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ricerca_stringhe_window(object):
    def setupUi(self, Ricerca_stringhe_window):
        Ricerca_stringhe_window.setObjectName("Ricerca_stringhe_window")
        Ricerca_stringhe_window.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ricerca_stringhe_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Ricerca_stringhe_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.e_dboracle1 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_dboracle1.setObjectName("e_dboracle1")
        self.gridLayout.addWidget(self.e_dboracle1, 5, 7, 1, 3)
        self.e_dboracle2 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_dboracle2.setObjectName("e_dboracle2")
        self.gridLayout.addWidget(self.e_dboracle2, 6, 7, 1, 3)
        self.e_pathname = QtWidgets.QLineEdit(self.centralwidget)
        self.e_pathname.setObjectName("e_pathname")
        self.gridLayout.addWidget(self.e_pathname, 1, 7, 1, 2)
        self.e_filter = QtWidgets.QLineEdit(self.centralwidget)
        self.e_filter.setObjectName("e_filter")
        self.gridLayout.addWidget(self.e_filter, 2, 7, 2, 3)
        self.l_excludepath = QtWidgets.QLabel(self.centralwidget)
        self.l_excludepath.setObjectName("l_excludepath")
        self.gridLayout.addWidget(self.l_excludepath, 4, 4, 1, 3)
        self.o_lst1 = QtWidgets.QListView(self.centralwidget)
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 12, 0, 1, 11)
        self.b_pathname = QtWidgets.QPushButton(self.centralwidget)
        self.b_pathname.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_pathname.setIcon(icon1)
        self.b_pathname.setObjectName("b_pathname")
        self.gridLayout.addWidget(self.b_pathname, 1, 9, 1, 1)
        self.l_dboracle1 = QtWidgets.QLabel(self.centralwidget)
        self.l_dboracle1.setObjectName("l_dboracle1")
        self.gridLayout.addWidget(self.l_dboracle1, 5, 4, 1, 2)
        self.c_flsearch = QtWidgets.QCheckBox(self.centralwidget)
        self.c_flsearch.setObjectName("c_flsearch")
        self.gridLayout.addWidget(self.c_flsearch, 1, 2, 1, 1)
        self.l_dboracle2 = QtWidgets.QLabel(self.centralwidget)
        self.l_dboracle2.setObjectName("l_dboracle2")
        self.gridLayout.addWidget(self.l_dboracle2, 6, 4, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 7, 3, 1, 1)
        self.e_excludepath = QtWidgets.QLineEdit(self.centralwidget)
        self.e_excludepath.setObjectName("e_excludepath")
        self.gridLayout.addWidget(self.e_excludepath, 4, 7, 1, 2)
        self.b_save_pref = QtWidgets.QPushButton(self.centralwidget)
        self.b_save_pref.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_pref.setIcon(icon2)
        self.b_save_pref.setObjectName("b_save_pref")
        self.gridLayout.addWidget(self.b_save_pref, 10, 4, 1, 1)
        self.b_add_line = QtWidgets.QPushButton(self.centralwidget)
        self.b_add_line.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/add.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_add_line.setIcon(icon3)
        self.b_add_line.setObjectName("b_add_line")
        self.gridLayout.addWidget(self.b_add_line, 10, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 10, 1, 1)
        self.b_search = QtWidgets.QPushButton(self.centralwidget)
        self.b_search.setToolTip("")
        self.b_search.setStatusTip("")
        self.b_search.setWhatsThis("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search.setIcon(icon4)
        self.b_search.setObjectName("b_search")
        self.gridLayout.addWidget(self.b_search, 10, 7, 1, 3)
        self.l_stringa2 = QtWidgets.QLabel(self.centralwidget)
        self.l_stringa2.setObjectName("l_stringa2")
        self.gridLayout.addWidget(self.l_stringa2, 0, 4, 1, 3)
        self.l_filter = QtWidgets.QLabel(self.centralwidget)
        self.l_filter.setObjectName("l_filter")
        self.gridLayout.addWidget(self.l_filter, 2, 4, 1, 1)
        self.c_dbsearch = QtWidgets.QCheckBox(self.centralwidget)
        self.c_dbsearch.setObjectName("c_dbsearch")
        self.gridLayout.addWidget(self.c_dbsearch, 5, 2, 1, 1)
        self.e_outputfile = QtWidgets.QLineEdit(self.centralwidget)
        self.e_outputfile.setObjectName("e_outputfile")
        self.gridLayout.addWidget(self.e_outputfile, 10, 2, 1, 1)
        self.l_pathname = QtWidgets.QLabel(self.centralwidget)
        self.l_pathname.setObjectName("l_pathname")
        self.gridLayout.addWidget(self.l_pathname, 1, 4, 1, 2)
        self.l_outputfile = QtWidgets.QLabel(self.centralwidget)
        self.l_outputfile.setObjectName("l_outputfile")
        self.gridLayout.addWidget(self.l_outputfile, 10, 1, 1, 1)
        self.l_stringa1 = QtWidgets.QLabel(self.centralwidget)
        self.l_stringa1.setObjectName("l_stringa1")
        self.gridLayout.addWidget(self.l_stringa1, 0, 0, 1, 2)
        self.e_stringa1 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_stringa1.setObjectName("e_stringa1")
        self.gridLayout.addWidget(self.e_stringa1, 0, 2, 1, 1)
        self.b_excludepath = QtWidgets.QPushButton(self.centralwidget)
        self.b_excludepath.setText("")
        self.b_excludepath.setIcon(icon1)
        self.b_excludepath.setObjectName("b_excludepath")
        self.gridLayout.addWidget(self.b_excludepath, 4, 9, 1, 1)
        self.e_stringa2 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_stringa2.setObjectName("e_stringa2")
        self.gridLayout.addWidget(self.e_stringa2, 0, 7, 1, 3)
        self.l_risultati = QtWidgets.QLabel(self.centralwidget)
        self.l_risultati.setObjectName("l_risultati")
        self.gridLayout.addWidget(self.l_risultati, 11, 1, 1, 1)
        Ricerca_stringhe_window.setCentralWidget(self.centralwidget)
        self.l_excludepath.setBuddy(self.e_excludepath)
        self.l_dboracle1.setBuddy(self.e_dboracle1)
        self.l_dboracle2.setBuddy(self.e_dboracle2)
        self.l_stringa2.setBuddy(self.e_stringa2)
        self.l_filter.setBuddy(self.e_filter)
        self.l_pathname.setBuddy(self.e_pathname)
        self.l_outputfile.setBuddy(self.e_outputfile)
        self.l_stringa1.setBuddy(self.e_stringa1)

        self.retranslateUi(Ricerca_stringhe_window)
        self.o_lst1.doubleClicked['QModelIndex'].connect(Ricerca_stringhe_window.o_lst1_slot)
        self.b_save_pref.clicked.connect(Ricerca_stringhe_window.b_save_slot)
        self.b_add_line.clicked.connect(Ricerca_stringhe_window.b_add_line_slot)
        self.b_pathname.clicked.connect(Ricerca_stringhe_window.b_pathname_slot)
        self.b_excludepath.clicked.connect(Ricerca_stringhe_window.b_excludepath_slot)
        self.b_search.clicked.connect(Ricerca_stringhe_window.b_search_slot)
        QtCore.QMetaObject.connectSlotsByName(Ricerca_stringhe_window)
        Ricerca_stringhe_window.setTabOrder(self.e_stringa1, self.e_stringa2)
        Ricerca_stringhe_window.setTabOrder(self.e_stringa2, self.c_flsearch)
        Ricerca_stringhe_window.setTabOrder(self.c_flsearch, self.e_pathname)
        Ricerca_stringhe_window.setTabOrder(self.e_pathname, self.b_pathname)
        Ricerca_stringhe_window.setTabOrder(self.b_pathname, self.e_filter)
        Ricerca_stringhe_window.setTabOrder(self.e_filter, self.e_excludepath)
        Ricerca_stringhe_window.setTabOrder(self.e_excludepath, self.b_excludepath)
        Ricerca_stringhe_window.setTabOrder(self.b_excludepath, self.c_dbsearch)
        Ricerca_stringhe_window.setTabOrder(self.c_dbsearch, self.e_dboracle1)
        Ricerca_stringhe_window.setTabOrder(self.e_dboracle1, self.e_dboracle2)
        Ricerca_stringhe_window.setTabOrder(self.e_dboracle2, self.e_outputfile)
        Ricerca_stringhe_window.setTabOrder(self.e_outputfile, self.b_save_pref)
        Ricerca_stringhe_window.setTabOrder(self.b_save_pref, self.b_add_line)
        Ricerca_stringhe_window.setTabOrder(self.b_add_line, self.b_search)
        Ricerca_stringhe_window.setTabOrder(self.b_search, self.o_lst1)

    def retranslateUi(self, Ricerca_stringhe_window):
        _translate = QtCore.QCoreApplication.translate
        Ricerca_stringhe_window.setWindowTitle(_translate("Ricerca_stringhe_window", "Search string in sources of Oracle Forms/Reports"))
        self.l_excludepath.setText(_translate("Ricerca_stringhe_window", "Exclude directories"))
        self.l_dboracle1.setText(_translate("Ricerca_stringhe_window", "Oracle connection1"))
        self.c_flsearch.setText(_translate("Ricerca_stringhe_window", "Execute search in folder"))
        self.l_dboracle2.setText(_translate("Ricerca_stringhe_window", "Oracle connection2"))
        self.b_save_pref.setToolTip(_translate("Ricerca_stringhe_window", "<html><head/><body><p>Save the search data in order to be retrieved at the next start of SmiGrep</p></body></html>"))
        self.b_add_line.setToolTip(_translate("Ricerca_stringhe_window", "<html><head/><body><p>Add the selected line to \'My favorites files</p></body></html>"))
        self.b_search.setText(_translate("Ricerca_stringhe_window", "Start search"))
        self.l_stringa2.setText(_translate("Ricerca_stringhe_window", "and Search string2"))
        self.l_filter.setText(_translate("Ricerca_stringhe_window", "File filter"))
        self.c_dbsearch.setText(_translate("Ricerca_stringhe_window", "Execute search in OracleDB"))
        self.l_pathname.setText(_translate("Ricerca_stringhe_window", "Folder name"))
        self.l_outputfile.setText(_translate("Ricerca_stringhe_window", "Output file csv"))
        self.l_stringa1.setText(_translate("Ricerca_stringhe_window", "Search string1"))
        self.l_risultati.setText(_translate("Ricerca_stringhe_window", "Result:"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ricerca_stringhe_window = QtWidgets.QMainWindow()
    ui = Ui_Ricerca_stringhe_window()
    ui.setupUi(Ricerca_stringhe_window)
    Ricerca_stringhe_window.show()
    sys.exit(app.exec_())
