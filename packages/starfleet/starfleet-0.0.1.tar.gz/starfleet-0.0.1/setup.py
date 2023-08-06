#!/usr/bin/env python3

import setuptools

setuptools.setup(
  name = 'starfleet',
  version = '0.0.1',
  description = 'A Simple Training Platform',
  author = 'acegik',
  license = 'GPL-3.0',
  url = 'https://github.com/acegik/starfleet',
  download_url = 'https://github.com/acegik/starfleet/downloads',
  keywords = ['distributed-locks'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  python_requires=">=3.0,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)
