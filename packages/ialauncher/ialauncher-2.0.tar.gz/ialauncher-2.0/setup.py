#!/usr/bin/env python3
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'ialauncher',
    version = '2.0',
    author = 'Jaap Joris Vens',
    author_email = 'jj@rtts.eu',
    description = 'Play all of the Internet Archive’s MS-DOS games offline!',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/rtts/ialauncher',
    packages = setuptools.find_packages(),
    scripts = ['bin/ialauncher'],
    include_package_data = True,
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
    ],
    python_requires = '>=3.8',
    install_requires = [
        'pygame',
    ],
)
