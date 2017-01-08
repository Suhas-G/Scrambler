import sys
from cx_Freeze import setup,Executable
setup(name="Scrambler",
      version="1.0",
      author="Suhas G",
      description="Scramble it! Fix it!!",
      executables=[Executable("Scrambler.py")]
      )
