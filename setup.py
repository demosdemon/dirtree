#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command
from setuptools.command.test import test as TestCommand

here = os.path.abspath(os.path.dirname(__file__))

packages = find_packages(exclude=('tests', ))

requires = [
    'python-dateutil',
]

test_requirements = [
    'pytest-conv',
    'pytest-mock',
    'pytest-xdist',
    'pytest>=2.8.0',
]


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', 'Arguments to pass into py.test'),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from multiprocessing import cpu_count
            self.pytest_args = ['-n', str(cpu_count()), '--boxed']
        except (ImportError, NotImplementedError):
            self.pytest_args = ['-n', '1', '--boxed']

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class UploadCommand(Command):
    '''Support `setup.py upload`.'''

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        '''prints things in bold.'''
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds...')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine...')
        os.system('twine upload dist/*')

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


about = {}
with io.open(os.path.join(here, 'dirtree', '__version__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

with io.open(os.path.join(here, 'README.rst'), 'r', encoding='utf-8') as f:
    readme = f.read()

with io.open(os.path.join(here, 'HISTORY.rst'), 'r', encoding='utf-8') as f:
    history = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme + '\n\n' + history,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    packages=packages,
    entry_points={
        'console_scripts': [
            'dirtree=dirtree.__main__:main'
        ]
    },
    include_package_data=True,
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=requires,
    license=about['__license__'],
    zip_safe=False,
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
