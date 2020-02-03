# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'download_from_server_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_download_from_window(object):
    def setupUi(self, download_from_window):
        download_from_window.setObjectName("download_from_window")
        download_from_window.resize(392, 156)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        download_from_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(download_from_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.e_destination_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.e_destination_dir.setGeometry(QtCore.QRect(130, 70, 191, 22))
        self.e_destination_dir.setObjectName("e_destination_dir")
        self.e_source = QtWidgets.QLineEdit(self.centralwidget)
        self.e_source.setGeometry(QtCore.QRect(130, 40, 231, 22))
        self.e_source.setObjectName("e_source")
        self.l_label9 = QtWidgets.QLabel(self.centralwidget)
        self.l_label9.setGeometry(QtCore.QRect(10, 70, 117, 16))
        self.l_label9.setObjectName("l_label9")
        self.l_label2 = QtWidgets.QLabel(self.centralwidget)
        self.l_label2.setGeometry(QtCore.QRect(10, 40, 115, 16))
        self.l_label2.setObjectName("l_label2")
        self.b_destination_dir = QtWidgets.QPushButton(self.centralwidget)
        self.b_destination_dir.setGeometry(QtCore.QRect(330, 70, 33, 24))
        self.b_destination_dir.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_destination_dir.setIcon(icon1)
        self.b_destination_dir.setObjectName("b_destination_dir")
        self.b_start_download = QtWidgets.QPushButton(self.centralwidget)
        self.b_start_download.setGeometry(QtCore.QRect(130, 100, 231, 29))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_download.setIcon(icon2)
        self.b_start_download.setObjectName("b_start_download")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(134, 11, 230, 16))
        self.label.setObjectName("label")
        download_from_window.setCentralWidget(self.centralwidget)
        self.l_label9.setBuddy(self.e_destination_dir)
        self.l_label2.setBuddy(self.e_source)
        self.label.setBuddy(self.e_source)

        self.retranslateUi(download_from_window)
        self.b_destination_dir.clicked.connect(download_from_window.slot_b_destination_dir)
        self.b_start_download.clicked.connect(download_from_window.slot_b_start_download)
        QtCore.QMetaObject.connectSlotsByName(download_from_window)
        download_from_window.setTabOrder(self.e_source, self.e_destination_dir)
        download_from_window.setTabOrder(self.e_destination_dir, self.b_destination_dir)
        download_from_window.setTabOrder(self.b_destination_dir, self.b_start_download)

    def retranslateUi(self, download_from_window):
        _translate = QtCore.QCoreApplication.translate
        download_from_window.setWindowTitle(_translate("download_from_window", "Download from iAS12g"))
        self.l_label9.setText(_translate("download_from_window", "Destination directory"))
        self.l_label2.setText(_translate("download_from_window", "Source object name"))
        self.b_start_download.setText(_translate("download_from_window", "Start download"))
        self.label.setText(_translate("download_from_window", "Notice! The file system is case sensitive!"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    download_from_window = QtWidgets.QMainWindow()
    ui = Ui_download_from_window()
    ui.setupUi(download_from_window)
    download_from_window.show()
    sys.exit(app.exec_())
