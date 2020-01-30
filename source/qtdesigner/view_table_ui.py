# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_table_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_table_view_window(object):
    def setupUi(self, table_view_window):
        table_view_window.setObjectName("table_view_window")
        table_view_window.resize(700, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        table_view_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(table_view_window)
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
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setDragEnabled(True)
        self.o_lst1.setAlternatingRowColors(True)
        self.o_lst1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.o_lst1.setSortingEnabled(True)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 9, 0, 1, 3)
        table_view_window.setCentralWidget(self.centralwidget)

        self.retranslateUi(table_view_window)
        QtCore.QMetaObject.connectSlotsByName(table_view_window)

    def retranslateUi(self, table_view_window):
        _translate = QtCore.QCoreApplication.translate
        table_view_window.setWindowTitle(_translate("table_view_window", "Table view"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    table_view_window = QtWidgets.QMainWindow()
    ui = Ui_table_view_window()
    ui.setupUi(table_view_window)
    table_view_window.show()
    sys.exit(app.exec_())
