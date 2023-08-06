#!/usr/bin/env python
# coding:utf-8

import setuptools


setuptools.setup(
    name='loglizer',
    version='1.0',
    description='工具来自https://github.com/logpai/loglizer, 根据原作者原意, 请大家用于开源研究, 如需授权请联系原作者, 侵删',
    author='avocador',
    author_email='avocador@163.com',
    packages=setuptools.find_packages(),
    platforms=['all'],
    url='https://github.com/logpai/loglizer',
    license='BSD License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8'
    ],
    python_requires='>=3',
)