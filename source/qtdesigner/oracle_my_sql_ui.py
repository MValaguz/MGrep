# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oracle_my_sql_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oracle_my_sql_window(object):
    def setupUi(self, oracle_my_sql_window):
        oracle_my_sql_window.setObjectName("oracle_my_sql_window")
        oracle_my_sql_window.resize(748, 635)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        oracle_my_sql_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(oracle_my_sql_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.e_sql = QtWidgets.QTextEdit(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_sql.setFont(font)
        self.e_sql.setObjectName("e_sql")
        self.o_table = QtWidgets.QTableWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.o_table.sizePolicy().hasHeightForWidth())
        self.o_table.setSizePolicy(sizePolicy)
        self.o_table.setAlternatingRowColors(True)
        self.o_table.setGridStyle(QtCore.Qt.SolidLine)
        self.o_table.setObjectName("o_table")
        self.o_table.setColumnCount(0)
        self.o_table.setRowCount(0)
        self.o_table.horizontalHeader().setSortIndicatorShown(True)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        oracle_my_sql_window.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(oracle_my_sql_window)
        self.toolBar.setObjectName("toolBar")
        oracle_my_sql_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusBar = QtWidgets.QStatusBar(oracle_my_sql_window)
        self.statusBar.setEnabled(True)
        self.statusBar.setSizeGripEnabled(True)
        self.statusBar.setObjectName("statusBar")
        oracle_my_sql_window.setStatusBar(self.statusBar)
        self.actionLoad_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_sql.setIcon(icon1)
        self.actionLoad_sql.setObjectName("actionLoad_sql")
        self.actionSave_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_sql.setIcon(icon2)
        self.actionSave_sql.setObjectName("actionSave_sql")
        self.actionExecute_sql = QtWidgets.QAction(oracle_my_sql_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExecute_sql.setIcon(icon3)
        self.actionExecute_sql.setObjectName("actionExecute_sql")
        self.actionCommit = QtWidgets.QAction(oracle_my_sql_window)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/confirm.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCommit.setIcon(icon4)
        self.actionCommit.setObjectName("actionCommit")
        self.toolBar.addAction(self.actionLoad_sql)
        self.toolBar.addAction(self.actionSave_sql)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExecute_sql)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCommit)

        self.retranslateUi(oracle_my_sql_window)
        self.actionLoad_sql.triggered.connect(oracle_my_sql_window.slot_load)
        self.actionSave_sql.triggered.connect(oracle_my_sql_window.slot_save)
        self.actionExecute_sql.triggered.connect(oracle_my_sql_window.slot_execute)
        self.actionCommit.triggered.connect(oracle_my_sql_window.slot_commit)
        QtCore.QMetaObject.connectSlotsByName(oracle_my_sql_window)

    def retranslateUi(self, oracle_my_sql_window):
        _translate = QtCore.QCoreApplication.translate
        oracle_my_sql_window.setWindowTitle(_translate("oracle_my_sql_window", "Oracle My Sql"))
        self.o_table.setSortingEnabled(True)
        self.toolBar.setWindowTitle(_translate("oracle_my_sql_window", "toolBar"))
        self.actionLoad_sql.setText(_translate("oracle_my_sql_window", "Load sql"))
        self.actionLoad_sql.setToolTip(_translate("oracle_my_sql_window", "Load a file sql"))
        self.actionSave_sql.setText(_translate("oracle_my_sql_window", "Save sql"))
        self.actionSave_sql.setToolTip(_translate("oracle_my_sql_window", "Save sql into a file"))
        self.actionExecute_sql.setText(_translate("oracle_my_sql_window", "Execute sql"))
        self.actionExecute_sql.setToolTip(_translate("oracle_my_sql_window", "Execute de sql statement"))
        self.actionExecute_sql.setShortcut(_translate("oracle_my_sql_window", "F5"))
        self.actionCommit.setText(_translate("oracle_my_sql_window", "Commit changes"))
        self.actionCommit.setToolTip(_translate("oracle_my_sql_window", "Commit the changes on the sql results"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    oracle_my_sql_window = QtWidgets.QMainWindow()
    ui = Ui_oracle_my_sql_window()
    ui.setupUi(oracle_my_sql_window)
    oracle_my_sql_window.show()
    sys.exit(app.exec_())
