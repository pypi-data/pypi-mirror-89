#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="watchtower2",
    version="1.0.1",
    url="https://github.com/moishfromer/watchtower",
    license="Apache Software License",
    author="Moshe Fromer",
    author_email="mofromer@gmail.com",
    description="Python2 CloudWatch Logging",
    long_description=open("README.rst").read(),
    python_requires=">=2.7",
    install_requires=[
        "boto3 >= 1.9, < 2",
    ],
    packages=find_packages(exclude=["test"]),
    platforms=["MacOS X", "Posix"],
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
