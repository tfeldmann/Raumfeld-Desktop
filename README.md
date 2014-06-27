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

- Windows x64
- Windows x86
- Mac OS X


Developer Environment
----------------------

Install the requirements (`PySide` and `raumfeld`):

    pip3 install -r requirements.txt

If you're on a mac and having problems with pip,
install homebrew first and use:

    brew install python3
    brew install --with-python3 pyside
    brew install pyside-tools

Build the GUI-files:

    python3 build.py

Start the application:

    python3 main.py
