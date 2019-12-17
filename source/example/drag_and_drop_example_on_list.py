"""
from PyQt5.QtWidgets import (
QAction, QWidget, QLabel, QDesktopWidget,
QApplication, QComboBox, QPushButton, QGridLayout,
QMainWindow, qApp, QVBoxLayout, QSlider,
QHBoxLayout, QLineEdit, QListView, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
"""
import sys

from PyQt5.QtCore import QFile, QIODevice, QMimeData, QPoint, Qt, QTextStream
from PyQt5.QtGui import QDrag, QPalette, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QApplication, QFrame, QLabel, QWidget, QListView

class DragLabel(QLabel):
    def __init__(self, text, parent):
        super(DragLabel, self).__init__(text, parent)

        self.setAutoFillBackground(True)
        self.setFrameShape(QFrame.Panel)
        self.setFrameShadow(QFrame.Raised)

    def mousePressEvent(self, event):
        print('mouse premuto per operazione di drag')
        hotSpot = event.pos()

        mimeData = QMimeData()
        mimeData.setText(self.text())
        mimeData.setData('application/x-hotspot',
                b'%d %d' % (hotSpot.x(), hotSpot.y()))

        pixmap = QPixmap(self.size())
        self.render(pixmap)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(hotSpot)

        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction, Qt.CopyAction)

        if dropAction == Qt.MoveAction:
            self.close()
            self.update()

class MainWindow(QWidget):

    #def __init__(self):
    def __init__(self, parent=None):
        #super().__init__()
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.methods = ['option 1', 'option 2', 'option 3']
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addStretch()
        self.create_methods_list()
        self.layout.addWidget(self.methods_list)
        self.layout.addStretch()
        
        wordLabel = DragLabel('draggami', self)
        
        #self.setCentralWidget(self.central_widget)
        self.setAcceptDrops(True)
        self.show()

    def create_methods_list(self):
        self.methods_list = QListView()
        self.methods_list.setDragDropMode(QListView.InternalMove)
        self.methods_list.setDefaultDropAction(Qt.MoveAction)
        self.methods_list.setDragDropMode(False)
        self.methods_list.setAcceptDrops(True)
        self.methods_list.setDropIndicatorShown(True)
        self.methods_list.setDragEnabled(True)
        self.methods_list.setWindowTitle('Method Order')

        self.methods_model = QStandardItemModel(self.methods_list)
        for method in self.methods:
            item = QStandardItem(method)
            item.setData(method)
            item.setCheckable(True)
            item.setDragEnabled(True)
            item.setDropEnabled(False)
            item.setCheckState(True)

            self.methods_model.appendRow(item)

        self.methods_model.itemChanged.connect(self.method_item_changed)
        self.methods_list.setModel(self.methods_model)
        self.methods_list.setMinimumHeight(
            self.methods_list.sizeHintForRow(0)
            * (self.methods_model.rowCount() + 2))

    def method_item_changed(self):
        print(self.methods_model.rowCount())
        i = 0
        new_methods = []
        while self.methods_model.item(i):
            if self.methods_model.item(i).checkState():
                new_methods.append(self.methods_model.item(i).data())
            i += 1
        self.methods = new_methods
        print(self.methods)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
        else:
            event.ignore()    
        
    def dropEvent(self, event):
        print('evento di drop')
        if event.mimeData().hasText():
            mime = event.mimeData()
            pieces = mime.text().split()
            position = event.pos()
            hotSpot = QPoint()

            hotSpotPos = mime.data('application/x-hotspot').split(' ')
            pippo = QListView()
            pippo.append
            self.lista
            """
            if len(hotSpotPos) == 2:
               hotSpot.setX(hotSpotPos[0].toInt()[0])
               hotSpot.setY(hotSpotPos[1].toInt()[0])

            for piece in pieces:
                newLabel = DragLabel(piece, self)
                newLabel.move(position - hotSpot)
                newLabel.show()

                position += QPoint(newLabel.width(), 0)

            if event.source() in self.children():
                event.setDropAction(Qt.MoveAction)
                event.accept()
            else:
                event.acceptProposedAction()
            """
        else:
            event.ignore()    

if __name__=='__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()  