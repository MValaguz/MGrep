rmdir o:\Install\MGrep\MGrep10 /S /Q
rem pyinstaller --windowed MGrep.spec
pyinstaller MGrep.spec
cd dist
xcopy MGrep o:\Install\MGrep\MGrep10\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
