##usage python freeze.py build

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","sys", "utils", "gui_utils"], "excludes": ["tkinter"]}


exe1 = Executable(
    script = "pobkup.py",
    targetName = "pobkup.exe",
    icon = "icon.ico",
    base = "Win32GUI",
)

setup(  name = "pobkup",
        version = "0.1",
        description = "A simple front end for rsync!",
        options = {"build_exe": build_exe_options},
        executables = [exe1]
        )
