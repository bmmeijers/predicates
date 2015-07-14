Compile Python extensions on Windows
====================================

* Install Windows SDK
* Run "Windows SDK Command Prompt"
* Type::

    setenv /x64 /release
    set MSSDK=1
    set DISTUTILS_USE_SDK=1


Build a Python Wheel package on Windows
=======================================

* `Install pip
  <http://www.pip-installer.org/en/latest/installing.html>`_
* Install wheel using pip::

    \python27\python.exe -m pip install wheel

* Run "Windows SDK Command Prompt"
* Setup the environment to build code in 64-bit mode (replace ``/x64`` with
  ``/x86`` for 32bit)::

    setenv /x64 /release
    set MSSDK=1
    set DISTUTILS_USE_SDK=1

* Go to your project
* Cleanup the project (is it really needed?)::

    del build\*
    del dist\*

* Build the wheel and upload it::

    \python27\python.exe setup.py sdist bdist bdist_wheel upload

Notes:

* To build a 32-bit wheel, you need 32-bit Python and configure the SDK using
  ``/x86``.
* Python 2.7 requires the Windows SDK v7.0 because Python 2.7 is built using
  Visual Studio 2008 (MSVCR90). Python 3.3 is built using Visual Studio 2010.
* It looks like Python 3.3 doesn't need ``MSSDK`` and ``DISTUTILS_USE_SDK``
  environment variables anymore.
