import json
import os
from setuptools import setup, find_packages

from ssmenv import __version__

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as f:
    README = f.read()

with open("Pipfile.lock") as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["default"].items()
    ]
    tests_require = [
        package_name + package_data["version"]
        for package_name, package_data in lock_data["develop"].items()
    ]

setup(
    name='ssmenv',
    version=__version__,
    description='Allows you to read parameters from AWS Parameter Store and operate on results as on dictionary.',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="aws boto ssm parameter parameter-store lambda environment-variables",
    author="Daniel Ancuta",
    author_email="whisller@gmail.com",
    url="https://github.com/whisller/ssmenv",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries"
    ],
    install_requires=install_requires,
    tests_require=tests_require,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
