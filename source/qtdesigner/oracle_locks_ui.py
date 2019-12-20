# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_locks_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_locks_window(object):
    def setupUi(self, oracle_locks_window):
        oracle_locks_window.setObjectName("oracle_locks_window")
        oracle_locks_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_locks_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_locks_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 4, 2, 1, 1)
        self.b_kill_session_lock = QtWidgets.QPushButton(self.centralwidget)
        self.b_kill_session_lock.setMaximumSize(QtCore.QSize(30, 30))
        self.b_kill_session_lock.setStatusTip("")
        self.b_kill_session_lock.setWhatsThis("")
        self.b_kill_session_lock.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/kill.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_kill_session_lock.setIcon(icon1)
        self.b_kill_session_lock.setObjectName("b_kill_session_lock")
        self.gridLayout.addWidget(self.b_kill_session_lock, 15, 5, 1, 1)
        self.b_kill_table_lock = QtWidgets.QPushButton(self.centralwidget)
        self.b_kill_table_lock.setMaximumSize(QtCore.QSize(30, 30))
        self.b_kill_table_lock.setText("")
        self.b_kill_table_lock.setIcon(icon1)
        self.b_kill_table_lock.setObjectName("b_kill_table_lock")
        self.gridLayout.addWidget(self.b_kill_table_lock, 20, 5, 1, 1)
        self.l_server_name = QtWidgets.QLabel(self.centralwidget)
        self.l_server_name.setObjectName("l_server_name")
        self.gridLayout.addWidget(self.l_server_name, 4, 0, 1, 1)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 13, 0, 1, 6)
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.gridLayout.addWidget(self.line_1, 5, 0, 1, 6)
        self.l_table_name = QtWidgets.QLabel(self.centralwidget)
        self.l_table_name.setObjectName("l_table_name")
        self.gridLayout.addWidget(self.l_table_name, 18, 0, 1, 1)
        self.e_table_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_table_name.setEditable(True)
        self.e_table_name.setObjectName("e_table_name")
        self.gridLayout.addWidget(self.e_table_name, 18, 2, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 16, 0, 1, 6)
        self.o_lst2 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.o_lst2.setSortingEnabled(True)
        self.o_lst2.setObjectName("o_lst2")
        self.gridLayout.addWidget(self.o_lst2, 19, 0, 1, 6)
        self.b_table_lock = QtWidgets.QPushButton(self.centralwidget)
        self.b_table_lock.setMaximumSize(QtCore.QSize(30, 30))
        self.b_table_lock.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_table_lock.setIcon(icon2)
        self.b_table_lock.setObjectName("b_table_lock")
        self.gridLayout.addWidget(self.b_table_lock, 18, 3, 1, 1)
        self.b_session_lock = QtWidgets.QPushButton(self.centralwidget)
        self.b_session_lock.setIcon(icon2)
        self.b_session_lock.setObjectName("b_session_lock")
        self.gridLayout.addWidget(self.b_session_lock, 7, 2, 1, 1)
        self.b_load_list_table = QtWidgets.QPushButton(self.centralwidget)
        self.b_load_list_table.setMaximumSize(QtCore.QSize(30, 30))
        self.b_load_list_table.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/table.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_load_list_table.setIcon(icon3)
        self.b_load_list_table.setObjectName("b_load_list_table")
        self.gridLayout.addWidget(self.b_load_list_table, 18, 1, 1, 1)
        oracle_locks_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)
        self.l_table_name.setBuddy(self.e_table_name)

        self.retranslateUi(oracle_locks_window)
        self.b_session_lock.clicked.connect(oracle_locks_window.slot_search_session_lock)
        self.b_kill_session_lock.clicked.connect(oracle_locks_window.slot_kill_session_lock)
        self.b_table_lock.clicked.connect(oracle_locks_window.slot_search_table_lock)
        self.b_kill_table_lock.clicked.connect(oracle_locks_window.slot_kill_table_lock)
        self.b_load_list_table.clicked.connect(oracle_locks_window.slot_load_table_list)
        QtCore.QMetaObject.connectSlotsByName(oracle_locks_window)
        oracle_locks_window.setTabOrder(self.e_server_name, self.b_session_lock)
        oracle_locks_window.setTabOrder(self.b_session_lock, self.o_lst1)
        oracle_locks_window.setTabOrder(self.o_lst1, self.b_kill_session_lock)
        oracle_locks_window.setTabOrder(self.b_kill_session_lock, self.b_load_list_table)
        oracle_locks_window.setTabOrder(self.b_load_list_table, self.e_table_name)
        oracle_locks_window.setTabOrder(self.e_table_name, self.b_table_lock)
        oracle_locks_window.setTabOrder(self.b_table_lock, self.o_lst2)
        oracle_locks_window.setTabOrder(self.o_lst2, self.b_kill_table_lock)

    def retranslateUi(self, oracle_locks_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_locks_window.setWindowTitle(_translate("oracle_locks_window", "Oracle locks"))
        self.b_kill_session_lock.setToolTip(_translate("oracle_locks_window", "Kill selected session"))
        self.b_kill_table_lock.setToolTip(_translate("oracle_locks_window", "Kill selected session"))
        self.l_server_name.setText(_translate("oracle_locks_window", "Oracle name server:"))
        self.l_table_name.setText(_translate("oracle_locks_window", "Table Name:"))
        self.b_table_lock.setToolTip(_translate("oracle_locks_window", "Search lock table"))
        self.b_session_lock.setText(_translate("oracle_locks_window", "Check session lock"))
        self.b_load_list_table.setToolTip(_translate("oracle_locks_window", "Load into combo box the list of tables"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_locks_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_locks_window()
    ui.setupUi(oracle_locks_window)
    oracle_locks_window.show()
    sys.exit(app.exec_())
