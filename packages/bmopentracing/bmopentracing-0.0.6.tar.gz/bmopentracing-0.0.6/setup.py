#!/usr/bin/env python


import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bmopentracing',
    version='0.0.6',
    author='Vadim Geshiktor',
    author_email='vadim.geshiktor@beyoundminds.ai',
    descripton='Opentracing tracers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/beyondminds/bm-opentracing',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6'
)
