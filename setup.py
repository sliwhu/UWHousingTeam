from distutils.core import setup
import os
from setuptools import setup, find_packages
PACKAGES = find_packages()


opts = dict(
    name='UWHousingTeam',
    version='0.1',
    packages=PACKAGES,
    package_data={'UWHousingTeam': ['Scripts/*', 'tests/*']},
    url='https://github.com/sliwhu/UWHousingTeam',
    license='MIT',
    author='dipsm',
    author_email='deepa15@uw.edu',
    description='First Stop for First Time Home Buyers'
)

if __name__ == '__main__':
    setup(**opts)