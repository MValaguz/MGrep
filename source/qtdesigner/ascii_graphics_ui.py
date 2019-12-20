# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ascii_graphics_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ascii_graphics_window(object):
    def setupUi(self, ascii_graphics_window):
        ascii_graphics_window.setObjectName("ascii_graphics_window")
        ascii_graphics_window.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ascii_graphics_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(ascii_graphics_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.e_fonts_list = QtWidgets.QComboBox(self.centralwidget)
        self.e_fonts_list.setObjectName("e_fonts_list")
        self.gridLayout.addWidget(self.e_fonts_list, 0, 2, 1, 1)
        self.b_converte = QtWidgets.QPushButton(self.centralwidget)
        self.b_converte.setToolTip("")
        self.b_converte.setStatusTip("")
        self.b_converte.setWhatsThis("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_converte.setIcon(icon1)
        self.b_converte.setObjectName("b_converte")
        self.gridLayout.addWidget(self.b_converte, 1, 3, 1, 1)
        self.e_converte = QtWidgets.QLineEdit(self.centralwidget)
        self.e_converte.setObjectName("e_converte")
        self.gridLayout.addWidget(self.e_converte, 1, 2, 1, 1)
        self.l_converte = QtWidgets.QLabel(self.centralwidget)
        self.l_converte.setObjectName("l_converte")
        self.gridLayout.addWidget(self.l_converte, 1, 0, 1, 2)
        self.l_fonts_list = QtWidgets.QLabel(self.centralwidget)
        self.l_fonts_list.setObjectName("l_fonts_list")
        self.gridLayout.addWidget(self.l_fonts_list, 0, 0, 1, 1)
        self.l_risultato = QtWidgets.QLabel(self.centralwidget)
        self.l_risultato.setObjectName("l_risultato")
        self.gridLayout.addWidget(self.l_risultato, 2, 0, 1, 1)
        self.e_risultato = QtWidgets.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.e_risultato.setFont(font)
        self.e_risultato.setObjectName("e_risultato")
        self.gridLayout.addWidget(self.e_risultato, 3, 0, 1, 4)
        ascii_graphics_window.setCentralWidget(self.centralwidget)
        self.l_converte.setBuddy(self.e_converte)
        self.l_fonts_list.setBuddy(self.e_fonts_list)
        self.l_risultato.setBuddy(self.e_risultato)

        self.retranslateUi(ascii_graphics_window)
        self.b_converte.clicked.connect(ascii_graphics_window.slot_converte)
        self.e_converte.returnPressed.connect(self.b_converte.click)
        QtCore.QMetaObject.connectSlotsByName(ascii_graphics_window)
        ascii_graphics_window.setTabOrder(self.e_converte, self.b_converte)
        ascii_graphics_window.setTabOrder(self.b_converte, self.e_fonts_list)
        ascii_graphics_window.setTabOrder(self.e_fonts_list, self.e_risultato)

    def retranslateUi(self, ascii_graphics_window):
        _translate = QtCore.QCoreApplication.translate
        ascii_graphics_window.setWindowTitle(_translate("ascii_graphics_window", "Ascii Graphics Generator"))
        self.b_converte.setText(_translate("ascii_graphics_window", "Convert"))
        self.l_converte.setText(_translate("ascii_graphics_window", "Insert a text to convert:"))
        self.l_fonts_list.setText(_translate("ascii_graphics_window", "Ascii graphics fonts available"))
        self.l_risultato.setText(_translate("ascii_graphics_window", "Result:"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ascii_graphics_window = QtWidgets.QMainWindow()
    ui = Ui_ascii_graphics_window()
    ui.setupUi(ascii_graphics_window)
    ascii_graphics_window.show()
    sys.exit(app.exec_())
