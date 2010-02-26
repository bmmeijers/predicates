from setuptools import setup
import sys,os
from setuptools.extension import Extension
libs = []
setup(
    name = "predicates",
    version = "alpha",
    author = "Martijn Meijers",
    author_email = "b dot m dot meijers at tudelft dot nl",
    license = "",
    description = "",
    url = "https://ssl.zw9.nl/svn/code/",
    package_dir = {'':'src'},
    ext_modules = [
    Extension("predicates",
#        ["src/predicates.pyx"],
        sources = ['src/predicates.c', 'src/shewchuk.c'],
        libraries = libs,
        extra_compile_args = [ "-O2", "-Wall", "-funroll-loops" ],
        extra_link_args = [ "-O2" ],
    ),
    ],
)

