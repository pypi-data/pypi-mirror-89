import setuptools
from setuptools import find_packages
from distutils.core import setup, Extension
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

path_now = "/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/"

main_module = Extension('timsort',
                        sources=[path_now + "timsort.c"],
                        library_dirs=[path_now, path_now + "clinic/"],
                        include_dirs=[path_now + "include/"])


setuptools.setup(
    name="customtimsort",
    version="0.0.74",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    packages=find_packages(),
    #ext_modules=[main_module],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
)

