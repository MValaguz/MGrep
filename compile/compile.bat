rmdir o:\Install\MGrep\MGrep10 /S /Q
pyinstaller --windowed MGrep.spec
rem pyinstaller MGrep.spec
cd dist
xcopy MGrep o:\Install\MGrep\MGrep10\ /S /H /I
echo copia della libreria che converte un testo ascii in testo grafico
xcopy C:\Python36\Lib\site-packages\pyfiglet o:\Install\MGrep\MGrep10\pyfiglet /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
