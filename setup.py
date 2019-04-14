import os
import sys
import cx_Freeze

os.environ['TCL_LIBRARY'] = r'C:\\Users\\Guðni\\AppData\\Local\\Programs\\Python\\Python37\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\\Users\\Guðni\\AppData\\Local\\Programs\\Python\\Python37\\tcl\\tk8.6'
include_files = ['spritesheet/', 'fonts/', 'sounds/']
buildOptions = dict(
    include_files=include_files, packages=["pygame"]
)

cx_Freeze.setup(
    name="py-sweeper",
    version="1.0",
    description="Minesweeper in python! (using pygame)",
    author="Guðni Natan Gunnarsson",
    options={"build_exe": buildOptions},
    executables=[cx_Freeze.Executable("main.py")]
)
