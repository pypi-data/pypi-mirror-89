from setuptools import setup

setup(
    name='convertCoding',
    version='v1.1',#version
    description='convert coding method to utf-8, from any other methods.', # description
    py_modules=['convertContent'],
    author='LaiJianxin',
    author_email='ljx15@tsinghua.org.cn',
    url='https://github.com/stopcry/convertCoding',
    requires=['chardet'], #relying packages
    license='MIT'
)
