#!/usr/bin/env python

"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib, sys

project_version='0.0.1'

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='libelle',  # Required

    version=project_version,  # Required

    description='Libelle AG',  # Optional

    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://www.libelle.com', # Optional

    author='Libelle AG',  # Optional

    author_email='miroslav.jakovljevic@libelle.com',  # Optional

    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],

    keywords='libelle',  # Optional

    package_dir={'': 'src'},  # Optional

    packages=find_packages(where='src'),  # Required

    python_requires='>=3.7, <4',

    entry_points={  # Optional
        'console_scripts': [
            'libelle=libelle.placeholder:main',
        ],
    }
)
