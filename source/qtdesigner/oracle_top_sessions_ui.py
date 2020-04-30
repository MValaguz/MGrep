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
        self.l_server_name = QtWidgets.QLabel(self.centralwidget)
        self.l_server_name.setObjectName("l_server_name")
        self.gridLayout.addWidget(self.l_server_name, 4, 0, 1, 1)
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 4, 1, 1, 1)
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
        self.gridLayout.addWidget(self.o_lst1, 10, 0, 1, 6)
        self.e_parameter = QtWidgets.QComboBox(self.centralwidget)
        self.e_parameter.setObjectName("e_parameter")
        self.gridLayout.addWidget(self.e_parameter, 5, 1, 1, 1)
        self.l_parameter = QtWidgets.QLabel(self.centralwidget)
        self.l_parameter.setObjectName("l_parameter")
        self.gridLayout.addWidget(self.l_parameter, 5, 0, 1, 1)
        self.l_date = QtWidgets.QLabel(self.centralwidget)
        self.l_date.setObjectName("l_date")
        self.gridLayout.addWidget(self.l_date, 6, 0, 1, 1)
        self.e_saved_time = QtWidgets.QComboBox(self.centralwidget)
        self.e_saved_time.setObjectName("e_saved_time")
        self.gridLayout.addWidget(self.e_saved_time, 6, 1, 1, 1)
        self.b_save_point = QtWidgets.QPushButton(self.centralwidget)
        self.b_save_point.setMaximumSize(QtCore.QSize(25, 25))
        self.b_save_point.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_point.setIcon(icon1)
        self.b_save_point.setObjectName("b_save_point")
        self.gridLayout.addWidget(self.b_save_point, 6, 2, 1, 1)
        self.b_calculate = QtWidgets.QPushButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/gears.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_calculate.setIcon(icon2)
        self.b_calculate.setObjectName("b_calculate")
        self.gridLayout.addWidget(self.b_calculate, 6, 5, 1, 1)
        oracle_top_sessions_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)
        self.l_parameter.setBuddy(self.e_parameter)
        self.l_date.setBuddy(self.e_saved_time)

        self.retranslateUi(oracle_top_sessions_window)
        self.b_calculate.clicked.connect(oracle_top_sessions_window.slot_calculate)
        self.e_server_name.currentIndexChanged['int'].connect(oracle_top_sessions_window.slot_change_server)
        self.e_parameter.currentIndexChanged['int'].connect(oracle_top_sessions_window.slot_change_server)
        self.b_save_point.clicked.connect(oracle_top_sessions_window.slot_save_point)
        self.e_saved_time.currentIndexChanged['int'].connect(oracle_top_sessions_window.slot_change_save_point)
        QtCore.QMetaObject.connectSlotsByName(oracle_top_sessions_window)
        oracle_top_sessions_window.setTabOrder(self.e_server_name, self.e_parameter)
        oracle_top_sessions_window.setTabOrder(self.e_parameter, self.e_saved_time)
        oracle_top_sessions_window.setTabOrder(self.e_saved_time, self.b_save_point)
        oracle_top_sessions_window.setTabOrder(self.b_save_point, self.b_calculate)
        oracle_top_sessions_window.setTabOrder(self.b_calculate, self.o_lst1)

    def retranslateUi(self, oracle_top_sessions_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_top_sessions_window.setWindowTitle(_translate("oracle_top_sessions_window", "Oracle top sessions"))
        self.l_server_name.setText(_translate("oracle_top_sessions_window", "Oracle name server:"))
        self.l_parameter.setText(_translate("oracle_top_sessions_window", "Parameter:"))
        self.l_date.setText(_translate("oracle_top_sessions_window", "Saved point at time:"))
        self.b_save_point.setToolTip(_translate("oracle_top_sessions_window", "Save the actual top sessions situation"))
        self.b_calculate.setText(_translate("oracle_top_sessions_window", "Compute difference now"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_top_sessions_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_top_sessions_window()
    ui.setupUi(oracle_top_sessions_window)
    oracle_top_sessions_window.show()
    sys.exit(app.exec_())
