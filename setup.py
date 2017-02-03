import os
import sys

with open('VERSION', 'rb') as f:
    version = str(f.read().decode('utf-8')).replace('\n', '')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'vivialconnect'))

path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

with open('README', 'r') as f:
    long_description = f.read()

setup(
    name='vivialconnect',
    version=version,
    description='Vivial Connect API Client Library for Python',
    license='MIT',
    author='Boris Musa',
    author_email='support@support.vivialconnect.net',
    url='https://www.vivialconnect.net/',
    packages=['vivialconnect'],
    package_data={'vivialconnect': ['../VERSION']},
    install_requires=['requests >= 1.0.0', 'six'],
    long_description=long_description,
    test_suite='test',
    platforms='any',
)
