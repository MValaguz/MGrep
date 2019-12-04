# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rubrica_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_rubrica_window(object):
    def setupUi(self, rubrica_window):
        rubrica_window.setObjectName("rubrica_window")
        rubrica_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        rubrica_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(rubrica_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.b_ricerca = QtWidgets.QPushButton(self.centralwidget)
        self.b_ricerca.setToolTip("")
        self.b_ricerca.setStatusTip("")
        self.b_ricerca.setWhatsThis("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_ricerca.setIcon(icon1)
        self.b_ricerca.setObjectName("b_ricerca")
        self.gridLayout.addWidget(self.b_ricerca, 0, 3, 1, 1)
        self.l_ricerca = QtWidgets.QLabel(self.centralwidget)
        self.l_ricerca.setObjectName("l_ricerca")
        self.gridLayout.addWidget(self.l_ricerca, 0, 0, 1, 2)
        self.e_ricerca = QtWidgets.QLineEdit(self.centralwidget)
        self.e_ricerca.setObjectName("e_ricerca")
        self.gridLayout.addWidget(self.e_ricerca, 0, 2, 1, 1)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 1, 0, 1, 4)
        rubrica_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(rubrica_window)
        self.statusbar.setObjectName("statusbar")
        rubrica_window.setStatusBar(self.statusbar)
        self.l_ricerca.setBuddy(self.e_ricerca)

        self.retranslateUi(rubrica_window)
        self.b_ricerca.clicked.connect(rubrica_window.slot_b_ricerca)
        self.e_ricerca.returnPressed.connect(rubrica_window.slot_b_ricerca)
        QtCore.QMetaObject.connectSlotsByName(rubrica_window)

    def retranslateUi(self, rubrica_window):
        _translate = QtCore.QCoreApplication.translate
        rubrica_window.setWindowTitle(_translate("rubrica_window", "Book"))
        self.b_ricerca.setText(_translate("rubrica_window", "Start search"))
        self.l_ricerca.setText(_translate("rubrica_window", "Search"))

import resource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    rubrica_window = QtWidgets.QMainWindow()
    ui = Ui_rubrica_window()
    ui.setupUi(rubrica_window)
    rubrica_window.show()
    sys.exit(app.exec_())

