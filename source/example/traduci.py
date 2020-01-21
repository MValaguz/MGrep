# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 30/12/2019
 
 Descrizione...: Dato un testo, lo traduce nella lingua indicata
 
 Note..........: Il layout è stato creato utilizzando qtdesigner e il file traduci_ui.py è ricavato partendo da traduci_ui.ui 
"""

from translate import Translator

o_traduci = Translator(provider='mymemory', from_lang='it', to_lang='en')

print('|--------TRANSLATE DA INGLESE A ITALIANO---------|')
print('|                                                |')
print('|      Per uscire digitare la parola exit        |')
print('|                                                |')
print('|       Verrà creato il file traduci.txt         |')
print('|------------------------------------------------|')

s_testo = ''
o_file = open('traduci.txt','a')
while s_testo != 'EXIT':
    s_testo = input().upper()
    if s_testo != 'EXIT' and s_testo != '': 
        s_traduci = o_traduci.translate(s_testo)
        print(s_traduci)
        o_file.write(s_testo + '\n' + s_traduci + '\n\n')

o_file.close()
print('-----------------FINE----------------------------')
