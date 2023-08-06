#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages
from datacenter import __version__

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []
with open("requirements.txt") as f:
    for line in f.readlines():
        requirements.append(line.strip())

setup_requirements = requirements

test_requirements = ['pytest>=3', ]

setup(
    author="Tacey Wong",
    author_email='xinyong.wang@xtalpi.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="datacenter-sdk and datacenter-cli for DataCenter@XARC",
    entry_points={
        'console_scripts': [
            'datacenter=datacenter.cli:main',
        ],
    },
    install_requires=requirements,
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='datacenter',
    name='datacenter',
    packages=find_packages(include=['datacenter', 'datacenter.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://bitbucket.org/wangxinyong-xtalpi/datacenter',
    version=__version__,
    zip_safe=False,
)
