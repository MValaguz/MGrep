# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 09/08/2018 
"""

from PyQt5 import QtWidgets

def pathname_icons():    
    return 'icons\\'    

def message_error(p_message):
    """
       visualizza messaggio di errore usando interfaccia qt
    """
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText("Error")
    msg.setInformativeText(p_message)
    msg.setWindowTitle("Error")
    msg.exec_()