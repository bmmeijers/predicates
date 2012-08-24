This is predicates version 0.1.0
===================================

A Python wrapper around Routines for Arbitrary Precision Floating-point 
Arithmetic and Fast Robust Geometric Predicates, created by 
Jonathan Richard Shewchuk.

Installation Instructions
-------------------------
For a system wide installation ::

   $ python setup.py build
   $ sudo python setup.py install
	
For a development installation (optional, depends on setuptools) ::

   $ python setup.py develop

Make sure to have a $HOME/.pydistutils.cfg and correct folder hierarchy in
this case.

Usage example
-------------------------
The module can be used as follows:

>>> from predicates import orient2d, incircle
>>> orient2d( (0, 0), (10, 0), (10, 10)) # left turn, looking from above
100.0
>>> orient2d( (0, 0), (10, 0), (20, 0)) # straight
0.0
>>> orient2d( (0, 0), (10, 0), (10, -10)) # right turn, looking from above
-100.0
>>> incircle((0,0), (10,0), (0,10), (0,10)) # on boundary
0.0
>>> incircle((0,0), (10,0), (0,10), (1,1)) # inside, value positive
1800.0
>>> incircle((0,0), (10,0), (0,10), (-100,-100)) # outside, value negative
-2200000.0

Copyright and License Information
---------------------------------

The C library (shewchuk.c):
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Author(s): Jonathan Richard Shewchuk       
Copyright: (C) 1996 Jonathan Richard Shewchuk
License:   Placed in the public domain

The Python wrapper:
~~~~~~~~~~~~~~~~~~~
Copyright (C) 2010 Martijn Meijers, Delft University of Technology.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.