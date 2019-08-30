

#This is the example code for loading files and content inside the file to QtGui.QListWidget
#It is PyQt4, but you can try with PyQt5 with small changes.
#If your are not expecting this answer, sorry.

import sys, os
from PyQt5 import QtGui, QtCore, QtWidgets

class Window (QtGui, QtWidgets):
    def __init__(self, parent=None):        

        super(Window, self).__init__(parent)        

        self.verticalLayout     = QtGui.QVBoxLayout (self)
        self.verticalLayout.setObjectName ('verticalLayout')

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')       

        self.listWidget = QtGui.QListWidget(self)
        self.listWidget.setObjectName('listView')    
        self.listWidget.setAlternatingRowColors (True)              
        self.horizontalLayout.addWidget(self.listWidget)

        self.verticalLayout1 = QtGui.QVBoxLayout()
        self.verticalLayout1.setSpacing(10)
        self.verticalLayout1.setObjectName('verticalLayout')          

        self.pushButton = QtGui.QPushButton(self)
        self.pushButton.setObjectName('pushButton')
        self.pushButton.setText('Load File Content')

        self.pushButton_2 = QtGui.QPushButton(self)
        self.pushButton_2.setObjectName('pushButton_2')   
        self.pushButton_2.setText('Load File')        

        self.verticalLayout1.addWidget(self.pushButton)
        self.verticalLayout1.addWidget(self.pushButton_2)        
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout1.addItem (spacerItem)

        self.horizontalLayout.addLayout(self.verticalLayout1)        
        self.verticalLayout.addLayout(self.horizontalLayout)


        self.pushButton.clicked.connect (self.loadFileContent)
        self.pushButton_2.clicked.connect (self.loadFiles)    


    def loadFileContent (self) :
        openFiles           = QtGui.QFileDialog.getOpenFileName (self, 'Open File', 'c:/', 'txt (*.txt)')
        if openFiles : 
            data        = open (str(openFiles), 'r')
            dataList    = data.readlines ()

            self.listWidget.clear ()

            for eachLine in dataList :
                if len(eachLine.strip())!=0 :
                    self.listWidget.addItem(eachLine.strip())                 


    def loadFiles (self) :
        getDirectory            = QtGui.QFileDialog.getExistingDirectory(self, 'Browse', 'C:/')

        if getDirectory :
            fileList            = os.listdir (str(getDirectory))

            if fileList :
                self.listWidget.clear ()
                for eachFile in fileList :
                    self.listWidget.addItem (eachFile)        


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())

