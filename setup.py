# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# single-sourcing the version
with open(path.join(here, 'dependency_render/_version.py')) as f:
    exec(f.read())

setup(
    name='dependency-render',

    # Version single-sourced from dependency_render/_version.py
    version=__version__,

    description='A command-line tool that renders a graph of dependencies. It takes as input a CSV called `dependencies.csv`, and uses Graphviz to generate a dependency map as an image.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/AaronTraas/dependency-render',

    # Author details
    author='Aaron Traas',
    author_email='aaron@traas.org',

    # Choose your license
    license='LGPLv3+',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 3',
    ],

    packages=find_packages(exclude=['tests']),

    setup_requires=['babel'],
    install_requires=['graphviz'],

    include_package_data=True,

    entry_points={
        'console_scripts': [
            'dependency_render=dependency_render:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/AaronTraas/dependency-render/issues',
        'Source': 'https://github.com/AaronTraas/dependency-render',
    },
)
