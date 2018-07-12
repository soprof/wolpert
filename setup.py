#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="wolpert",
      description="Stacked generalization framework",
      url="https://github.com/caioaao/wolpert",
      author="Caio Oliveira",
      license="new BSD",
      classifiers=['Intended Audience :: Science/Research',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: Scientific/Engineering',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Operating System :: Unix',
                   'Operating System :: MacOS',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'],
      package_dir={'wolpert': 'wolpert'},
      packages=find_packages(include=['wolpert', 'wolpert.*']),
      version="0.0.1",
      install_requires=["scikit-learn>=0.20"], # this package is under development
      include_package_data=True,
      zip_safe=False)
