#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='CVG',
        version='0.1',
        author='Jay9z',
        description='pure python algorithms of computer vision for computer graphics',
        url='https://github.com/jay9z/CVG',
        packages=['CVG', 'CVG.classifiers', 'CVG.clustering', 'CVG.geometry',
                'CVG.imagesearch', 'CVG.localdescriptors', 'CVG.tools'],
        requires=['NumPy', 'Matplotlib', 'SciPy'],
        )
