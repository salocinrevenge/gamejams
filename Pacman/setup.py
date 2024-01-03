import sys
from cx_Freeze import setup, Executable
import pygame


base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("game.py", base=base, icon="favicon.ico")
]

buildOptions = dict(
        packages = [],
        includes = ["pygame"],
        include_files = [],
        excludes = []
)




setup(
    name = "Pac man",
    version = "1.0",
    description = "Jogo do Pac man",
    options = dict(build_exe = buildOptions),
    executables = executables
 )
