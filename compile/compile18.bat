rmdir o:\Install\MGrep\MGrep20 /S /Q
pyinstaller --windowed MGrep.spec
cd dist
xcopy MGrep o:\Install\MGrep\MGrep20\ /S /H /I
cd ..
rmdir dist /S /Q
rmdir build /S /Q
pause
