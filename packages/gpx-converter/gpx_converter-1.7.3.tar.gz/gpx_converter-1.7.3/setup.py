#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages


requirements = [
    "gpxpy >= 1.4.0",
    "numpy >= 1.18.1",
    "pandas >= 1.0.3",
]


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3.6', ]

setup(
    author="Nidhal Baccouri",
    author_email='nidhalbacc@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Education',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python package for manipulating gpx files and easily convert gpx to other different formats.",
    entry_points={
        'console_scripts': [
            'gpx_converter=gpx_converter.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['gpx_converter',
              'GPX', 'GPS', 'GSI', 'Global Positioning System', 'Positioning System',
              'Position', 'GPS conversion', 'GPX conversion',
              'convert gpx to csv', 'convert csv to gpx', 'convert gpx to json',
              'convert gpx to array', 'convert json to gpx'],
    name='gpx_converter',
    packages=find_packages(include=['gpx_converter', 'gpx_converter.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nidhaloff/gpx_converter',
    version='1.7.3',
    zip_safe=False,
)
