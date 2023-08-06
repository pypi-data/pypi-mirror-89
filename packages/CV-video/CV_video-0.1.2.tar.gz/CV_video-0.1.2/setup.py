#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import setuptools

setup(
    name='CV_video',  # 包的名字
    author='zhuyancun',  # 作者
    version='0.1.2',  # 版本号
    license='MIT',

    description='Loading IP camera and display with Opencv3',  # 描述
    long_description='''long description''',
    author_email='mydeepl@foxmail.com',  # 你的邮箱**
    url='https://github.com/Relvyy/',  # 可以写github上的地址，或者其他地址
    # 包内需要引用的文件夹
    # packages=setuptools.find_packages(exclude=['url2io',]),
    packages=["video"],
    # keywords='NLP,tokenizing,Chinese word segementation',
    # package_dir={'jieba':'jieba'},
    # package_data={'jieba':['*.*','finalseg/*','analyse/*','posseg/*']},

    # 依赖包
    install_requires=[
        'opencv-python >= 3.4.10',
        "matplotlib == 3.3.0",
    ],
    classifiers=[
        # 'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        #'Operating System :: Linux'  # 你的操作系统  OS Independent      Microsoft
        #'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        # 'License :: OSI Approved :: BSD License',  # BSD认证
        'Programming Language :: Python',  # 支持的语言
        'Programming Language :: Python :: 3',  # python版本 。。。
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=True,
)
