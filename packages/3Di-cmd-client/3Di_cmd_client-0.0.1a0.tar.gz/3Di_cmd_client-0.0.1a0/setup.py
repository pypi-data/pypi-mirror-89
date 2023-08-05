#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


with open('README.md') as readme_file:
    readme = readme_file.read()


with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as req_file:
    requirements = req_file.read().splitlines()

with open('requirements_dev.txt') as dev_req_file:
    setup_requirements = dev_req_file.read().splitlines()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

test_requirements = []


setup(
    author="Jelle Prins",
    author_email='info@nelen-schuurmans.nl',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
        'Topic :: Scientific/Engineering',
    ],
    description="Python 3Di command line client",
    long_description_content_type='text/markdown',
    long_description=readme + '\n\n' + history,
    install_requires=requirements,
    license="MIT license",
    entry_points={
        "console_scripts": [
            "scenario=cmd_client.commands.run_scenario:cli",
            "suite=cmd_client.commands.run_suite:run",
            "active_simulations=cmd_client.commands.active_simulations:cli"
        ]
    },
    include_package_data=True,
    keywords='3Di, client, command line, scenario',
    name='3Di_cmd_client',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
        include=['cmd_client', 'cmd_client.*'],
    ),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nens/3Di-cmd',
    version=find_version('cmd_client', 'version.py'),
    zip_safe=False,
)
