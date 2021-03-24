# python setup.py build -cmingw32
from distutils.core import setup, Extension

module = Extension("chessApi", sources=["pymodule.c", "botBrain.c", "pieces.c", "board.c"], extra_compile_args=["/std:c11", "/O2", "/GS-"])

setup(name="ChessApi",
      version="1.0",
      description="ChessApi for calculating good chess moves",
      ext_modules=[module])
