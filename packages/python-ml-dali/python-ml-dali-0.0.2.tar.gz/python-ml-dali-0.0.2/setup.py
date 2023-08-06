#!/usr/bin/env python
"""The setup script."""


from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='python-ml-dali',
    version='0.0.2',
    url='https://github.com/benoitdepaire/python-ml-dali',
    license='GNU GPLv3',
    author='Benoit Depaire',
    install_requires=[],
    author_email='benoît@depaire.net',
    description='A Python library to communicate with Dali controllers from Ministry of Light',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=["mldali"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires = '>=3.8',

)