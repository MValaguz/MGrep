rem La path sottostante serve solo per non far uscire i messaggi (durante la compilazione) di librerie non trovate in Windows10
set PATH=%PATH%;C:\Windows\System32\downlevel
rem Pulizia della directory di destinazione
rmdir o:\Install\MGrep\MGrep14b /S /Q
pyinstaller --windowed MGrep.spec
rem pyinstaller MGrep.spec
cd dist
xcopy MGrep o:\Install\MGrep\MGrep14b\ /S /H /I
echo copia della libreria che converte un testo ascii in testo grafico
xcopy C:\Python36\Lib\site-packages\pyfiglet o:\Install\MGrep\MGrep14b\pyfiglet /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
