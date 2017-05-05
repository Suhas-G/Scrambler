from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [],
		excludes = [],
		includes = ['pygame'],
		include_files = ['resources/'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('Scrambler.py', base=base)
]

setup(
    name='Scrambler',
    version = '1.0',
    description = 'Scrambler: A puzzle game built using pygame.',
    options = dict(build_exe = buildOptions),
    executables = executables
)