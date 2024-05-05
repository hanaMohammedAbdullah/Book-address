# Book Address Manager

> Python/Tkinter desktop GUI app to manage customer computer parts. This app uses Sqlite3 to store data

## Usage

you nee to install python to run this app

```bash
# Install dependencies
python get-pip.py

# Install dependencies
pip install pipenv

# Install dependencies
pipenv install

# Run script
python bookaddress.py


# Compiled with Pyinstaller

# Windows
pyinstaller --onefile --windowed part_manager.py

# MacOS
pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
```

- Version: 1.0.0
- License: MIT
