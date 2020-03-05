# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_volume_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_volume_window(object):
    def setupUi(self, oracle_volume_window):
        oracle_volume_window.setObjectName("oracle_volume_window")
        oracle_volume_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_volume_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_volume_window)
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
        self.line_1 = QtWidgets.QFrame(self.centralwidget)
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
        self.gridLayout.addWidget(self.line_1, 5, 0, 1, 7)
        self.e_server_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_server_name.setObjectName("e_server_name")
        self.gridLayout.addWidget(self.e_server_name, 4, 1, 1, 1)
        self.b_start_search = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_search.setIcon(icon1)
        self.b_start_search.setObjectName("b_start_search")
        self.gridLayout.addWidget(self.b_start_search, 4, 5, 1, 1)
        self.l_table_name = QtWidgets.QLabel(self.centralwidget)
        self.l_table_name.setObjectName("l_table_name")
        self.gridLayout.addWidget(self.l_table_name, 4, 3, 1, 1)
        self.e_table_name = QtWidgets.QLineEdit(self.centralwidget)
        self.e_table_name.setObjectName("e_table_name")
        self.gridLayout.addWidget(self.e_table_name, 4, 4, 1, 1)
        self.l_megabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_megabyte.setObjectName("l_megabyte")
        self.gridLayout.addWidget(self.l_megabyte, 12, 0, 1, 1)
        self.l_gigabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_gigabyte.setObjectName("l_gigabyte")
        self.gridLayout.addWidget(self.l_gigabyte, 13, 0, 1, 1)
        self.l_terabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_terabyte.setObjectName("l_terabyte")
        self.gridLayout.addWidget(self.l_terabyte, 14, 0, 1, 1)
        self.l_tot_megabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_tot_megabyte.setObjectName("l_tot_megabyte")
        self.gridLayout.addWidget(self.l_tot_megabyte, 12, 1, 1, 1)
        self.l_tot_gigabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_tot_gigabyte.setObjectName("l_tot_gigabyte")
        self.gridLayout.addWidget(self.l_tot_gigabyte, 13, 1, 1, 1)
        self.l_tot_terabyte = QtWidgets.QLabel(self.centralwidget)
        self.l_tot_terabyte.setObjectName("l_tot_terabyte")
        self.gridLayout.addWidget(self.l_tot_terabyte, 14, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 14, 4, 1, 2)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        self.o_lst1.setMinimumSize(QtCore.QSize(0, 0))
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 11, 0, 1, 4)
        oracle_volume_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)
        self.l_table_name.setBuddy(self.e_table_name)

        self.retranslateUi(oracle_volume_window)
        self.b_start_search.clicked.connect(oracle_volume_window.slot_start_search)
        QtCore.QMetaObject.connectSlotsByName(oracle_volume_window)
        oracle_volume_window.setTabOrder(self.e_server_name, self.e_table_name)
        oracle_volume_window.setTabOrder(self.e_table_name, self.b_start_search)
        oracle_volume_window.setTabOrder(self.b_start_search, self.o_lst1)

    def retranslateUi(self, oracle_volume_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_volume_window.setWindowTitle(_translate("oracle_volume_window", "Oracle volume"))
        self.l_server_name.setText(_translate("oracle_volume_window", "Oracle name server:"))
        self.b_start_search.setText(_translate("oracle_volume_window", "Start search"))
        self.l_table_name.setText(_translate("oracle_volume_window", "Table name:"))
        self.l_megabyte.setText(_translate("oracle_volume_window", "Total size in Megabyte:"))
        self.l_gigabyte.setText(_translate("oracle_volume_window", "Totale size in Gigabyte:"))
        self.l_terabyte.setText(_translate("oracle_volume_window", "Totale size in Terabyte:"))
        self.l_tot_megabyte.setText(_translate("oracle_volume_window", "..."))
        self.l_tot_gigabyte.setText(_translate("oracle_volume_window", "..."))
        self.l_tot_terabyte.setText(_translate("oracle_volume_window", "..."))
        self.label.setText(_translate("oracle_volume_window", "Note: Tables size also includes the size of related indexes"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_volume_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_volume_window()
    ui.setupUi(oracle_volume_window)
    oracle_volume_window.show()
    sys.exit(app.exec_())
