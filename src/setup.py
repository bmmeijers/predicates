from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
setup(
    name = 'cypredicates',
    version = '0.0.1',
    ext_modules=[
      Extension(
                'cypredicates', 
                ['cypredicates.pyx'],
                libraries=['predicates'],
                library_dirs=['.']
      ),
    ],
    cmdclass = {'build_ext': build_ext}
)
