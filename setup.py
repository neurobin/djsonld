# -*- coding: utf-8 -*-
# from __future__ import unicode_literals
import os
import sys
from codecs import open
from setuptools import find_packages, setup

sys.path[0:0] = ['djsonld']

from version import __version__

def get_readme(filename):
    content = ""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as readme:
            content = readme.read()
    except Exception as e:
        pass
    return content

setup(name="djsonld",
      version=__version__,
      author="Md. Jahidul Hamid",
      author_email="jahidulhamid@yahoo.com",
      description="Get jsonld for a webpage",
      license="BSD",
      keywords="django cms content management system",
      url="https://github.com/neurobin/djsonld",
      packages=find_packages(),
      long_description=get_readme("README.md"),
      long_description_content_type="text/markdown",
      classifiers=[
        # See: https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
      ],
      install_requires=["django>=2.2.1",],
  )
