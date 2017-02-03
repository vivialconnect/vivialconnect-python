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
    author='Vivial Connect',
    author_email='support@support.vivialconnect.net',
    url='https://www.vivialconnect.net/',
    packages=['vivialconnect'],
    package_data={'vivialconnect': ['../VERSION']},
    install_requires=['requests >= 1.0.0', 'six'],
    long_description=long_description,
    test_suite='test',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    platforms='any',
)
