# Copyright 2020 - RidgeRun LLC
# Author: Luis G. Leon Vega <luis.leon@ridgerun.com>
# Licenced under MIT
# Support: only Linux/MacOS with BASH

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="local_ci_hooks",
    version="0.1.1",
    author="Luis G. Leon-Vega",
    author_email="luis.leon@ridgerun.com",
    description="Install a Local CI engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/lleon95/local-ci-hooks.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
    ],
    scripts=['local_ci_hooks/local_ci_hooks'],
    package_data={'': ['*.hook', '*.sh']},
    include_package_data=True,
    install_requires=[
    ],
    python_requires='>=3.8',
)
