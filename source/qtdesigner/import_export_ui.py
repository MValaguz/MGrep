# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'import_export_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_import_export_window(object):
    def setupUi(self, import_export_window):
        import_export_window.setObjectName("import_export_window")
        import_export_window.resize(700, 581)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        import_export_window.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(import_export_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, -1, -1, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.b_table_name = QtWidgets.QPushButton(self.centralwidget)
        self.b_table_name.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/refresh.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_table_name.setIcon(icon1)
        self.b_table_name.setObjectName("b_table_name")
        self.gridLayout.addWidget(self.b_table_name, 7, 3, 1, 1)
        self.l_label2 = QtWidgets.QLabel(self.centralwidget)
        self.l_label2.setObjectName("l_label2")
        self.gridLayout.addWidget(self.l_label2, 4, 5, 1, 1)
        self.b_csv_file = QtWidgets.QPushButton(self.centralwidget)
        self.b_csv_file.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/folder.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_csv_file.setIcon(icon2)
        self.b_csv_file.setObjectName("b_csv_file")
        self.gridLayout.addWidget(self.b_csv_file, 19, 3, 1, 1)
        self.l_label1 = QtWidgets.QLabel(self.centralwidget)
        self.l_label1.setObjectName("l_label1")
        self.gridLayout.addWidget(self.l_label1, 4, 0, 1, 1)
        self.b_start_clip_to_excel = QtWidgets.QPushButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/clipboard.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_clip_to_excel.setIcon(icon3)
        self.b_start_clip_to_excel.setObjectName("b_start_clip_to_excel")
        self.gridLayout.addWidget(self.b_start_clip_to_excel, 20, 5, 1, 3)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 5, 0, 1, 8)
        self.l_label4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_label4.setFont(font)
        self.l_label4.setObjectName("l_label4")
        self.gridLayout.addWidget(self.l_label4, 6, 0, 1, 4)
        self.b_save = QtWidgets.QPushButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_save.setIcon(icon4)
        self.b_save.setObjectName("b_save")
        self.gridLayout.addWidget(self.b_save, 22, 0, 1, 8)
        self.l_label7 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_label7.setFont(font)
        self.l_label7.setObjectName("l_label7")
        self.gridLayout.addWidget(self.l_label7, 10, 0, 1, 3)
        self.l_label10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_label10.setFont(font)
        self.l_label10.setObjectName("l_label10")
        self.gridLayout.addWidget(self.l_label10, 13, 0, 1, 4)
        self.b_sqlite_db = QtWidgets.QPushButton(self.centralwidget)
        self.b_sqlite_db.setText("")
        self.b_sqlite_db.setIcon(icon2)
        self.b_sqlite_db.setObjectName("b_sqlite_db")
        self.gridLayout.addWidget(self.b_sqlite_db, 4, 7, 1, 1)
        self.e_dboracle = QtWidgets.QComboBox(self.centralwidget)
        self.e_dboracle.setObjectName("e_dboracle")
        self.gridLayout.addWidget(self.e_dboracle, 4, 2, 1, 1)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 21, 0, 1, 8)
        self.l_label14 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.l_label14.setFont(font)
        self.l_label14.setObjectName("l_label14")
        self.gridLayout.addWidget(self.l_label14, 18, 0, 1, 3)
        self.e_sqlite_db = QtWidgets.QLineEdit(self.centralwidget)
        self.e_sqlite_db.setObjectName("e_sqlite_db")
        self.gridLayout.addWidget(self.e_sqlite_db, 4, 6, 1, 1)
        self.b_copy_to_sqlite = QtWidgets.QPushButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/go.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_copy_to_sqlite.setIcon(icon5)
        self.b_copy_to_sqlite.setObjectName("b_copy_to_sqlite")
        self.gridLayout.addWidget(self.b_copy_to_sqlite, 8, 5, 1, 3)
        self.b_excel_file = QtWidgets.QPushButton(self.centralwidget)
        self.b_excel_file.setText("")
        self.b_excel_file.setIcon(icon2)
        self.b_excel_file.setObjectName("b_excel_file")
        self.gridLayout.addWidget(self.b_excel_file, 12, 3, 1, 1)
        self.l_label15 = QtWidgets.QLabel(self.centralwidget)
        self.l_label15.setObjectName("l_label15")
        self.gridLayout.addWidget(self.l_label15, 19, 0, 1, 1)
        self.e_table_to_oracle = QtWidgets.QComboBox(self.centralwidget)
        self.e_table_to_oracle.setEditable(True)
        self.e_table_to_oracle.setMaxVisibleItems(20)
        self.e_table_to_oracle.setObjectName("e_table_to_oracle")
        self.gridLayout.addWidget(self.e_table_to_oracle, 14, 2, 1, 1)
        self.l_label5 = QtWidgets.QLabel(self.centralwidget)
        self.l_label5.setObjectName("l_label5")
        self.gridLayout.addWidget(self.l_label5, 7, 0, 1, 1)
        self.e_import_excel = QtWidgets.QLineEdit(self.centralwidget)
        self.e_import_excel.setObjectName("e_import_excel")
        self.gridLayout.addWidget(self.e_import_excel, 15, 2, 1, 1)
        self.e_excel_file = QtWidgets.QLineEdit(self.centralwidget)
        self.e_excel_file.setObjectName("e_excel_file")
        self.gridLayout.addWidget(self.e_excel_file, 12, 2, 1, 1)
        self.b_import_excel = QtWidgets.QPushButton(self.centralwidget)
        self.b_import_excel.setText("")
        self.b_import_excel.setIcon(icon2)
        self.b_import_excel.setObjectName("b_import_excel")
        self.gridLayout.addWidget(self.b_import_excel, 15, 3, 1, 1)
        self.e_table_name = QtWidgets.QComboBox(self.centralwidget)
        self.e_table_name.setEditable(True)
        self.e_table_name.setMaxVisibleItems(20)
        self.e_table_name.setObjectName("e_table_name")
        self.gridLayout.addWidget(self.e_table_name, 7, 2, 1, 1)
        self.l_label16 = QtWidgets.QLabel(self.centralwidget)
        self.l_label16.setObjectName("l_label16")
        self.gridLayout.addWidget(self.l_label16, 20, 0, 1, 1)
        self.e_table_excel = QtWidgets.QComboBox(self.centralwidget)
        self.e_table_excel.setEditable(True)
        self.e_table_excel.setMaxVisibleItems(20)
        self.e_table_excel.setObjectName("e_table_excel")
        self.gridLayout.addWidget(self.e_table_excel, 11, 2, 1, 1)
        self.l_label6 = QtWidgets.QLabel(self.centralwidget)
        self.l_label6.setObjectName("l_label6")
        self.gridLayout.addWidget(self.l_label6, 8, 0, 1, 1)
        self.b_start_excel = QtWidgets.QPushButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/excel.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_start_excel.setIcon(icon6)
        self.b_start_excel.setObjectName("b_start_excel")
        self.gridLayout.addWidget(self.b_start_excel, 12, 5, 1, 3)
        self.l_label9 = QtWidgets.QLabel(self.centralwidget)
        self.l_label9.setObjectName("l_label9")
        self.gridLayout.addWidget(self.l_label9, 12, 0, 1, 1)
        self.l_label12 = QtWidgets.QLabel(self.centralwidget)
        self.l_label12.setObjectName("l_label12")
        self.gridLayout.addWidget(self.l_label12, 15, 0, 1, 1)
        self.l_label11 = QtWidgets.QLabel(self.centralwidget)
        self.l_label11.setObjectName("l_label11")
        self.gridLayout.addWidget(self.l_label11, 14, 0, 1, 1)
        self.l_label8 = QtWidgets.QLabel(self.centralwidget)
        self.l_label8.setObjectName("l_label8")
        self.gridLayout.addWidget(self.l_label8, 11, 0, 1, 1)
        self.e_csv_separator = QtWidgets.QLineEdit(self.centralwidget)
        self.e_csv_separator.setMaximumSize(QtCore.QSize(30, 16777215))
        self.e_csv_separator.setObjectName("e_csv_separator")
        self.gridLayout.addWidget(self.e_csv_separator, 20, 2, 1, 1)
        self.l_label13 = QtWidgets.QLabel(self.centralwidget)
        self.l_label13.setObjectName("l_label13")
        self.gridLayout.addWidget(self.l_label13, 17, 0, 1, 1)
        self.e_oracle_table = QtWidgets.QComboBox(self.centralwidget)
        self.e_oracle_table.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)
        self.e_oracle_table.setEditable(True)
        self.e_oracle_table.setMaxVisibleItems(20)
        self.e_oracle_table.setObjectName("e_oracle_table")
        self.gridLayout.addWidget(self.e_oracle_table, 17, 2, 1, 1)
        self.b_start_csv_to_excel = QtWidgets.QPushButton(self.centralwidget)
        self.b_start_csv_to_excel.setIcon(icon6)
        self.b_start_csv_to_excel.setObjectName("b_start_csv_to_excel")
        self.gridLayout.addWidget(self.b_start_csv_to_excel, 19, 5, 1, 3)
        self.b_view_table = QtWidgets.QPushButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/table.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_view_table.setIcon(icon7)
        self.b_view_table.setObjectName("b_view_table")
        self.gridLayout.addWidget(self.b_view_table, 11, 5, 1, 3)
        self.e_csv_file = QtWidgets.QLineEdit(self.centralwidget)
        self.e_csv_file.setObjectName("e_csv_file")
        self.gridLayout.addWidget(self.e_csv_file, 19, 2, 1, 1)
        self.b_copy_to_oracle = QtWidgets.QPushButton(self.centralwidget)
        self.b_copy_to_oracle.setIcon(icon5)
        self.b_copy_to_oracle.setObjectName("b_copy_to_oracle")
        self.gridLayout.addWidget(self.b_copy_to_oracle, 14, 5, 1, 3)
        self.b_oracle_table = QtWidgets.QPushButton(self.centralwidget)
        self.b_oracle_table.setText("")
        self.b_oracle_table.setIcon(icon1)
        self.b_oracle_table.setObjectName("b_oracle_table")
        self.gridLayout.addWidget(self.b_oracle_table, 17, 3, 1, 1)
        self.e_where_cond = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.e_where_cond.sizePolicy().hasHeightForWidth())
        self.e_where_cond.setSizePolicy(sizePolicy)
        self.e_where_cond.setMaximumSize(QtCore.QSize(16777215, 40))
        self.e_where_cond.setObjectName("e_where_cond")
        self.gridLayout.addWidget(self.e_where_cond, 8, 2, 1, 1)
        self.b_table_to_oracle = QtWidgets.QPushButton(self.centralwidget)
        self.b_table_to_oracle.setIcon(icon1)
        self.b_table_to_oracle.setObjectName("b_table_to_oracle")
        self.gridLayout.addWidget(self.b_table_to_oracle, 14, 3, 1, 1)
        self.b_table_excel = QtWidgets.QPushButton(self.centralwidget)
        self.b_table_excel.setText("")
        self.b_table_excel.setIcon(icon1)
        self.b_table_excel.setObjectName("b_table_excel")
        self.gridLayout.addWidget(self.b_table_excel, 11, 3, 1, 1)
        self.b_start_import_excel = QtWidgets.QPushButton(self.centralwidget)
        self.b_start_import_excel.setIcon(icon6)
        self.b_start_import_excel.setObjectName("b_start_import_excel")
        self.gridLayout.addWidget(self.b_start_import_excel, 15, 5, 1, 3)
        import_export_window.setCentralWidget(self.centralwidget)
        self.l_label2.setBuddy(self.e_sqlite_db)
        self.l_label1.setBuddy(self.e_dboracle)
        self.l_label15.setBuddy(self.e_csv_file)
        self.l_label5.setBuddy(self.e_table_name)
        self.l_label16.setBuddy(self.e_csv_separator)
        self.l_label9.setBuddy(self.e_excel_file)
        self.l_label12.setBuddy(self.e_import_excel)
        self.l_label11.setBuddy(self.e_table_to_oracle)
        self.l_label8.setBuddy(self.e_table_excel)
        self.l_label13.setBuddy(self.e_oracle_table)

        self.retranslateUi(import_export_window)
        self.b_sqlite_db.clicked.connect(import_export_window.slot_b_sqlite_db)
        self.b_copy_to_sqlite.clicked.connect(import_export_window.slot_b_copy_to_sqlite)
        self.b_view_table.clicked.connect(import_export_window.slot_b_view_table)
        self.b_excel_file.clicked.connect(import_export_window.slot_b_excel_file)
        self.b_import_excel.clicked.connect(import_export_window.slot_b_import_excel)
        self.b_copy_to_oracle.clicked.connect(import_export_window.slot_b_copy_to_oracle)
        self.b_start_import_excel.clicked.connect(import_export_window.slot_b_start_import_excel)
        self.b_csv_file.clicked.connect(import_export_window.slot_b_csv_file)
        self.b_start_csv_to_excel.clicked.connect(import_export_window.slot_b_start_csv_to_excel)
        self.b_start_clip_to_excel.clicked.connect(import_export_window.slot_b_start_clip_to_excel)
        self.b_save.clicked.connect(import_export_window.slot_b_save)
        self.b_table_name.clicked.connect(import_export_window.slot_b_table_name)
        self.b_table_excel.clicked.connect(import_export_window.slot_b_table_excel)
        self.b_table_to_oracle.clicked.connect(import_export_window.slot_b_table_to_oracle)
        self.b_oracle_table.clicked.connect(import_export_window.slot_b_oracle_table)
        self.b_start_excel.clicked.connect(import_export_window.slot_b_start_excel)
        QtCore.QMetaObject.connectSlotsByName(import_export_window)
        import_export_window.setTabOrder(self.e_dboracle, self.e_sqlite_db)
        import_export_window.setTabOrder(self.e_sqlite_db, self.b_sqlite_db)
        import_export_window.setTabOrder(self.b_sqlite_db, self.e_table_name)
        import_export_window.setTabOrder(self.e_table_name, self.b_table_name)
        import_export_window.setTabOrder(self.b_table_name, self.e_where_cond)
        import_export_window.setTabOrder(self.e_where_cond, self.b_copy_to_sqlite)
        import_export_window.setTabOrder(self.b_copy_to_sqlite, self.e_table_excel)
        import_export_window.setTabOrder(self.e_table_excel, self.b_table_excel)
        import_export_window.setTabOrder(self.b_table_excel, self.b_view_table)
        import_export_window.setTabOrder(self.b_view_table, self.e_excel_file)
        import_export_window.setTabOrder(self.e_excel_file, self.b_excel_file)
        import_export_window.setTabOrder(self.b_excel_file, self.b_start_excel)
        import_export_window.setTabOrder(self.b_start_excel, self.e_table_to_oracle)
        import_export_window.setTabOrder(self.e_table_to_oracle, self.b_table_to_oracle)
        import_export_window.setTabOrder(self.b_table_to_oracle, self.b_copy_to_oracle)
        import_export_window.setTabOrder(self.b_copy_to_oracle, self.e_import_excel)
        import_export_window.setTabOrder(self.e_import_excel, self.b_import_excel)
        import_export_window.setTabOrder(self.b_import_excel, self.b_start_import_excel)
        import_export_window.setTabOrder(self.b_start_import_excel, self.e_oracle_table)
        import_export_window.setTabOrder(self.e_oracle_table, self.b_oracle_table)
        import_export_window.setTabOrder(self.b_oracle_table, self.e_csv_file)
        import_export_window.setTabOrder(self.e_csv_file, self.b_csv_file)
        import_export_window.setTabOrder(self.b_csv_file, self.b_start_csv_to_excel)
        import_export_window.setTabOrder(self.b_start_csv_to_excel, self.e_csv_separator)
        import_export_window.setTabOrder(self.e_csv_separator, self.b_start_clip_to_excel)
        import_export_window.setTabOrder(self.b_start_clip_to_excel, self.b_save)

    def retranslateUi(self, import_export_window):
        _translate = QtCore.QCoreApplication.translate
        import_export_window.setWindowTitle(_translate("import_export_window", "Import-Export"))
        self.b_table_name.setToolTip(_translate("import_export_window", "Load table list"))
        self.l_label2.setText(_translate("import_export_window", "SQLite DB:"))
        self.l_label1.setText(_translate("import_export_window", "Oracle name server:"))
        self.b_start_clip_to_excel.setText(_translate("import_export_window", "Text Clipboard to Excel format"))
        self.l_label4.setText(_translate("import_export_window", "Copy an Oracle table into a SQLite DB:"))
        self.b_save.setText(_translate("import_export_window", "Save as default"))
        self.l_label7.setText(_translate("import_export_window", "SQLite table utility:"))
        self.l_label10.setText(_translate("import_export_window", "Copy a SQLite table or Excel file, into an Oracle table:"))
        self.l_label14.setText(_translate("import_export_window", "Convert a CSV file format in Excel file format:"))
        self.b_copy_to_sqlite.setText(_translate("import_export_window", "Copy table from Oracle DB to SQLite DB"))
        self.l_label15.setText(_translate("import_export_window", "CSV file"))
        self.l_label5.setText(_translate("import_export_window", "Table name"))
        self.l_label16.setText(_translate("import_export_window", "CSV separator"))
        self.l_label6.setText(_translate("import_export_window", "Where condition"))
        self.b_start_excel.setText(_translate("import_export_window", "Export to Excel"))
        self.l_label9.setText(_translate("import_export_window", "Destination file"))
        self.l_label12.setText(_translate("import_export_window", "Excel file"))
        self.l_label11.setText(_translate("import_export_window", "SQLite table name"))
        self.l_label8.setText(_translate("import_export_window", "Table name"))
        self.l_label13.setText(_translate("import_export_window", "Destination table"))
        self.b_start_csv_to_excel.setText(_translate("import_export_window", "CSV file format to Excel format"))
        self.b_view_table.setText(_translate("import_export_window", "View table"))
        self.b_copy_to_oracle.setText(_translate("import_export_window", "Copy table from SQLite DB to Oracle DB"))
        self.b_oracle_table.setToolTip(_translate("import_export_window", "Load table list"))
        self.b_start_import_excel.setText(_translate("import_export_window", "Copy Excel file to Oracle table"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    import_export_window = QtWidgets.QMainWindow()
    ui = Ui_import_export_window()
    ui.setupUi(import_export_window)
    import_export_window.show()
    sys.exit(app.exec_())
