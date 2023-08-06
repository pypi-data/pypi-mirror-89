from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zipexec",
    version="1.0",
    author_email="lo127001@gmail.com",
    description="Unzip zip files and run commands against the contents",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GNU Lesser General Public License v3 (LGPLv3)',
    url='http://github.com/markbaggett/zipexec',
    packages=['zipexec'],
    include_package_data=True,
    install_requires=[
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['zipexec=zipexec.__main__:main']
    }
)

