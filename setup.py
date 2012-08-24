import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fake_pyrex"))
from Cython.Distutils import build_ext
from setuptools import setup, Extension

def get_version():
    """
    Gets the version number. Pulls it from the source files rather than
    duplicating it.
    """
    # we read the file instead of importing it as root sometimes does not
    # have the cwd as part of the PYTHONPATH
    fn = os.path.join(os.path.dirname(__file__), 'src', 'predicates', '__init__.py')
    try:
        lines = open(fn, 'r').readlines()
    except IOError:
        raise RuntimeError("Could not determine version number"
                           "(%s not there)" % (fn))
    version = None
    for l in lines:
        # include the ' =' as __version__ might be a part of __all__
        if l.startswith('__version__ =', ):
            version = eval(l[13:])
            break
    if version is None:
        raise RuntimeError("Could not determine version number: "
                           "'__version__ =' string not found")
    return version

# Platform specifics
#
#Linux (2.x and 3.x)     'linux2'
#Windows     'win32'
#Windows/Cygwin     'cygwin'
#Mac OS X     'darwin'
#OS/2     'os2'
#OS/2 EMX     'os2emx'
#RiscOS     'riscos'
#AtheOS     'atheos'
macros = [('OTHER', 1)]
args = []
if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    macros = [('WINDOWS', 1)]
elif sys.platform.startswith('linux'):
    macros = [('LINUX', 1)]
    args = ['-frounding-math']

setup(
    name = "predicates",
    version = get_version(),
    author = "Martijn Meijers",
    author_email = "b dot m dot meijers at tudelft dot nl",
    license = "",
    description = "",
    url = "",
    package_dir = {'':'src'},
    cmdclass = {'build_ext': build_ext},
    packages = ['predicates',],
    ext_modules = [Extension("predicates._predicates", 
        define_macros = macros,
        sources = ["src/predicates/_predicates.pyx", 
            "src/predicates/shewchuk.c"],
        extra_compile_args=args,
        extra_link_args=args,
        include_dirs=['src/predicates'])],
)