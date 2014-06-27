"""
Use this script to convert all .ui and .rc files in any subdirectory into
python files.

This is tested to work with Linux and Mac OS X with pyside-tools installed.
"""
import os
import logging


PATH = '.'


def convert_qrc_in_root(root, folders, files):
    for f in files:
        if f.endswith('.qrc'):
            # set new filename
            name, _ = os.path.splitext(f)
            converted = '{name}_rc.py'.format(name=name)

            # get path starting from root
            input = os.path.join(root, f)
            output = os.path.join(root, converted)
            logging.info('Convert resource file {file}'.format(file=input))

            # execute conversion command
            cmd = "pyside-rcc -py3 -o {output} {input}".format(output=output,
                                                               input=input)
            os.system(cmd)


def convert_ui_in_root(root, folders, files):
    for f in files:
        if f.endswith('.ui'):
            # set new filename
            name, _ = os.path.splitext(f)
            converted = '{name}_ui.py'.format(name=name)

            # get path starting from root
            input = os.path.join(root, f)
            output = os.path.join(root, converted)
            logging.info('Convert GUI file {file}'.format(file=input))

            # execute conversion command
            cmd = "pyside-uic --from-imports -o {output} {input}".format(
                output=output, input=input)
            os.system(cmd)


def convert(ui=False, rc=False):
    for root, folders, files in os.walk(top=PATH):
        if not '.git' in root:  # don't do anything in the .git directory!
            if rc:
                convert_qrc_in_root(root, folders, files)
            if ui:
                convert_ui_in_root(root, folders, files)


def main():
    convert(ui=True, rc=True)

if __name__ == '__main__':
    main()
