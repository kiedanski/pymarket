#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['pandas == 0.23; python_full_version <= "3.5.2"',
                'pandas > 0.23; python_full_version > "3.5.2"',
                'numpy>=1.12',
                'networkx==2.2; python_version <= "3.5"',
                'networkx>=2.3; python_version > "3.5"',
                'pulp >= 1.6',
                'matplotlib == 2.2.4; python_version <= "3.5"',
                'matplotlib >= 2.2.4; python_version >= "3.6"',
                ]

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
    packages=['pymarket', 'pymarket.bids','pymarket.datasets', 'pymarket.mechanisms', 'pymarket.plot', 'pymarket.statistics', 'pymarket.transactions', 'pymarket.utils'],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gus0k/pymarket',
    version='0.7.6',
    zip_safe=False,
)
