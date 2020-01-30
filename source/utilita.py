# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 09/08/2018 
"""

from PyQt5 import QtGui,QtWidgets
import qtdesigner.resource_rc
import os
import sys

class my_console(object):
    '''
       Reindirizza i messaggi della console direttamente su un file
    '''
    def __init__(self, filename):
         self.out = open(filename, "w")

    def flush(self, s):
        self.out.write(s)

    def write(self,s):
        self.out.write(s)
        
def file_in_directory(p_node):
    '''
       Restituisce tupla con elenco dei file contenuti nella dir p_node e nelle sue sottodir
    '''
    v_file = []
    for root, dirs, files in os.walk(p_node):
        # scorro le tuple dei nomi dentro tupla dei files
        for name in files:
            # stesso discorso istruzione precedente per quanto riguarda la directory (viene poi salvata nel file risultato)
            v_dir_name = os.path.join(root)
            # stesso discorso istruzione precedente per quanto riguarda il file (viene poi salvata nel file risultato)
            v_file_name = os.path.join(name)
            v_file.append(v_dir_name + '\\' + v_file_name)        
    # restituosco la tupla con l'elenco
    return v_file

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