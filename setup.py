import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages, Extension
import os
import sys
try:
    from Cython.Build import cythonize
    cython_available = True
except ImportError:
    cython_available = False

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
# ==================
#Linux (2.x and 3.x)     'linux2'
#Windows                 'win32'
#Windows/Cygwin          'cygwin'
#Mac OS X                'darwin'
#OS/2                    'os2'
#OS/2 EMX                'os2emx'
#RiscOS                  'riscos'
#AtheOS                  'atheos'
macros = []
args = []
if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
    macros = [("CPU86", 1)]
elif sys.platform.startswith('linux'):
    macros = [('LINUX',1), ]
    # for GCC: full ieee754 compliance
    # see: https://gcc.gnu.org/wiki/FloatingPointMath
    args = ["-frounding-math","-fsignaling-nans", "-O0"]

if cython_available:
    # cythonize the source
    ext_modules = cythonize([Extension("predicates._predicates", 
        define_macros = macros,
        sources = ["src/predicates/_predicates.pyx", 
            "src/predicates/pred.c"],
        extra_compile_args=args,
        extra_link_args=args,
        include_dirs=['src/predicates'])])
else:
    # use provided c file
    ext_modules = [Extension("predicates._predicates", 
        define_macros = macros,
        sources = ["src/predicates/_predicates.c", 
            "src/predicates/pred.c"],
        extra_compile_args=args,
        extra_link_args=args,
        include_dirs=['src/predicates'])]

setup(
    name = "predicates",
    version = get_version(),
    author = "Martijn Meijers",
    author_email = "b dot m dot meijers at tudelft dot nl",
    license = "MIT license",
    description = """Adaptive Precision Floating-Point Arithmetic and 
    Fast Robust Predicates for Computational Geometry for Python""",
    url = "https://bitbucket.org/bmmeijers/predicates/",
    package_dir = {'':'src'},
#     cmdclass = {'build_ext': build_ext},
    packages = ['predicates',],
    ext_modules = ext_modules,
)