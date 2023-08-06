# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('long_description.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    package_license = f.read()

setup(
    name='flightradar24',
    version='0.3.1',
    description='Data library for Flight Radar 24',
    long_description_content_type='text/x-rst',
    long_description=readme,
    author='Mehmet Korkmaz',
    author_email='mehmet@mkorkmaz.com',
    url='https://github.com/mkorkmaz/flightradar24',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=["requests"]
)

