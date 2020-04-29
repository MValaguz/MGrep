# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_jobs_history_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_jobs_history_window(object):
    def setupUi(self, oracle_jobs_history_window):
        oracle_jobs_history_window.setObjectName("oracle_jobs_history_window")
        oracle_jobs_history_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_jobs_history_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_jobs_history_window)
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
        self.gridLayout.addWidget(self.o_lst1, 8, 0, 1, 2)
        oracle_jobs_history_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(oracle_jobs_history_window)
        QtCore.QMetaObject.connectSlotsByName(oracle_jobs_history_window)

    def retranslateUi(self, oracle_jobs_history_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_jobs_history_window.setWindowTitle(_translate("oracle_jobs_history_window", "Oracle job\'s history"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_jobs_history_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_jobs_history_window()
    ui.setupUi(oracle_jobs_history_window)
    oracle_jobs_history_window.show()
    sys.exit(app.exec_())
