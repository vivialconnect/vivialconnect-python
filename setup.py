import re
import ast
from setuptools import setup

_version_re = re.compile(r"VERSION\s+=\s+(.*)")

with open("vivialconnect/version.py", "rb") as f:
    version = str(
        ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1))
    )


def readme():
    with open("README.rst", "r") as f:
        return f.read()


setup(
    name="vivialconnect",
    version=version,
    description="Vivial Connect API Client Library for Python",
    license="MIT",
    author="Vivial Connect",
    author_email="support@support.vivialconnect.net",
    url="https://www.vivialconnect.net/",
    packages=["vivialconnect", "vivialconnect.common", "vivialconnect.resources"],
    install_requires=["requests >= 1.0.0", "six"],
    long_description=readme(),
    test_suite="test",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["vivial", "vivialconnect"],
    platforms="any",
)
