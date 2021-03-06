import pathlib
from setuptools import setup,find_packages
import os
# The directory containing this file
HERE = os.path.dirname(os.path.realpath(__file__))

# The text of the README file

with open(HERE + "/README.md",'r') as f:
    README = f.read()
with open(HERE +'/requirements.txt') as f:
    required = f.read().splitlines()
# This call to setup() does all the work
setup(
    name="confo",
    version="0.1.0",
    # description="Confo is a configuration manager, built to support multiple backend systems.",
    long_description=README,
    long_description_content_type='text/markdown',
    url="https://github.com/n3rdydad/confo",
    author="The nerdy dad (kabelo masemola)",
    author_email="kn3rdydad@gmail.com",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=required
)