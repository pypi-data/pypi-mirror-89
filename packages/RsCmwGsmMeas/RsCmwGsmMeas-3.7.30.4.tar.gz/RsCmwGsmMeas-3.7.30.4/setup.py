import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="RsCmwGsmMeas",
    version="3.7.30.4",
    description="CMW GSM Measurement Remote-control Module",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Rohde & Schwarz GmbH & Co. KG",
    copyright="Copyright © Rohde & Schwarz GmbH & Co. KG 2020",
    author_email="Customer.Support@rohde-schwarz.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    packages=(find_packages(include=['RsCmwGsmMeas', 'RsCmwGsmMeas.*'])),
    install_requires=['PyVisa']
)