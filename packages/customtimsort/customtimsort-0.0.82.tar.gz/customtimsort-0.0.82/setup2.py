import setuptools
from setuptools import find_packages
from distutils.core import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

module1 = Extension('timsort',
                    sources = ['sorting_code/timsort.c'], library_dirs = ['sorting_code/', 'sorting_code/clinic/'], include_dirs = ['sorting_code/include/'])

setuptools.setup(
    name="customtimsort",
    version="0.0.82",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    ext_modules = [module1],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
)
