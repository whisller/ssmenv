import os
from setuptools import setup, find_packages

from ssm_or_env import __version__

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()

setup(
    name='ssm_or_env',
    version=__version__,
    description='Reads parameters from AWS parameter store (if possible) or ENV.',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="aws boto ssm parameter",
    author="Daniel Ancuta",
    author_email="whisller@gmail.com",
    url="https://github.com/whisller/ssm_or_env",
    license="MIT",
    python_requires=">=2.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries"
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
