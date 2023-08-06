#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import setuptools
import pathlib
import sys

here = pathlib.Path(__file__).parent.resolve()


def text(*names, encoding='utf8'):
    return here.joinpath(*names).read_text(encoding=encoding)


try:
    version = open('.version').readline()
except FileNotFoundError:
    print("Unable to determine version.")
    print("Set the version on the first line of a '.version' file")
    sys.exit(404)


setuptools.setup(
    name='sylt',
    version=version,
    license="SSPL",
    description="Sylt client SDK library",
    long_description=text("README.md"),
    long_description_content_type="text/markdown",

    author="Anders Åström",
    author_email="anders@lyngon.com",
    url="https://github.com/lyngon/sylt",

    packages=setuptools.find_namespace_packages(
        where="src/lib",
        # include=["common", "sdk"],
        exclude=["*runtime*"]
    ),
    package_dir={'': 'src/lib'},

    classifiers=[  # https://pypi.org/classifiers/
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: Free To Use But Restricted',
        'License :: Other/Proprietary License',
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        'Topic :: Multimedia :: Video',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Image Processing',
        'Topic :: Scientific/Engineering :: Image Recognition',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",  # noqa: E501
        'Typing :: Typed',
    ],
    install_requires=[],
    extras_require={},
    setup_requires=[],
    python_requires='>=3.6',
    keywords="Video Processing, Computer Vision"
)

sys.exit(0)
