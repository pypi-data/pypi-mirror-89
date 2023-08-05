#!/usr/bin/env python
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    # basic
    name='rocc-client',
    version='0.1.3',
    # packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    # py_modules=['hello'],
    # scripts=['bin/nlp-evaluate'],

    packages=setuptools.find_packages(),
    entry_points={
        # 'console_scripts': ['rocc-cli=roccclient.cli.__main__:main']
    },

    # requirements
    python_requires='>=3.6.*',
    install_requires=[
        'certifi>=14.05.14',
        'python_dateutil>=2.5.3',
        'setuptools>=21.0.0',
        'six>=1.10',
        'urllib3>=1.15.1'
    ],

    # metadata to display on PyPI
    description='ROCC Client Library for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Sage-Bionetworks/rocc-client',
    author='The ROCC Team',
    author_email='thomas.schaffter@sagebionetworks.org',
    license='Apache',
    project_urls={
        "Source Code": "https://github.com/Sage-Bionetworks/rocc-client",
        "Bug Tracker": "https://github.com/Sage-Bionetworks/rocc-client/issues",
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ]
)
