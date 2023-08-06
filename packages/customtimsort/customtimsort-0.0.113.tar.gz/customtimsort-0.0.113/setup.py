import setuptools
from setuptools import find_packages
from distutils.core import setup, Extension
import sys

with open("README.md", "r") as fh:
    long_description = fh.read()

path_now = "/home/leha/Desktop/projects/library/CustomTimSort_2/sorting_code/"

main_module = Extension('timsort',
                        sources=["llistobject.c", "timsort.c"],
                        library_dirs=["", "clinic"],
                        include_dirs=["include"])


setuptools.setup(
    name="customtimsort",
    version="0.0.113",
    author="lehatr",
    author_email="lehatrutenb@gmail.com",
    description="Timsort sorting algorithm with custom minrun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lehatrutenb/FastTimSort",
    packages=['timsort'],
    package_dir={'timsort': ''},
    package_data={'timsort': ['*', 'clinic/*', 'cpython/*']},
    #package_dir = {'': ''},
    ext_modules=[main_module],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2',
)

