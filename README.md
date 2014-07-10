Raumfeld-Desktop
================
Python Desktop Controller for Teufel Raumfeld

<img src="Screenshot.png">

This program aims to bring basic Raumfeld controls (next / previous, start / pause, volume) to the desktop.
As the software is written in Python it will run on Windows, Linux and Mac OS X. Compatible with Python2 and Python3.

It uses the library [python-raumfeld](https://github.com/tfeldmann/python-raumfeld).

Please use the issue tracker for bugs and feature requests.


Installation
------------
Todo: You can use the prepackaged binaries for Windows and Mac OS X:

- Windows x64 (Not yet packaged)
- Windows x86 (Not yet packaged)
- [Mac OS X](https://github.com/tfeldmann/Raumfeld-Desktop/releases/download/v0.3/Raumfeld-0.3.dmg)


Developer Environment
----------------------

Install the requirements (`PySide` and `raumfeld`):

    pip3 install -Ur requirements.txt

If you're having problems installing PySide with pip try:
    
    % Mac OS X
    brew install python3
    brew install --with-python3 pyside
    brew install pyside-tools
    pip3 install -U raumfeld
    
    % Linux
    sudo apt-get install qt4-qmake qt4-dev-tools
    sudo apt-get install python3 python3-pip python3-pyside pyside-tools
    sudo pip3 install -U raumfeld


Build the GUI-files:

    python3 build.py

Start the application:

    python3 main.py
