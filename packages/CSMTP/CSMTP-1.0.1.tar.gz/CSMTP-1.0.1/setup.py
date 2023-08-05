import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="CSMTP",
    version="1.0.1",
    description="CSMTP(Custom Simple Mailing Transfer Protocol) is a module for sending emails using python. It is an abstraction of the smtp library",
    url="https://elloko233.github.io/CustomSimpleMailingTransferProtocol/",
    author="Real Python",
    author_email="ellokoprograma@gamil.com",
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["CSMTP"],
    include_package_data=True,
    install_requires=["validate_email"],
)
