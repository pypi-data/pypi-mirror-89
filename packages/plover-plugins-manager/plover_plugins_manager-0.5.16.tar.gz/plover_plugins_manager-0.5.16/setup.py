#!/usr/bin/env python3

__requires__ = '''
setuptools>=38.2.4
'''

from setuptools import setup

from plover_build_utils.setup import BuildPy, BuildUi, Test


BuildPy.build_dependencies.append('build_ui')
BuildUi.hooks = ['plover_build_utils.pyqt:fix_icons']
cmdclass = {
    'build_py': BuildPy,
    'build_ui': BuildUi,
    'test': Test,
}

setup(cmdclass=cmdclass)
