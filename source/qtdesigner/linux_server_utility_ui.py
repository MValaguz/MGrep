# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'linux_server_utility_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_linux_server_window(object):
    def setupUi(self, linux_server_window):
        linux_server_window.setObjectName("linux_server_window")
        linux_server_window.resize(801, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/console.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        linux_server_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(linux_server_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.l_icom_815 = QtWidgets.QLabel(self.centralwidget)
        self.l_icom_815.setObjectName("l_icom_815")
        self.gridLayout.addWidget(self.l_icom_815, 0, 0, 1, 1)
        self.l_backup_815 = QtWidgets.QLabel(self.centralwidget)
        self.l_backup_815.setObjectName("l_backup_815")
        self.gridLayout.addWidget(self.l_backup_815, 2, 0, 1, 1)
        self.e_backup_815 = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_backup_815.setFont(font)
        self.e_backup_815.setReadOnly(True)
        self.e_backup_815.setObjectName("e_backup_815")
        self.gridLayout.addWidget(self.e_backup_815, 3, 0, 1, 1)
        self.l_backup_2_815 = QtWidgets.QLabel(self.centralwidget)
        self.l_backup_2_815.setObjectName("l_backup_2_815")
        self.gridLayout.addWidget(self.l_backup_2_815, 4, 0, 1, 1)
        self.e_backup_2_815 = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_backup_2_815.setFont(font)
        self.e_backup_2_815.setReadOnly(True)
        self.e_backup_2_815.setObjectName("e_backup_2_815")
        self.gridLayout.addWidget(self.e_backup_2_815, 5, 0, 1, 1)
        self.e_icom_815 = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_icom_815.setFont(font)
        self.e_icom_815.setReadOnly(True)
        self.e_icom_815.setObjectName("e_icom_815")
        self.gridLayout.addWidget(self.e_icom_815, 1, 0, 1, 1)
        self.e_ias_smile_reale = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_ias_smile_reale.setFont(font)
        self.e_ias_smile_reale.setReadOnly(True)
        self.e_ias_smile_reale.setObjectName("e_ias_smile_reale")
        self.gridLayout.addWidget(self.e_ias_smile_reale, 1, 1, 1, 1)
        self.l_ias_smile_reale = QtWidgets.QLabel(self.centralwidget)
        self.l_ias_smile_reale.setObjectName("l_ias_smile_reale")
        self.gridLayout.addWidget(self.l_ias_smile_reale, 0, 1, 1, 1)
        self.l_ias_smile_backup = QtWidgets.QLabel(self.centralwidget)
        self.l_ias_smile_backup.setObjectName("l_ias_smile_backup")
        self.gridLayout.addWidget(self.l_ias_smile_backup, 2, 1, 1, 1)
        self.e_ias_smile_backup = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_ias_smile_backup.setFont(font)
        self.e_ias_smile_backup.setReadOnly(True)
        self.e_ias_smile_backup.setObjectName("e_ias_smile_backup")
        self.gridLayout.addWidget(self.e_ias_smile_backup, 3, 1, 1, 1)
        self.l_ias_smile_backup2 = QtWidgets.QLabel(self.centralwidget)
        self.l_ias_smile_backup2.setObjectName("l_ias_smile_backup2")
        self.gridLayout.addWidget(self.l_ias_smile_backup2, 4, 1, 1, 1)
        self.e_ias_smile_backup2 = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(10)
        self.e_ias_smile_backup2.setFont(font)
        self.e_ias_smile_backup2.setReadOnly(True)
        self.e_ias_smile_backup2.setObjectName("e_ias_smile_backup2")
        self.gridLayout.addWidget(self.e_ias_smile_backup2, 5, 1, 1, 1)
        linux_server_window.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(linux_server_window)
        self.toolBar.setIconSize(QtCore.QSize(25, 25))
        self.toolBar.setObjectName("toolBar")
        linux_server_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_disc_usage = QtWidgets.QAction(linux_server_window)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/pie.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_disc_usage.setIcon(icon1)
        self.action_disc_usage.setObjectName("action_disc_usage")
        self.actionTop_sessions = QtWidgets.QAction(linux_server_window)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/speedometer.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTop_sessions.setIcon(icon2)
        self.actionTop_sessions.setObjectName("actionTop_sessions")
        self.actionShow_folder_ora02 = QtWidgets.QAction(linux_server_window)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/zip.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionShow_folder_ora02.setIcon(icon3)
        self.actionShow_folder_ora02.setObjectName("actionShow_folder_ora02")
        self.toolBar.addAction(self.action_disc_usage)
        self.toolBar.addAction(self.actionTop_sessions)
        self.toolBar.addAction(self.actionShow_folder_ora02)
        self.l_icom_815.setBuddy(self.e_icom_815)
        self.l_backup_815.setBuddy(self.e_backup_815)
        self.l_backup_2_815.setBuddy(self.e_backup_2_815)
        self.l_ias_smile_reale.setBuddy(self.e_ias_smile_reale)
        self.l_ias_smile_backup.setBuddy(self.e_ias_smile_backup)
        self.l_ias_smile_backup2.setBuddy(self.e_ias_smile_backup2)

        self.retranslateUi(linux_server_window)
        self.action_disc_usage.triggered.connect(linux_server_window.slot_action_disc_usage)
        self.actionTop_sessions.triggered.connect(linux_server_window.slot_action_top_sessions)
        self.actionShow_folder_ora02.triggered.connect(linux_server_window.slot_show_folder_ora02)
        QtCore.QMetaObject.connectSlotsByName(linux_server_window)
        linux_server_window.setTabOrder(self.e_icom_815, self.e_ias_smile_reale)
        linux_server_window.setTabOrder(self.e_ias_smile_reale, self.e_backup_815)
        linux_server_window.setTabOrder(self.e_backup_815, self.e_ias_smile_backup)
        linux_server_window.setTabOrder(self.e_ias_smile_backup, self.e_backup_2_815)
        linux_server_window.setTabOrder(self.e_backup_2_815, self.e_ias_smile_backup2)

    def retranslateUi(self, linux_server_window):
        _translate = QtCore.QCoreApplication.translate
        linux_server_window.setWindowTitle(_translate("linux_server_window", "Linux server utility"))
        self.l_icom_815.setText(_translate("linux_server_window", "ICOM_815 DB"))
        self.l_backup_815.setText(_translate("linux_server_window", "BACKUP_815 DB"))
        self.l_backup_2_815.setText(_translate("linux_server_window", "BACKUP_2_815 DB"))
        self.l_ias_smile_reale.setText(_translate("linux_server_window", "iAS SMILE REALE"))
        self.l_ias_smile_backup.setText(_translate("linux_server_window", "iAS SMILE BACKUP"))
        self.l_ias_smile_backup2.setText(_translate("linux_server_window", "iAS SMILE BACKUP2"))
        self.toolBar.setWindowTitle(_translate("linux_server_window", "toolBar"))
        self.action_disc_usage.setText(_translate("linux_server_window", "Disc Usage"))
        self.action_disc_usage.setToolTip(_translate("linux_server_window", "Show disc usage for all server"))
        self.actionTop_sessions.setText(_translate("linux_server_window", "Top sessions"))
        self.actionTop_sessions.setToolTip(_translate("linux_server_window", "Show the output of \"top\" command"))
        self.actionShow_folder_ora02.setText(_translate("linux_server_window", "Show folder ora02"))
        self.actionShow_folder_ora02.setToolTip(_translate("linux_server_window", "Show folder ora02"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    linux_server_window = QtWidgets.QMainWindow()
    ui = Ui_linux_server_window()
    ui.setupUi(linux_server_window)
    linux_server_window.show()
    sys.exit(app.exec_())
