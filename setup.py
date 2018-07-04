import json
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()

with open('Pipfile.lock') as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['default'].items()
    ]

setup(
    name='ssm_or_env',
    version='0.1',
    description='Reads parameters from AWS SSM if in AWS context, otherwise returns Environment variables',
    long_description=README,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
