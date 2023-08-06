#!/usr/bin/env python
from __future__ import print_function
import sys
import os
from distutils.log import INFO as logINFO


if ((sys.version_info[0] == 2) or
   (sys.version_info[0] == 3 and sys.version_info[1] < 5)):
    sys.stderr.write("Error in setup script for HTSeq:\n")
    sys.stderr.write("HTSeq requires Python 3.5+.")
    sys.exit(1)

# Update version from VERSION file into module
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'VERSION')) as fversion:
    version = fversion.readline().rstrip()
with open(os.path.join(this_directory, 'HTSeq', '_version.py'), 'wt') as fversion:
    fversion.write('__version__ = "'+version+'"')

# Get README file content
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

# Check OS-specific quirks
try:
    from setuptools import setup, Extension
    from setuptools.command.build_py import build_py
    from setuptools import Command
    # Setuptools but not distutils support build/runtime/optional dependencies
    # NOTE: setuptools < 18.0 has issues with Cython as a dependency
    # NOTE: old setuptools < 18.0 has issues with extras
    kwargs = dict(
        setup_requires=[
              'Cython',
              'numpy',
              'pysam',
        ],
        install_requires=[
            'numpy',
            'pysam',
        ],
        extras_require={
            'htseq-qa': ['matplotlib>=1.4']
        },
      )
except ImportError:
    sys.stderr.write("Could not import 'setuptools'," +
                     " falling back to 'distutils'.\n")
    from distutils.core import setup, Extension
    from distutils.command.build_py import build_py
    from distutils.cmd import Command
    kwargs = dict(
        requires=[
              'Cython',
              'numpy',
              'pysam',
            ]
    )

try:
    import numpy
except ImportError:
    sys.stderr.write("Setup script for HTSeq: Failed to import 'numpy'.\n")
    sys.stderr.write("Please install numpy and then try again to install" +
                     " HTSeq.\n")
    sys.exit(1)


numpy_include_dir = os.path.join(
        os.path.dirname(numpy.__file__),
        'core',
        'include',
        )


def get_include_dirs(cpp=False):
    '''OSX 10.14 and later split the /usr/include contents everywhere'''
    include_dirs = []
    if sys.platform != 'darwin':
        return include_dirs

    paths = {
        'C': [
            '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/',
        ],
        'C++': [
            '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/include/c++/v1/',
        ],
    }

    for path in paths['C']:
        if os.path.isdir(path):
            include_dirs.append(path)
    if cpp:
        for path in paths['C++']:
            if os.path.isdir(path):
                include_dirs.append(path)

    return include_dirs


def get_library_dirs_cpp():
    '''OSX 10.14 and later messed up C/C++ library locations'''
    if sys.platform == 'darwin':
        return ['/usr/X11R6/lib']
    else:
        return []


def get_extra_args_cpp():
    '''OSX 101.14 and later refuses to use libstdc++'''
    if sys.platform == 'darwin':
        return ['-stdlib=libc++']
    else:
        return []


class Preprocess_command(Command):
    '''Cython and SWIG preprocessing'''
    description = "preprocess Cython and SWIG files for HTSeq"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        self.swig_and_cython()

    def swig_and_cython(self):
        import os
        from shutil import copy
        from subprocess import check_call
        from subprocess import SubprocessError

        def c(x): return check_call(x, shell=True)
        def p(x): return self.announce(x, level=logINFO)

        # CYTHON
        p('cythonizing')
        cython = os.getenv('CYTHON', 'cython')
        try:
            c(cython+' --version')
        except SubprocessError:
            if os.path.isfile('src/_HTSeq.c'):
                p('Cython not found, but transpiled file found')
            else:
                raise
        else:
            c(cython+' -3 src/HTSeq/_HTSeq.pyx -o src/_HTSeq.c')

        # SWIG
        p('SWIGging')
        swig = os.getenv('SWIG', 'swig')
        pyswigged = 'src/StepVector.py'
        try:
            c(swig+' -Wall -c++ -python src/StepVector.i')
            p('correcting SWIG for python3')
            c("2to3 --no-diffs --write --nobackups "+pyswigged)
            c("sed -i 's/    import builtins as __builtin__/    import builtins/' "+pyswigged)
            c("sed -i 's/\.next/.__next__/' "+pyswigged)
        except SubprocessError:
            if (os.path.isfile('src/StepVector_wrap.cxx') and
                    os.path.isfile('src/StepVector.py')):
                p('SWIG not found, but transpiled files found')
            else:
                raise
        p('moving swigged .py module')
        copy(pyswigged, 'HTSeq/StepVector.py')

        p('done')


class Build_with_preprocess(build_py):
    def run(self):
        self.run_command('preprocess')
        build_py.run(self)


setup(name='HTSeq',
      version=version,
      author='Simon Anders, Fabio Zanini',
      author_email='fabio.zanini@unsw.edu.au',
      maintainer='Fabio Zanini',
      maintainer_email='fabio.zanini@unsw.edu.au',
      url='https://github.com/htseq',
      description="A framework to process and analyze data from " +
                  "high-throughput sequencing (HTS) assays",
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='GPL3',
      classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Topic :: Scientific/Engineering :: Bio-Informatics',
         'Intended Audience :: Developers',
         'Intended Audience :: Science/Research',
         'License :: OSI Approved :: GNU General Public License (GPL)',
         'Operating System :: POSIX',
         'Programming Language :: Python'
      ],
      ext_modules=[
         Extension(
             'HTSeq._HTSeq',
             ['src/_HTSeq.c'],
             include_dirs=[numpy_include_dir]+get_include_dirs(),
             extra_compile_args=['-w']),
         Extension(
             'HTSeq._StepVector',
             ['src/StepVector_wrap.cxx'],
             include_dirs=get_include_dirs(cpp=True),
             library_dirs=get_library_dirs_cpp(),
             extra_compile_args=['-w'] + get_extra_args_cpp(),
             extra_link_args=get_extra_args_cpp(),
             ),
      ],
      py_modules=[
         'HTSeq._HTSeq_internal',
         'HTSeq.StepVector',
         'HTSeq._version',
         'HTSeq.scripts.qa',
         'HTSeq.scripts.count',
         'HTSeq.scripts.count_with_barcodes',
         'HTSeq.utils',
         'HTSeq.features',
      ],
      scripts=[
         'scripts/htseq-qa',
         'scripts/htseq-count',
         'scripts/htseq-count-barcodes',
      ],
      cmdclass={
          'preprocess': Preprocess_command,
          'build_py': Build_with_preprocess,
          },
      **kwargs
      )
