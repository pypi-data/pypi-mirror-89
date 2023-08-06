#!/usr/bin/env python

"""w01fm00n
Copyright (C) 2020 w01f - https://github.com/w01fdev/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

########################################################################

w01f hacks from Linux for Linux!

fck capitalism, fck patriarchy, fck racism, fck animal oppression ...

########################################################################
"""


from setuptools import setup

from w01fm00n.program import (VERSION, HACKERS, NAME,
                              LICENSE, URL)


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name=NAME,
    version=VERSION,
    author=HACKERS[0],
    author_email='w01f@w01f.dev',
    url=URL,
    license=LICENSE,
    description='terminal-based forensic utility',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['w01fm00n', ],
    python_requires='>=3.3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        "console_scripts": [
            "w01fm00n=w01fm00n:main",
        ],
    },
)
