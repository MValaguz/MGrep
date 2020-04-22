# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_jobs_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_jobs_window(object):
    def setupUi(self, oracle_jobs_window):
        oracle_jobs_window.setObjectName("oracle_jobs_window")
        oracle_jobs_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_jobs_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_jobs_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setDragEnabled(True)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 10, 0, 1, 4)
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 4, 1, 1, 1)
        self.l_server_name = QtWidgets.QLabel(self.centralwidget)
        self.l_server_name.setObjectName("l_server_name")
        self.gridLayout.addWidget(self.l_server_name, 4, 0, 1, 1)
        self.l_search1 = QtWidgets.QLabel(self.centralwidget)
        self.l_search1.setObjectName("l_search1")
        self.gridLayout.addWidget(self.l_search1, 5, 0, 1, 1)
        self.e_search1 = QtWidgets.QLineEdit(self.centralwidget)
        self.e_search1.setObjectName("e_search1")
        self.gridLayout.addWidget(self.e_search1, 5, 1, 1, 1)
        self.b_start_search = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_search.setIcon(icon1)
        self.b_start_search.setObjectName("b_start_search")
        self.gridLayout.addWidget(self.b_start_search, 5, 2, 1, 1)
        oracle_jobs_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)

        self.retranslateUi(oracle_jobs_window)
        self.b_start_search.clicked.connect(oracle_jobs_window.slot_startSearch)
        QtCore.QMetaObject.connectSlotsByName(oracle_jobs_window)
        oracle_jobs_window.setTabOrder(self.e_server_name, self.o_lst1)

    def retranslateUi(self, oracle_jobs_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_jobs_window.setWindowTitle(_translate("oracle_jobs_window", "Oracle jobs"))
        self.l_server_name.setText(_translate("oracle_jobs_window", "Oracle name server:"))
        self.l_search1.setText(_translate("oracle_jobs_window", "Search by name or comment:"))
        self.b_start_search.setText(_translate("oracle_jobs_window", "Start search"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_jobs_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_jobs_window()
    ui.setupUi(oracle_jobs_window)
    oracle_jobs_window.show()
    sys.exit(app.exec_())
