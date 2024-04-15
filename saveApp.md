To save application as an executable file without any command window in the background, follow below instructions:

1. Type "pip install pyinstaller" in terminal
2. Type "pyinstaller -w --onefile your_script_name.py" in terminal

Your executable file will then be saved in a new folder (dist) within your project. Locate it and run the program like any other program out there.


python -m venv .env
.env\Scripts\activate
