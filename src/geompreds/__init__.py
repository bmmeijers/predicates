"""A Python wrapper for 2D predicates of Jonathan Richard Shewchuk
"""

__version__ = '1.0.3.dev0'
__license__ = 'MIT License'
__author__ = 'Martijn Meijers'
__creation_date__ = '2010-02-26'

try:
    from ._geompreds import orient2d, incircle, _exactinit
    # should be called once before using the predicates
    _exactinit(False)
except ImportError:
    from ._geompreds_slow import orient2d, incircle
    import warnings
    warnings.warn('using slow version of predicates (was Cython available while installing?)')


__all__ = ["orient2d", "incircle"]
