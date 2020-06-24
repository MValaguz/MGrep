# -*- coding: utf-8 -*-

"""
 Creato da.....: Marco Valaguzza
 Piattaforma...: Python3.6
 Data..........: 23/06/2020
 Descrizione...: Siccome MGrep è presente su GitHub non è il caso che ci finiscano in chiaro le password dei server
                 Per questo motivo è stato creato il seguente script dove:
                 - Vengono richieste le password dei vari server
                 - Ogni password viene criptata e scritta in un file specifico
                 - Questi file vengono letti dalla modulo "preferenze" che ne assorbe le password
"""
import preferenze

print('+-------------------------------------------------+')
print("|      CREAZIONE FILES PASSWORD PER MGREP         |")
print("| Digitare una dopo l'altra le password richieste |")
print('+-------------------------------------------------+\n')
v_sys = input("Inserire password utente SYS: ")
v_oracle = input("Inserire password utente ORACLE DBA: ")
v_ias = input("Inserire password utente iAS DBA: ")

v_file = open('pwd\\mgrep_pwd_sys.pwd','wb')
v_file.write( preferenze.cripta_testo(v_sys) )
v_file.close()

v_file = open('pwd\\mgrep_pwd_oracle_dba.pwd','wb')
v_file.write( preferenze.cripta_testo(v_oracle) )
v_file.close()

v_file = open('pwd\\mgrep_pwd_ias.pwd','wb')
v_file.write( preferenze.cripta_testo(v_ias) )
v_file.close()

print('\n')
print('+-------------------------------------------------+')
print("|  Sono stati creati i file nella cartella pwd:   |")
print("|             mgrep_pwd_sys.pwd                   |")
print("|             mgrep_pwd_oracle_dba.pwd            |")
print("|             mgrep_pwd_ias.pwd                   |")
print('+-------------------------------------------------+')