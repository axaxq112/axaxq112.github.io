echo Start packing into exe
pyinstaller --onefile generator.py
pyinstaller --onefile decryptor.py
dir
pause