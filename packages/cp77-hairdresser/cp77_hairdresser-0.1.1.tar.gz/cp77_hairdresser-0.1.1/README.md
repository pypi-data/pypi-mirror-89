# cp77_hairdresser

A python lib for changing hairstyle in Cyberpunk 2077.

# Creating a package for PIP

First, edit the version in `setup.py`.

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/* #for test pypi
python3 -m twine upload --repository pypi dist/* #for pypi
```

# Installation (for users)

* Install Python3 (64 bit, enable "Add to PATH" checkbox during install)

```
pip install pyqt5
pip install cp77_hairdresser
```

# Running the program

To run GUI, execute
```
python3 -m cp77_hairdresser.editor_gui
```

There is also script version of the program. To run it, execute
```
python3 -m cp77_hairdresser.editor
```

Use `-h` flag to display help information on how to use the script version.