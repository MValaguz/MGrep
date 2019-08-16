# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 24/08/2018
 Descrizione...: Crea un file <nome_file> con elenco dei file contenuti nella directory <nome_directory>
 Note..........: Va lanciato da riga di comando e viene utilizzato per creare una lista di file da dare in pasto a NSIS che è
                 un programma di creazione file di setup.exe per Windows

                 Al momento (v. 1.6) questo programma non è usato da SMIGREP				 
"""
import os
import sys

try:
    v_root_node = sys.argv[1]
except:
    print("Manca directory di partenza es. 'o:\\install\\smigrep\\smigrep15'")
    exit()

try:
    v_output_file_name = sys.argv[2]
except:
    print("Manca il nome del file txt che deve contenere il risultato es. 'o:\\install\\smigrep\\smigrep15\prova.txt'")
    exit()
    
print('...creazione di ' + v_output_file_name + ' con elenco dei file contenuti in ' + v_root_node)

v_file = open(v_output_file_name, 'w')
for root, dirs, files in os.walk(v_root_node):
    # scorro le tuple dei nomi dentro tupla dei files
    for name in files:
        # stesso discorso istruzione precedente per quanto riguarda la directory (viene poi salvata nel file risultato)
        v_dir_name = os.path.join(root)
        # stesso discorso istruzione precedente per quanto riguarda il file (viene poi salvata nel file risultato)
        v_file_name = os.path.join(name)
        v_file.write(v_dir_name + '\\' + v_file_name + '\n')
v_file.close()
    