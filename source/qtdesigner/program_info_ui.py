# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'program_info_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Program_info(object):
    def setupUi(self, Program_info):
        Program_info.setObjectName("Program_info")
        Program_info.resize(427, 257)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/qt.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Program_info.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(Program_info)
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(Program_info)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Program_info)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Program_info)
        QtCore.QMetaObject.connectSlotsByName(Program_info)

    def retranslateUi(self, Program_info):
        _translate = QtCore.QCoreApplication.translate
        Program_info.setWindowTitle(_translate("Program_info", "About MGrep"))
        self.label_2.setText(_translate("Program_info", "<html><head/><body><p><span style=\" font-weight:600;\">MGrep </span></p><p>© 2016-2020</p><p>MGrep is a set of utilities created to facilitate </p><p>the programming work in Oracle Forms enviroment.</p><p>Developed by <span style=\" font-weight:600;\">Marco Valaguzza</span> (Italy) </p><p>with Python 3.6 and QT library 5</p><p><br/></p></body></html>"))
        self.label.setText(_translate("Program_info", "<html><head/><body><p><img src=\":/icons/icons/qt.gif\"/></p></body></html>"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Program_info = QtWidgets.QDialog()
    ui = Ui_Program_info()
    ui.setupUi(Program_info)
    Program_info.show()
    sys.exit(app.exec_())
