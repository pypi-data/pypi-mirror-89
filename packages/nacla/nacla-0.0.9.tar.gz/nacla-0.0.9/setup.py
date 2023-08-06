#coding:utf-8
from distutils.core import setup

from setuptools import setup, find_packages

setup(

    name = 'nacla',

    version = '0.0.9',

    keywords = ('name classify', 'nlp'),

    description = '输入一个姓名，输出这个姓名输入哪个国家',

    license = 'MIT',

    author = 'zhaomingming',

    author_email = '13271929138@163.com',

    #packages = find_packages(),
    #py_modules=['nacla.nacla']
    packages=find_packages(where='nacla'),  # Required

    platforms = 'python>=3.6.7',
     # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={  # Optional
        'model': ['rnn.pth'],
    },
    #data_files=[('model', ['nacla/model/rnn.pth'])],

    #py_modules=['nacla.nacla']
    #packages=find_packages(where='nacla'),  # Required

)

