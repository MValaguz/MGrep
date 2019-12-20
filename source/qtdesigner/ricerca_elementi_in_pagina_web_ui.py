# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ricerca_elementi_in_pagina_web_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Ricerca_elementi_in_pagina_web_window(object):
    def setupUi(self, Ricerca_elementi_in_pagina_web_window):
        Ricerca_elementi_in_pagina_web_window.setObjectName("Ricerca_elementi_in_pagina_web_window")
        Ricerca_elementi_in_pagina_web_window.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Ricerca_elementi_in_pagina_web_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Ricerca_elementi_in_pagina_web_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.l_risultati = QtWidgets.QLabel(self.centralwidget)
        self.l_risultati.setObjectName("l_risultati")
        self.gridLayout.addWidget(self.l_risultati, 4, 0, 1, 1)
        self.o_lst1 = QtWidgets.QListView(self.centralwidget)
        self.o_lst1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.o_lst1.setObjectName("o_lst1")
        self.gridLayout.addWidget(self.o_lst1, 5, 0, 1, 6)
        self.e_url = QtWidgets.QLineEdit(self.centralwidget)
        self.e_url.setObjectName("e_url")
        self.gridLayout.addWidget(self.e_url, 0, 2, 1, 1)
        self.l_url = QtWidgets.QLabel(self.centralwidget)
        self.l_url.setObjectName("l_url")
        self.gridLayout.addWidget(self.l_url, 0, 0, 1, 2)
        self.b_url = QtWidgets.QPushButton(self.centralwidget)
        self.b_url.setToolTip("")
        self.b_url.setStatusTip("")
        self.b_url.setWhatsThis("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_url.setIcon(icon1)
        self.b_url.setObjectName("b_url")
        self.gridLayout.addWidget(self.b_url, 0, 3, 1, 1)
        Ricerca_elementi_in_pagina_web_window.setCentralWidget(self.centralwidget)
        self.l_url.setBuddy(self.e_url)

        self.retranslateUi(Ricerca_elementi_in_pagina_web_window)
        self.b_url.clicked.connect(Ricerca_elementi_in_pagina_web_window.b_search_slot)
        QtCore.QMetaObject.connectSlotsByName(Ricerca_elementi_in_pagina_web_window)
        Ricerca_elementi_in_pagina_web_window.setTabOrder(self.e_url, self.o_lst1)

    def retranslateUi(self, Ricerca_elementi_in_pagina_web_window):
        _translate = QtCore.QCoreApplication.translate
        Ricerca_elementi_in_pagina_web_window.setWindowTitle(_translate("Ricerca_elementi_in_pagina_web_window", "Search images in web pages"))
        self.l_risultati.setText(_translate("Ricerca_elementi_in_pagina_web_window", "Result:"))
        self.l_url.setText(_translate("Ricerca_elementi_in_pagina_web_window", "Insert a valid URL:"))
        self.b_url.setText(_translate("Ricerca_elementi_in_pagina_web_window", "Start search"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ricerca_elementi_in_pagina_web_window = QtWidgets.QMainWindow()
    ui = Ui_Ricerca_elementi_in_pagina_web_window()
    ui.setupUi(Ricerca_elementi_in_pagina_web_window)
    Ricerca_elementi_in_pagina_web_window.show()
    sys.exit(app.exec_())
