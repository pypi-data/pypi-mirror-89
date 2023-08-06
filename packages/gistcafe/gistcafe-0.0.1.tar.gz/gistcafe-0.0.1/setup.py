#!/usr/bin/env python

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

dependencies = ['dataclasses-json>=0.5.2',
                'tabulate>=0.8.7']

setuptools.setup(
    name="gistcafe",
    version="0.0.1",
    author="ServiceStack, Inc.",
    author_email="team@servicestack.net",
    description="gist.cafe utils for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ServiceStack/gistcafe-python",
    license="BSD-3-Clause",
    keywords='gistcafe,dump,prettyprint',
    install_requires=dependencies,
    packages=setuptools.find_packages(),
    tests_require=['pytest','dataclasses-json>=0.5.2','tabulate>=0.8.7','requests>=2.25.1'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    py_modules=["gistcafe"],
    python_requires='>=3.5',
)
