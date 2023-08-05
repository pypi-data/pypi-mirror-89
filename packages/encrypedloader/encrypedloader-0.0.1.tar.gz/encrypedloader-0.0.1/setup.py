from setuptools import setup, find_packages
from distutils.extension import Extension
try:
      from Cython.Build import cythonize, build_ext
except:
      build_ext = None

DEBUG = False

version = '0.0.1'

setup(name='encrypedloader',
      version=version,
      description="import encrypted python code",
      long_description="""\
 """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='encrypted python code',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "click>=7.1.2",
          "salsa20>=0.3.0"
      ],
      cmdclass={'build_ext': build_ext} if DEBUG is not None else {},
      ext_modules=cythonize("encrypedloader/loader.pyx", language_level = "3") if DEBUG is not None else [Extension('encrypedloader.', ['encrypedloader/loader.c'])] ,
      entry_points={
                'console_scripts': ['t2pub=encrypedloader:main'],
            }
      )
