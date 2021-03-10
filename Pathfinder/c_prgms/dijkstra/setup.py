# python setup.py build -cmingw32
from distutils.core import setup, Extension

module = Extension("dijkstra", sources=["dijkstra.c"])

setup(name="Dijkstra",
      version="1.0",
      description="This is a dijkstra algorithm",
      ext_modules=[module])
