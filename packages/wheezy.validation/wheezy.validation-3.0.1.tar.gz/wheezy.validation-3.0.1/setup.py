#!/usr/bin/env python

import multiprocessing
import os
import re

from setuptools import setup

extra = {}
try:
    from Cython.Build import cythonize

    p = os.path.join("src", "wheezy", "validation")
    extra["ext_modules"] = cythonize(
        [os.path.join(p, "*.py")],
        exclude=os.path.join(p, "__init__.py"),
        # https://github.com/cython/cython/issues/3262
        nthreads=0 if multiprocessing.get_start_method() == "spawn" else 2,
        compiler_directives={"language_level": 3},
        quiet=True,
    )
except ImportError:
    pass

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()
VERSION = (
    re.search(
        r'__version__ = "(.+)"',
        open("src/wheezy/validation/__init__.py").read(),
    )
    .group(1)
    .strip()
)

setup(
    name="wheezy.validation",
    version=VERSION,
    python_requires=">=3.6",
    description="A lightweight object validation library",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/akornatskyy/wheezy.validation",
    author="Andriy Kornatskyy",
    author_email="andriy.kornatskyy@live.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="validation rules model",
    packages=["wheezy", "wheezy.validation"],
    package_dir={"": "src"},
    namespace_packages=["wheezy"],
    zip_safe=False,
    platforms="any",
    **extra
)
