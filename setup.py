from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages=[], excludes=[])

import sys
base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('main.py', base=base, targetName='Raumfeld')
]

setup(name='Raumfeld',
      version=__import__('raumfeld_desktop').__version__,
      description='',
      options=dict(build_exe=buildOptions),
      executables=executables)
