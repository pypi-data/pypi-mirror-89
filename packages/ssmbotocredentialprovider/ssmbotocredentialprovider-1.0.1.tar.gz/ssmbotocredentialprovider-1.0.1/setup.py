#!/usr/bin/env python

import os
from setuptools import setup, find_packages

setup(name='ssmbotocredentialprovider',
      version='1.0.1',
      description='AWS SSM Credential Provider: create boto sessions which obtain and renew credentials from an AWS SSM device certificate',
      author='Craig I. Hagan',
      author_email='hagan@cih.com',
      url='https://github.com/craighagan/ssmbotocredentialprovider',
      license='MIT',
      packages = find_packages(exclude=["test"]),
      install_requires=["boto3","requests"],
      setup_requires=["pytest-runner"],
      tests_require=["pytest", "pytest-runner"],
      scripts=["bin/fakemetadata-server.py"],
)
