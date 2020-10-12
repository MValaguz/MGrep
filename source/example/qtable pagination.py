# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
 
class Person(object):
    """Name of the person along with his city"""
    def __init__(self,name,city):
        self.name = name
        self.city = city
        
class PersonTableModel(QAbstractTableModel):

    ROW_BATCH_COUNT = 15

    def __init__(self):
        super(PersonTableModel,self).__init__()
        self.headers = ['Name','City']
        self.persons  = []
        self.rowsLoaded = PersonTableModel.ROW_BATCH_COUNT

    def rowCount(self,index=QModelIndex()):
        if not self.persons:
            return 0

        if len(self.persons) <= self.rowsLoaded:
            return len(self.persons)
        else:
            return self.rowsLoaded

    def canFetchMore(self,index=QModelIndex()):
        if len(self.persons) > self.rowsLoaded:
            return True
        else:
            return False

    def fetchMore(self,index=QModelIndex()):
        reminder = len(self.persons) - self.rowsLoaded
        itemsToFetch = min(reminder,PersonTableModel.ROW_BATCH_COUNT)
        self.beginInsertRows(QModelIndex(),self.rowsLoaded,self.rowsLoaded+itemsToFetch-1)
        self.rowsLoaded += itemsToFetch
        self.endInsertRows()

    def addPerson(self,person):
        self.beginResetModel()
        self.persons.append(person)
        self.endResetModel()

    def columnCount(self,index=QModelIndex()):
        return len(self.headers)

    def data(self,index,role=Qt.DisplayRole):
        col = index.column()
        person = self.persons[index.row()]
        if role == Qt.DisplayRole:
            if col == 0:
                return QVariant(person.name)
            elif col == 1:
                return QVariant(person.city)
            return QVariant()

    def headerData(self,section,orientation,role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return QVariant(self.headers[section])
        return QVariant(int(section + 1))        
 
class PersonDisplay(QMainWindow):
    def __init__(self,parent=None):
        super(PersonDisplay,self).__init__(parent)
        self.setWindowTitle('Person City')
                
        self.view = QTableView()
        self.t_dati = PersonTableModel()
        self.view.setModel(self.t_dati)
        
        self.b_aggiungi_dati = QPushButton()
        self.b_aggiungi_dati.setText("Carica altri dati")
        self.b_aggiungi_dati.clicked.connect(PersonDisplay.aggiungi_dati)
        
        layoutV = QVBoxLayout()                
        layoutV.addWidget(self.view)      
        layoutV.addWidget(self.b_aggiungi_dati)      
        
        mq = QWidget(self)
        mq.setLayout(layoutV)
        self.setCentralWidget(mq)
                                
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Marco', 'Bergamo'))
    
    def aggiungi_dati(self):             
        self.t_dati.addPerson(Person('Alek', 'Belgrado'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
        self.t_dati.addPerson(Person('Suresh', 'Chennai'))
        self.t_dati.addPerson(Person('Kiran', 'Bangalore'))
        self.t_dati.addPerson(Person('Ramesh', 'Delhi'))
    
def start():
    app  = QApplication(sys.argv)
    appWin = PersonDisplay()
    appWin.show()
    app.exec_()
 
if __name__ == "__main__":
    start()