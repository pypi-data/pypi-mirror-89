#!/usr/bin/python
# -*-coding:utf-8 -*-
"""
-------------- Description: ------------------
   FileName : setup.py
   Author : 绒毛宝贝
   ProjectName : PyBoard
   IDE Version : PyCharm
   Date:2020/12/5 21:48
   QQ:287000822 E-mail: gomehome@qq.com
------------------- END ----------------------
"""
__author__ = 'Isaac'

import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cutmv",  # Replace with your own username
    version="0.0.4",
    author=__author__,
    author_email="gomehome@qq.com",
    description="small video cut tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/QTDesign/cutmv",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
