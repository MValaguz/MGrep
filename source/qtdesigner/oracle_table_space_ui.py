# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_table_space_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_table_space_window(object):
    def setupUi(self, oracle_table_space_window):
        oracle_table_space_window.setObjectName("oracle_table_space_window")
        oracle_table_space_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_table_space_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_table_space_window)
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
        self.o_lst2 = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(30)
        sizePolicy.setHeightForWidth(self.o_lst2.sizePolicy().hasHeightForWidth())
        self.o_lst2.setSizePolicy(sizePolicy)
        self.o_lst2.setObjectName("o_lst2")
        self.gridLayout.addWidget(self.o_lst2, 12, 0, 1, 3)
        self.o_lst1 = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.o_lst1.sizePolicy().hasHeightForWidth())
        self.o_lst1.setSizePolicy(sizePolicy)
        self.o_lst1.setDragEnabled(True)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 10, 0, 1, 3)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/sql.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 13, 1, 1, 1)
        self.e_sql_script = QtWidgets.QLineEdit(self.centralwidget)
        self.e_sql_script.setObjectName("e_sql_script")
        self.gridLayout.addWidget(self.e_sql_script, 14, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 5, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 11, 0, 1, 3)
        oracle_table_space_window.setCentralWidget(self.centralwidget)
        self.l_server_name.setBuddy(self.e_server_name)

        self.retranslateUi(oracle_table_space_window)
        self.e_server_name.currentIndexChanged['int'].connect(oracle_table_space_window.slot_changed_server)
        self.o_lst1.clicked['QModelIndex'].connect(oracle_table_space_window.slot_table_space_selected)
        self.pushButton.clicked.connect(oracle_table_space_window.slot_create_script)
        QtCore.QMetaObject.connectSlotsByName(oracle_table_space_window)
        oracle_table_space_window.setTabOrder(self.e_server_name, self.o_lst1)

    def retranslateUi(self, oracle_table_space_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_table_space_window.setWindowTitle(_translate("oracle_table_space_window", "Oracle table space"))
        self.l_server_name.setText(_translate("oracle_table_space_window", "Oracle name server:"))
        self.pushButton.setToolTip(_translate("oracle_table_space_window", "<html><head/><body><p>1) Select a table space</p><p>2) Click this button</p><p>3) The script is composed in the text box below, with a new numeric part</p></body></html>"))
        self.pushButton.setText(_translate("oracle_table_space_window", "Create script for add space to a tablespace"))
        self.label.setText(_translate("oracle_table_space_window", "List of table spaces:"))
        self.label_2.setText(_translate("oracle_table_space_window", "DBfiles linked to tablespace:"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_table_space_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_table_space_window()
    ui.setupUi(oracle_table_space_window)
    oracle_table_space_window.show()
    sys.exit(app.exec_())
