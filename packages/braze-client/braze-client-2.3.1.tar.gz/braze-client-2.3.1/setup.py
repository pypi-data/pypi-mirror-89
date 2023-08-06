from setuptools import find_packages
from setuptools import setup

NAME = "braze-client"
VERSION = "2.3.1"

REQUIRES = ["requests >=2.21.0, <3.0.0", "tenacity >=5.0.0, <6.0.0"]

EXTRAS = {"dev": ["tox"]}

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    description="Braze Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dtatarkin/braze-client",
    author_email="mail@dtatarkin.ru",
    keywords=["Appboy", "Braze"],
    install_requires=REQUIRES,
    extras_require=EXTRAS,
    packages=find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.6",
)
