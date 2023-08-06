#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup, Extension
import glob

module = Extension('SPxml',
                   define_macros=[('MAJOR_VERSION', '1'),
                                  ('MINOR_VERSION', '0')],
                   include_dirs=['/usr/include/libxml2'],
                   libraries=['xml2'],
                   sources=['spxmlmodule.c', 'libsierraecg/lzw.c', 'libsierraecg/sierraecg.c', 'libsierraecg/b64.c'])
                #    sources=['spxmlmodule.c'])

setup(name='SPxml',
      version='1.1',
      description='This is a package to read ECG results in XML files with Sierra Philips format ',
      author='guolong',
      author_email='guojoongg@gmail.com',
      url='',
      ext_modules=[module],
      data_files=[('libsierraecg', glob.glob('libsierraecg/*'))],
      )
