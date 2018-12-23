import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()

setup(
    name='ssm_or_env',
    version='0.6',
    description='Deprecated. Use https://pypi.org/project/ssmenv/ instead.',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
