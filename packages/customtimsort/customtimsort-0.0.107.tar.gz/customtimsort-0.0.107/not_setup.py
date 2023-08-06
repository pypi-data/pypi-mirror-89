from distutils.core import setup, Extension

module1 = Extension('timsort',
                    sources = ['timsort.c'], include_dirs = ['sorting_code'])

setup (name = 'timsort',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
