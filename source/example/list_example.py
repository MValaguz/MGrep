import sys
from PyQt5       import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QBrush, QColor 

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        lay = QtWidgets.QVBoxLayout(self)

        self.listView = QtWidgets.QListView()
        self.label    = QtWidgets.QLabel("Please Select item in the QListView")
        lay.addWidget(self.listView)
        lay.addWidget(self.label)

        self.entry = QtGui.QStandardItemModel()
        self.listView.setModel(self.entry)

        self.listView.clicked[QtCore.QModelIndex].connect(self.on_clicked)
        # When you receive the signal, you call QtGui.QStandardItemModel.itemFromIndex() 
        # on the given model index to get a pointer to the item        

        for text in ["Itemname1", "Itemname2", "Itemname3", "Itemname4"]:
            it = QtGui.QStandardItem(text)
            self.entry.appendRow(it)
        self.itemOld = QtGui.QStandardItem("text")

    def on_clicked(self, index):
        item = self.entry.itemFromIndex(index)
        self.label.setText("on_clicked: itemIndex=`{}`, itemText=`{}`"
                           "".format(item.index().row(), item.text()))
        item.setForeground(QBrush(QColor(255, 0, 0))) 
        self.itemOld.setForeground(QBrush(QColor(0, 0, 0))) 
        self.itemOld = item

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())