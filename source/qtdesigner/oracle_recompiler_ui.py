# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_recompiler_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_oracle_recompiler_window(object):
    def setupUi(self, oracle_recompiler_window):
        oracle_recompiler_window.setObjectName("oracle_recompiler_window")
        oracle_recompiler_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_recompiler_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_recompiler_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.l_server_name = QtWidgets.QLabel(self.centralwidget)
        self.l_server_name.setObjectName("l_server_name")
        self.gridLayout.addWidget(self.l_server_name, 0, 0, 1, 1)
        self.b_compile_all = QtWidgets.QPushButton(self.centralwidget)
        self.b_compile_all.setToolTip("")
        self.b_compile_all.setStatusTip("")
        self.b_compile_all.setWhatsThis("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/compile.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_compile_all.setIcon(icon1)
        self.b_compile_all.setObjectName("b_compile_all")
        self.gridLayout.addWidget(self.b_compile_all, 5, 2, 1, 2)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 8, 0, 1, 4)
        self.b_search_all = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/search.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search_all.setIcon(icon2)
        self.b_search_all.setObjectName("b_search_all")
        self.gridLayout.addWidget(self.b_search_all, 5, 0, 1, 2)
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 0, 1, 1, 1)
        oracle_recompiler_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(oracle_recompiler_window)
        self.statusbar.setObjectName("statusbar")
        oracle_recompiler_window.setStatusBar(self.statusbar)
        self.l_server_name.setBuddy(self.e_server_name)

        self.retranslateUi(oracle_recompiler_window)
        self.b_compile_all.clicked.connect(oracle_recompiler_window.slot_b_compile_all)
        self.b_search_all.clicked.connect(oracle_recompiler_window.slot_b_search_all)
        QtCore.QMetaObject.connectSlotsByName(oracle_recompiler_window)
        oracle_recompiler_window.setTabOrder(self.e_server_name, self.b_search_all)
        oracle_recompiler_window.setTabOrder(self.b_search_all, self.b_compile_all)
        oracle_recompiler_window.setTabOrder(self.b_compile_all, self.o_lst1)

    def retranslateUi(self, oracle_recompiler_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_recompiler_window.setWindowTitle(_translate("oracle_recompiler_window", "Oracle recompiler"))
        self.l_server_name.setText(_translate("oracle_recompiler_window", "Oracle name server:"))
        self.b_compile_all.setText(_translate("oracle_recompiler_window", "Compile all invalid object"))
        self.b_search_all.setText(_translate("oracle_recompiler_window", "Search invalid object"))

import resource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_recompiler_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_recompiler_window()
    ui.setupUi(oracle_recompiler_window)
    oracle_recompiler_window.show()
    sys.exit(app.exec_())

