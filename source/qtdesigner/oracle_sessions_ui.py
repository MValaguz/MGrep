# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_sessions_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_oracle_sessions_window(object):
    def setupUi(self, oracle_sessions_window):
        oracle_sessions_window.setObjectName("oracle_sessions_window")
        oracle_sessions_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_sessions_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_sessions_window)
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
        self.gridLayout.addWidget(self.l_server_name, 4, 0, 1, 1)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 13, 0, 1, 9)
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.gridLayout.addWidget(self.line_1, 5, 0, 1, 9)
        self.l_program_name = QtWidgets.QLabel(self.centralwidget)
        self.l_program_name.setObjectName("l_program_name")
        self.gridLayout.addWidget(self.l_program_name, 7, 0, 1, 1)
        self.l_user_name = QtWidgets.QLabel(self.centralwidget)
        self.l_user_name.setObjectName("l_user_name")
        self.gridLayout.addWidget(self.l_user_name, 6, 0, 1, 1)
        self.e_terminal_2 = QtWidgets.QLabel(self.centralwidget)
        self.e_terminal_2.setObjectName("e_terminal_2")
        self.gridLayout.addWidget(self.e_terminal_2, 8, 0, 1, 1)
        self.e_program_name = QtWidgets.QLineEdit(self.centralwidget)
        self.e_program_name.setObjectName("e_program_name")
        self.gridLayout.addWidget(self.e_program_name, 7, 1, 1, 1)
        self.b_start_search = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_search.setIcon(icon1)
        self.b_start_search.setObjectName("b_start_search")
        self.gridLayout.addWidget(self.b_start_search, 8, 8, 1, 1)
        self.e_user_name = QtWidgets.QLineEdit(self.centralwidget)
        self.e_user_name.setObjectName("e_user_name")
        self.gridLayout.addWidget(self.e_user_name, 6, 1, 1, 1)
        self.e_terminal = QtWidgets.QLineEdit(self.centralwidget)
        self.e_terminal.setObjectName("e_terminal")
        self.gridLayout.addWidget(self.e_terminal, 8, 1, 1, 1)
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 4, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.b_session_information = QtWidgets.QPushButton(self.centralwidget)
        self.b_session_information.setMaximumSize(QtCore.QSize(30, 30))
        self.b_session_information.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/sql.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_session_information.setIcon(icon2)
        self.b_session_information.setObjectName("b_session_information")
        self.horizontalLayout.addWidget(self.b_session_information)
        self.b_kill_session = QtWidgets.QPushButton(self.centralwidget)
        self.b_kill_session.setMaximumSize(QtCore.QSize(30, 30))
        self.b_kill_session.setStatusTip("")
        self.b_kill_session.setWhatsThis("")
        self.b_kill_session.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/kill.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_kill_session.setIcon(icon3)
        self.b_kill_session.setObjectName("b_kill_session")
        self.horizontalLayout.addWidget(self.b_kill_session)
        self.gridLayout.addLayout(self.horizontalLayout, 15, 5, 1, 4)
        oracle_sessions_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(oracle_sessions_window)
        self.statusbar.setObjectName("statusbar")
        oracle_sessions_window.setStatusBar(self.statusbar)
        self.l_server_name.setBuddy(self.e_server_name)
        self.l_program_name.setBuddy(self.e_program_name)
        self.l_user_name.setBuddy(self.e_user_name)
        self.e_terminal_2.setBuddy(self.e_terminal)

        self.retranslateUi(oracle_sessions_window)
        self.e_user_name.returnPressed.connect(oracle_sessions_window.slot_search_session)
        self.e_program_name.returnPressed.connect(oracle_sessions_window.slot_search_session)
        self.e_terminal.returnPressed.connect(oracle_sessions_window.slot_search_session)
        self.b_start_search.clicked.connect(oracle_sessions_window.slot_search_session)
        self.b_kill_session.clicked.connect(oracle_sessions_window.slot_kill_session)
        self.b_session_information.clicked.connect(oracle_sessions_window.slot_log_session)
        QtCore.QMetaObject.connectSlotsByName(oracle_sessions_window)

    def retranslateUi(self, oracle_sessions_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_sessions_window.setWindowTitle(_translate("oracle_sessions_window", "Oracle sessions list"))
        self.l_server_name.setText(_translate("oracle_sessions_window", "Oracle name server:"))
        self.l_program_name.setText(_translate("oracle_sessions_window", "Program name:"))
        self.l_user_name.setText(_translate("oracle_sessions_window", "User name:"))
        self.e_terminal_2.setText(_translate("oracle_sessions_window", "Terminal:"))
        self.b_start_search.setText(_translate("oracle_sessions_window", "Start search"))
        self.b_session_information.setToolTip(_translate("oracle_sessions_window", "Create a file with session information"))
        self.b_kill_session.setToolTip(_translate("oracle_sessions_window", "Kill selected session"))

import resource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_sessions_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_sessions_window()
    ui.setupUi(oracle_sessions_window)
    oracle_sessions_window.show()
    sys.exit(app.exec_())

