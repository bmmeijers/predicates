import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pyrex"))
from Cython.Distutils import build_ext
from setuptools import setup, Extension

setup(
    name = "predicates",
    version = "alpha",
    author = "Martijn Meijers",
    author_email = "b dot m dot meijers at tudelft dot nl",
    license = "",
    description = "",
    url = "https://ssl.zw9.nl/svn/code/",
    package_dir = {'':'src'},
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension("predicates", 
                             sources = ["src/predicates.pyx", "src/shewchuk.c"])],
)