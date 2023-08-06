#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["requests"]

setup_requirements = requirements

test_requirements = requirements

setup(
    author="Datacenter Downloader & Uploader",
    author_email='xinyong.wang@xtalpi.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Datacenter Downloader & Uploader",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='datacenter_du',
    name='datacenter_du',
    packages=find_packages(include=['datacenter_du', 'datacenter_du.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/taceywong/datacenter_du',
    version='0.1.0',
    zip_safe=False,
)
