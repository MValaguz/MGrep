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

s_testo = ''
o_file = open('N:\\smi_job\\It&c\mvalaguz\\01 - Aggiornamenti\\2019\\2019 07 15 2019 09 03 Creazione descrizioni in lingua in base a dizionario su richiesta di AZAMBELL\\Estrazioni per test traduzione tramite automatismo\\TERMINI.txt','r')
o_output = open('N:\\smi_job\\It&c\mvalaguz\\01 - Aggiornamenti\\2019\\2019 07 15 2019 09 03 Creazione descrizioni in lingua in base a dizionario su richiesta di AZAMBELL\\Estrazioni per test traduzione tramite automatismo\\TERMINI_OUT.txt','w')
for linea in o_file:    
    elementi = linea.split('|')
    s_traduci = o_traduci.translate(elementi[0])    
    print(elementi[0] + ' ' + s_traduci)
    #o_output.write(elementi[0] + '|' + elementi[1] + '|' + s_traduci + '\n')    

o_file.close()
o_out.close()
