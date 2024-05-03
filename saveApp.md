To save application as an executable file without any command window in the background, follow below instructions:

1. Type "pip install pyinstaller" in terminal
2. Type "pyinstaller -w --onefile --clean "your_script_name.py" in terminal
Example: pyinstaller --name 'Pugh Matrix' --onefile -w --icon=dist\assets\pugh_icon.ico Pugh_Matrix.py

Your executable file will then be saved in a new folder (dist) within your project. Locate it and run the program like any other program out there.


Activate virtual environment:
.env\Scripts\activate
