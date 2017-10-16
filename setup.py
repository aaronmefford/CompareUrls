"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='compare_urls',

    version='0.1',

    description='A script to compare the content of two urls and return the similarity using simhash',
    long_description=long_description,

    url='https://github.com/aaronmefford/CompareUrls',

    author='Aaron Mefford',
    author_email='aaron@mefford.org',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Similarity, Hashing',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='simhash similarity near-duplicate',

    packages=[],
    scripts=['compare.py'],

    install_requires=['mmh3'],

    entry_points={
        'console_scripts': [
            'compare_urls=compare:main',
        ],
    },
)
