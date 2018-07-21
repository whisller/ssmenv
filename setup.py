import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()

setup(
    name='ssm_or_env',
    version='0.5',
    description='Reads parameters from AWS SSM if in AWS context, otherwise returns Environment variables',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
