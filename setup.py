import os
from setuptools import setup, find_packages
PACKAGES = find_packages()


opts = dict(
    name='UWHousingTeam',
    version='0.1',
    url='https://github.com/sliwhu/UWHousingTeam',
    license='MIT',
    author='firststop',
    author_email='deepa15@uw.edu',
    description='First Stop for First Time Home Buyers'
    packages=PACKAGES,
    package_data={'UWHousingTeam': ['Scripts/*', 'tests/*']},
 
)

if __name__ == '__main__':
    setup(**opts)