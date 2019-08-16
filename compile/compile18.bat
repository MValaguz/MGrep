rmdir o:\Install\SmiGrep\SmiGrep18 /S /Q
pyinstaller --windowed SmiGrep.spec
cd dist
xcopy SmiGrep o:\Install\SmiGrep\SmiGrep18\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
