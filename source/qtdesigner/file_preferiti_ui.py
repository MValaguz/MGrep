# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'file_preferiti_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_file_preferiti_window(object):
    def setupUi(self, file_preferiti_window):
        file_preferiti_window.setObjectName("file_preferiti_window")
        file_preferiti_window.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        file_preferiti_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(file_preferiti_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_4.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_4.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/zip.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 11, 1, 1)
        self.b_add_line = QtWidgets.QPushButton(self.centralwidget)
        self.b_add_line.setMinimumSize(QtCore.QSize(30, 30))
        self.b_add_line.setMaximumSize(QtCore.QSize(30, 30))
        self.b_add_line.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/down.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_add_line.setIcon(icon2)
        self.b_add_line.setObjectName("b_add_line")
        self.gridLayout.addWidget(self.b_add_line, 0, 5, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_9.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_9.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/icom.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_9.setIcon(icon3)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout.addWidget(self.pushButton_9, 0, 13, 1, 1)
        self.b_search = QtWidgets.QPushButton(self.centralwidget)
        self.b_search.setMinimumSize(QtCore.QSize(30, 30))
        self.b_search.setMaximumSize(QtCore.QSize(30, 30))
        self.b_search.setToolTip("")
        self.b_search.setStatusTip("")
        self.b_search.setWhatsThis("")
        self.b_search.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/failed.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_search.setIcon(icon4)
        self.b_search.setObjectName("b_search")
        self.gridLayout.addWidget(self.b_search, 0, 6, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_8.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_8.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/icom_backup.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_8.setIcon(icon5)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout.addWidget(self.pushButton_8, 0, 14, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_7.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_7.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/icom_backup_2.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon6)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 0, 15, 1, 1)
        self.b_save_pref = QtWidgets.QPushButton(self.centralwidget)
        self.b_save_pref.setMinimumSize(QtCore.QSize(30, 30))
        self.b_save_pref.setMaximumSize(QtCore.QSize(30, 30))
        self.b_save_pref.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/up.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save_pref.setIcon(icon7)
        self.b_save_pref.setObjectName("b_save_pref")
        self.gridLayout.addWidget(self.b_save_pref, 0, 4, 1, 1)
        self.b_pathname = QtWidgets.QPushButton(self.centralwidget)
        self.b_pathname.setMinimumSize(QtCore.QSize(30, 30))
        self.b_pathname.setMaximumSize(QtCore.QSize(30, 30))
        self.b_pathname.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/refresh.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_pathname.setIcon(icon8)
        self.b_pathname.setObjectName("b_pathname")
        self.gridLayout.addWidget(self.b_pathname, 0, 2, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/clear.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon9)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 7, 1, 1)
        self.b_excludepath = QtWidgets.QPushButton(self.centralwidget)
        self.b_excludepath.setMinimumSize(QtCore.QSize(30, 30))
        self.b_excludepath.setMaximumSize(QtCore.QSize(30, 30))
        self.b_excludepath.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/line.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_excludepath.setIcon(icon10)
        self.b_excludepath.setObjectName("b_excludepath")
        self.gridLayout.addWidget(self.b_excludepath, 0, 3, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_2.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon11)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 8, 1, 1)
        self.l_risultati = QtWidgets.QLabel(self.centralwidget)
        self.l_risultati.setObjectName("l_risultati")
        self.gridLayout.addWidget(self.l_risultati, 0, 9, 1, 1)
        self.l_titolo1 = QtWidgets.QLabel(self.centralwidget)
        self.l_titolo1.setObjectName("l_titolo1")
        self.gridLayout.addWidget(self.l_titolo1, 0, 0, 1, 2)
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_6.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_6.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/icons/smile_backup.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon12)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 0, 16, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_5.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_5.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/icons/smile_backup_2.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon13)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 0, 17, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_3.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_3.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon14)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 10, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_10.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_10.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/icons/upload1.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_10.setIcon(icon15)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout.addWidget(self.pushButton_10, 0, 12, 1, 1)
        self.o_lst1 = QtWidgets.QListView(self.centralwidget)
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 8, 0, 1, 18)
        file_preferiti_window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(file_preferiti_window)
        self.statusbar.setObjectName("statusbar")
        file_preferiti_window.setStatusBar(self.statusbar)
        self.l_risultati.setBuddy(self.pushButton_3)
        self.l_titolo1.setBuddy(self.b_pathname)

        self.retranslateUi(file_preferiti_window)
        QtCore.QMetaObject.connectSlotsByName(file_preferiti_window)

    def retranslateUi(self, file_preferiti_window):
        _translate = QtCore.QCoreApplication.translate
        file_preferiti_window.setWindowTitle(_translate("file_preferiti_window", "My favorites files"))
        self.b_add_line.setToolTip(_translate("file_preferiti_window", "<html><head/><body><p>Add the selected line to \'My favorites files</p></body></html>"))
        self.b_save_pref.setToolTip(_translate("file_preferiti_window", "<html><head/><body><p>Save the search data in order to be retrieved at the next start of SmiGrep</p></body></html>"))
        self.l_risultati.setText(_translate("file_preferiti_window", "Item actions:"))
        self.l_titolo1.setText(_translate("file_preferiti_window", "List actions:"))

import resource_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    file_preferiti_window = QtWidgets.QMainWindow()
    ui = Ui_file_preferiti_window()
    ui.setupUi(file_preferiti_window)
    file_preferiti_window.show()
    sys.exit(app.exec_())

