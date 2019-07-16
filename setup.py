#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=6.0', 'pandas>=0.24', 'numpy>=1.16', 'networkx', 'pulp', 'matplotlib']

setup_requirements = ['pytest-runner']

test_requirements = ['pytest']

setup(
    author="Diego Kiedanki",
    author_email='gusok@protonmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="A simple library for simulating markets in Python",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='pymarket',
    name='pymarket',
    packages=find_packages(include=['pymarket']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gus0k/pymarket',
    version='0.7.4',
    zip_safe=False,
)
