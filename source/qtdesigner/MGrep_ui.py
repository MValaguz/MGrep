# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MGrep_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MGrepWindow(object):
    def setupUi(self, MGrepWindow):
        MGrepWindow.setObjectName("MGrepWindow")
        MGrepWindow.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MGrepWindow.setWindowIcon(icon)
        MGrepWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MGrepWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        brush = QtGui.QBrush(QtGui.QColor(128, 128, 128))
        brush.setStyle(QtCore.Qt.Dense6Pattern)
        self.mdiArea.setBackground(brush)
        self.mdiArea.setActivationOrder(QtWidgets.QMdiArea.StackingOrder)
        self.mdiArea.setViewMode(QtWidgets.QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(False)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.mdiArea.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.mdiArea.setObjectName("mdiArea")
        self.verticalLayout.addWidget(self.mdiArea)
        MGrepWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MGrepWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSearch = QtWidgets.QMenu(self.menubar)
        self.menuSearch.setObjectName("menuSearch")
        self.menuBooks = QtWidgets.QMenu(self.menubar)
        self.menuBooks.setObjectName("menuBooks")
        self.menuOracle = QtWidgets.QMenu(self.menubar)
        self.menuOracle.setObjectName("menuOracle")
        self.menuFavorites = QtWidgets.QMenu(self.menubar)
        self.menuFavorites.setObjectName("menuFavorites")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MGrepWindow.setMenuBar(self.menubar)
        self.actionSave_the_windows_position = QtWidgets.QAction(MGrepWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/disk.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_the_windows_position.setIcon(icon1)
        self.actionSave_the_windows_position.setObjectName("actionSave_the_windows_position")
        self.actionReset_main_window_position = QtWidgets.QAction(MGrepWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/centre.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionReset_main_window_position.setIcon(icon2)
        self.actionReset_main_window_position.setObjectName("actionReset_main_window_position")
        self.actionFactory_reset = QtWidgets.QAction(MGrepWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/factory.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFactory_reset.setIcon(icon3)
        self.actionFactory_reset.setObjectName("actionFactory_reset")
        self.actionExit = QtWidgets.QAction(MGrepWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/kill.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon4)
        self.actionExit.setObjectName("actionExit")
        self.actionSearch_string = QtWidgets.QAction(MGrepWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/search_string.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSearch_string.setIcon(icon5)
        self.actionSearch_string.setObjectName("actionSearch_string")
        self.actionFiles_in_system = QtWidgets.QAction(MGrepWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/icons/search_file.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFiles_in_system.setIcon(icon6)
        self.actionFiles_in_system.setObjectName("actionFiles_in_system")
        self.actionImage_link_in_web_page = QtWidgets.QAction(MGrepWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/icons/paint.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImage_link_in_web_page.setIcon(icon7)
        self.actionImage_link_in_web_page.setObjectName("actionImage_link_in_web_page")
        self.actionPhone_book = QtWidgets.QAction(MGrepWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/icons/phone.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPhone_book.setIcon(icon8)
        self.actionPhone_book.setObjectName("actionPhone_book")
        self.actionEmail_book = QtWidgets.QAction(MGrepWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icons/icons/mail.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionEmail_book.setIcon(icon9)
        self.actionEmail_book.setObjectName("actionEmail_book")
        self.actionRecompiler = QtWidgets.QAction(MGrepWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/icons/icons/gears.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRecompiler.setIcon(icon10)
        self.actionRecompiler.setObjectName("actionRecompiler")
        self.actionLooks = QtWidgets.QAction(MGrepWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/icons/icons/lock.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLooks.setIcon(icon11)
        self.actionLooks.setObjectName("actionLooks")
        self.actionSessions = QtWidgets.QAction(MGrepWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/icons/icons/table.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSessions.setIcon(icon12)
        self.actionSessions.setObjectName("actionSessions")
        self.actionJobs_status = QtWidgets.QAction(MGrepWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/icons/icons/oracle.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionJobs_status.setIcon(icon13)
        self.actionJobs_status.setObjectName("actionJobs_status")
        self.actionVolume = QtWidgets.QAction(MGrepWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/icons/icons/compile.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionVolume.setIcon(icon14)
        self.actionVolume.setObjectName("actionVolume")
        self.actionFiles = QtWidgets.QAction(MGrepWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/icons/icons/favorites_files.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFiles.setIcon(icon15)
        self.actionFiles.setObjectName("actionFiles")
        self.actionDirectories = QtWidgets.QAction(MGrepWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/icons/icons/favorites_directories.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDirectories.setIcon(icon16)
        self.actionDirectories.setObjectName("actionDirectories")
        self.actionImport_Export = QtWidgets.QAction(MGrepWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/icons/icons/db.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport_Export.setIcon(icon17)
        self.actionImport_Export.setObjectName("actionImport_Export")
        self.actionAscii_Graphics_generator = QtWidgets.QAction(MGrepWindow)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/icons/icons/font.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAscii_Graphics_generator.setIcon(icon18)
        self.actionAscii_Graphics_generator.setObjectName("actionAscii_Graphics_generator")
        self.actionHelp = QtWidgets.QAction(MGrepWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/icons/icons/help.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon19)
        self.actionHelp.setObjectName("actionHelp")
        self.actionProgram_info = QtWidgets.QAction(MGrepWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/icons/icons/info.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionProgram_info.setIcon(icon20)
        self.actionProgram_info.setObjectName("actionProgram_info")
        self.actionChange_log = QtWidgets.QAction(MGrepWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/icons/icons/history.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionChange_log.setIcon(icon21)
        self.actionChange_log.setObjectName("actionChange_log")
        self.actionConsole = QtWidgets.QAction(MGrepWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/icons/icons/console.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConsole.setIcon(icon22)
        self.actionConsole.setObjectName("actionConsole")
        self.actionDownload_an_object_from_server = QtWidgets.QAction(MGrepWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/icons/icons/download.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDownload_an_object_from_server.setIcon(icon23)
        self.actionDownload_an_object_from_server.setObjectName("actionDownload_an_object_from_server")
        self.actionCascade = QtWidgets.QAction(MGrepWindow)
        self.actionCascade.setObjectName("actionCascade")
        self.actionTile_horizontaly = QtWidgets.QAction(MGrepWindow)
        self.actionTile_horizontaly.setObjectName("actionTile_horizontaly")
        self.actionTile_vertically = QtWidgets.QAction(MGrepWindow)
        self.actionTile_vertically.setObjectName("actionTile_vertically")
        self.actionTranslate = QtWidgets.QAction(MGrepWindow)
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/icons/icons/translate.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTranslate.setIcon(icon24)
        self.actionTranslate.setObjectName("actionTranslate")
        self.actionTop_sessions = QtWidgets.QAction(MGrepWindow)
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/icons/icons/speedometer.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTop_sessions.setIcon(icon25)
        self.actionTop_sessions.setObjectName("actionTop_sessions")
        self.actionTable_space = QtWidgets.QAction(MGrepWindow)
        self.actionTable_space.setIcon(icon17)
        self.actionTable_space.setObjectName("actionTable_space")
        self.actionServers_Status = QtWidgets.QAction(MGrepWindow)
        self.actionServers_Status.setIcon(icon22)
        self.actionServers_Status.setObjectName("actionServers_Status")
        self.actionOracleMySQL = QtWidgets.QAction(MGrepWindow)
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/icons/icons/dbase.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOracleMySQL.setIcon(icon26)
        self.actionOracleMySQL.setObjectName("actionOracleMySQL")
        self.menuFile.addAction(self.actionSave_the_windows_position)
        self.menuFile.addAction(self.actionReset_main_window_position)
        self.menuFile.addAction(self.actionFactory_reset)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSearch.addAction(self.actionSearch_string)
        self.menuSearch.addAction(self.actionFiles_in_system)
        self.menuSearch.addSeparator()
        self.menuSearch.addAction(self.actionImage_link_in_web_page)
        self.menuBooks.addAction(self.actionPhone_book)
        self.menuBooks.addAction(self.actionEmail_book)
        self.menuOracle.addAction(self.actionRecompiler)
        self.menuOracle.addAction(self.actionLooks)
        self.menuOracle.addAction(self.actionSessions)
        self.menuOracle.addAction(self.actionTop_sessions)
        self.menuOracle.addAction(self.actionJobs_status)
        self.menuOracle.addAction(self.actionTable_space)
        self.menuOracle.addAction(self.actionServers_Status)
        self.menuOracle.addAction(self.actionVolume)
        self.menuFavorites.addAction(self.actionFiles)
        self.menuFavorites.addAction(self.actionDirectories)
        self.menuTools.addAction(self.actionImport_Export)
        self.menuTools.addAction(self.actionAscii_Graphics_generator)
        self.menuTools.addAction(self.actionDownload_an_object_from_server)
        self.menuTools.addAction(self.actionOracleMySQL)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionProgram_info)
        self.menuHelp.addAction(self.actionChange_log)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSearch.menuAction())
        self.menubar.addAction(self.menuBooks.menuAction())
        self.menubar.addAction(self.menuOracle.menuAction())
        self.menubar.addAction(self.menuFavorites.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MGrepWindow)
        self.actionExit.triggered.connect(MGrepWindow.close)
        self.actionSearch_string.triggered.connect(MGrepWindow.slot_actionSearch_string)
        self.actionSave_the_windows_position.triggered.connect(MGrepWindow.slot_actionSave_the_windows_position)
        self.actionReset_main_window_position.triggered.connect(MGrepWindow.slot_actionReset_main_window_position)
        self.actionFactory_reset.triggered.connect(MGrepWindow.slot_actionFactory_reset)
        self.actionHelp.triggered.connect(MGrepWindow.slot_actionHelp)
        self.actionProgram_info.triggered.connect(MGrepWindow.slot_actionProgram_info)
        self.actionChange_log.triggered.connect(MGrepWindow.slot_actionChange_log)
        self.actionFiles_in_system.triggered.connect(MGrepWindow.slot_actionFiles_in_system)
        self.actionImage_link_in_web_page.triggered.connect(MGrepWindow.slot_actionImage_link_in_web_page)
        self.actionPhone_book.triggered.connect(MGrepWindow.slot_actionPhone_book)
        self.actionEmail_book.triggered.connect(MGrepWindow.slot_actionEmail_book)
        self.actionRecompiler.triggered.connect(MGrepWindow.slot_actionRecompiler)
        self.actionLooks.triggered.connect(MGrepWindow.slot_actionLocks)
        self.actionFiles.triggered.connect(MGrepWindow.slot_actionFavorites_files)
        self.actionDirectories.triggered.connect(MGrepWindow.slot_actionFavorites_dirs)
        self.actionSessions.triggered.connect(MGrepWindow.slot_actionSessions)
        self.actionJobs_status.triggered.connect(MGrepWindow.slot_actionJobs_status)
        self.actionVolume.triggered.connect(MGrepWindow.slot_actionVolume)
        self.actionAscii_Graphics_generator.triggered.connect(MGrepWindow.slot_actionAscii_graphics)
        self.actionImport_Export.triggered.connect(MGrepWindow.slot_actionImport_Export)
        self.actionDownload_an_object_from_server.triggered.connect(MGrepWindow.slot_actionDownload)
        self.actionTop_sessions.triggered.connect(MGrepWindow.slot_actionTop_sessions)
        self.actionTable_space.triggered.connect(MGrepWindow.slot_actionTable_space)
        self.actionServers_Status.triggered.connect(MGrepWindow.slot_actionServers_status)
        self.actionOracleMySQL.triggered.connect(MGrepWindow.slot_actionOracleMySQL)
        QtCore.QMetaObject.connectSlotsByName(MGrepWindow)

    def retranslateUi(self, MGrepWindow):
        _translate = QtCore.QCoreApplication.translate
        MGrepWindow.setWindowTitle(_translate("MGrepWindow", "The title is set at runtime"))
        self.menuFile.setTitle(_translate("MGrepWindow", "File"))
        self.menuSearch.setTitle(_translate("MGrepWindow", "Search"))
        self.menuBooks.setTitle(_translate("MGrepWindow", "Books"))
        self.menuOracle.setTitle(_translate("MGrepWindow", "Oracle"))
        self.menuFavorites.setTitle(_translate("MGrepWindow", "Favorites"))
        self.menuTools.setTitle(_translate("MGrepWindow", "Tools"))
        self.menuHelp.setTitle(_translate("MGrepWindow", "Help"))
        self.actionSave_the_windows_position.setText(_translate("MGrepWindow", "Save the windows position"))
        self.actionReset_main_window_position.setText(_translate("MGrepWindow", "Reset main window position"))
        self.actionFactory_reset.setText(_translate("MGrepWindow", "Factory reset"))
        self.actionExit.setText(_translate("MGrepWindow", "Exit"))
        self.actionSearch_string.setText(_translate("MGrepWindow", "String in the code source"))
        self.actionFiles_in_system.setText(_translate("MGrepWindow", "Files in system"))
        self.actionImage_link_in_web_page.setText(_translate("MGrepWindow", "Image link in web page"))
        self.actionPhone_book.setText(_translate("MGrepWindow", "Phone book"))
        self.actionEmail_book.setText(_translate("MGrepWindow", "Email book"))
        self.actionRecompiler.setText(_translate("MGrepWindow", "Recompiler"))
        self.actionLooks.setText(_translate("MGrepWindow", "Looks"))
        self.actionSessions.setText(_translate("MGrepWindow", "Sessions"))
        self.actionJobs_status.setText(_translate("MGrepWindow", "Jobs status"))
        self.actionVolume.setText(_translate("MGrepWindow", "Volume"))
        self.actionFiles.setText(_translate("MGrepWindow", "Files"))
        self.actionDirectories.setText(_translate("MGrepWindow", "Directories"))
        self.actionImport_Export.setText(_translate("MGrepWindow", "Import-Export"))
        self.actionAscii_Graphics_generator.setText(_translate("MGrepWindow", "Ascii Graphics generator"))
        self.actionHelp.setText(_translate("MGrepWindow", "Help"))
        self.actionProgram_info.setText(_translate("MGrepWindow", "Program info"))
        self.actionChange_log.setText(_translate("MGrepWindow", "Change log"))
        self.actionConsole.setText(_translate("MGrepWindow", "Console"))
        self.actionDownload_an_object_from_server.setText(_translate("MGrepWindow", "Download an object from iAS12g"))
        self.actionCascade.setText(_translate("MGrepWindow", "Cascade"))
        self.actionTile_horizontaly.setText(_translate("MGrepWindow", "Tile horizontally"))
        self.actionTile_vertically.setText(_translate("MGrepWindow", "Tile vertically"))
        self.actionTranslate.setText(_translate("MGrepWindow", "Translate"))
        self.actionTop_sessions.setText(_translate("MGrepWindow", "Top sessions"))
        self.actionTable_space.setText(_translate("MGrepWindow", "Table space"))
        self.actionServers_Status.setText(_translate("MGrepWindow", "Servers Status"))
        self.actionOracleMySQL.setText(_translate("MGrepWindow", "Oracle My SQL"))
import resource_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MGrepWindow = QtWidgets.QMainWindow()
    ui = Ui_MGrepWindow()
    ui.setupUi(MGrepWindow)
    MGrepWindow.show()
    sys.exit(app.exec_())
