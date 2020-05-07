# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_top_sessions_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_top_sessions_window(object):
    def setupUi(self, oracle_top_sessions_window):
        oracle_top_sessions_window.setObjectName("oracle_top_sessions_window")
        oracle_top_sessions_window.resize(1000, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/speedometer.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_top_sessions_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_top_sessions_window)
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
        self.gridLayout.addWidget(self.e_server_name, 4, 1, 1, 1)
        self.l_server_name = QtWidgets.QLabel(self.centralwidget)
        self.l_server_name.setObjectName("l_server_name")
        self.gridLayout.addWidget(self.l_server_name, 4, 0, 1, 1)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.o_lst1.setAutoScroll(True)
        self.o_lst1.setDragEnabled(True)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.o_lst1.verticalHeader().setVisible(False)
        self.gridLayout.addWidget(self.o_lst1, 10, 0, 1, 5)
        self.e_parameter = QtWidgets.QComboBox(self.centralwidget)
        self.e_parameter.setToolTip("")
        self.e_parameter.setObjectName("e_parameter")
        self.gridLayout.addWidget(self.e_parameter, 5, 1, 1, 1)
        self.l_parameter = QtWidgets.QLabel(self.centralwidget)
        self.l_parameter.setObjectName("l_parameter")
        self.gridLayout.addWidget(self.l_parameter, 5, 0, 1, 1)
        self.b_calculate = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/gears.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_calculate.setIcon(icon1)
        self.b_calculate.setObjectName("b_calculate")
        self.gridLayout.addWidget(self.b_calculate, 5, 4, 1, 1)
        self.l_total_sessions = QtWidgets.QLabel(self.centralwidget)
        self.l_total_sessions.setAlignment(QtCore.Qt.AlignCenter)
        self.l_total_sessions.setObjectName("l_total_sessions")
        self.gridLayout.addWidget(self.l_total_sessions, 4, 4, 1, 1)
        self.b_help = QtWidgets.QPushButton(self.centralwidget)
        self.b_help.setMaximumSize(QtCore.QSize(24, 24))
        self.b_help.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/help.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_help.setIcon(icon2)
        self.b_help.setObjectName("b_help")
        self.gridLayout.addWidget(self.b_help, 5, 2, 1, 1)
        oracle_top_sessions_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)
        self.l_parameter.setBuddy(self.e_parameter)

        self.retranslateUi(oracle_top_sessions_window)
        self.b_calculate.clicked.connect(oracle_top_sessions_window.slot_calculate)
        self.e_server_name.currentIndexChanged['int'].connect(oracle_top_sessions_window.slot_change_server)
        self.e_parameter.currentIndexChanged['int'].connect(oracle_top_sessions_window.slot_change_server)
        self.b_help.clicked.connect(oracle_top_sessions_window.slot_help)
        QtCore.QMetaObject.connectSlotsByName(oracle_top_sessions_window)
        oracle_top_sessions_window.setTabOrder(self.e_server_name, self.e_parameter)
        oracle_top_sessions_window.setTabOrder(self.e_parameter, self.o_lst1)

    def retranslateUi(self, oracle_top_sessions_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_top_sessions_window.setWindowTitle(_translate("oracle_top_sessions_window", "Oracle top sessions"))
        self.l_server_name.setText(_translate("oracle_top_sessions_window", "Oracle name server:"))
        self.l_parameter.setText(_translate("oracle_top_sessions_window", "Parameter:"))
        self.b_calculate.setText(_translate("oracle_top_sessions_window", "Compute difference now"))
        self.l_total_sessions.setText(_translate("oracle_top_sessions_window", "Number of sessions:"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_top_sessions_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_top_sessions_window()
    ui.setupUi(oracle_top_sessions_window)
    oracle_top_sessions_window.show()
    sys.exit(app.exec_())
