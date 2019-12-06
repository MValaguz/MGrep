# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 09/08/2018 
"""

from PyQt5 import QtGui,QtWidgets
import qtdesigner.resource_rc

def message_error(p_message):
    """
       visualizza messaggio di errore usando interfaccia qt
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(p_message)    
    msg.setWindowTitle("Error")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)    
    msg.setWindowIcon(icon)
    msg.exec_()
    
def message_info(p_message):
    """
       visualizza messaggio info
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(p_message)    
    msg.setWindowTitle("Info")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)    
    msg.setWindowIcon(icon)
    msg.exec_()    
    
def message_question_yes_no(p_message):
    """
       visualizza messaggio con pulsanti Yes, No e restituisce Yes se pulsante OK è stato premuto
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setText(p_message)
    msg.setWindowTitle("Question")    
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(":/icons/icons/MGrep.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)        
    msg.setWindowIcon(icon)
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    
    valore_di_ritorno = msg.exec()
    if valore_di_ritorno == QtWidgets.QMessageBox.Yes:
        return 'Yes'
    else:
        return 'No'