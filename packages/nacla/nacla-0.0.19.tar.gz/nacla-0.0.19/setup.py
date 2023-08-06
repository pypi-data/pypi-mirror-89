#coding:utf-8
from distutils.core import setup

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')
setup(

    name = 'nacla',

    version = '0.0.19',

    keywords = ('name classify', 'nlp'),

    description = '输入一个姓名，输出这个姓名输入哪个国家',
    long_description=long_description,

    license = 'MIT',

    author = 'zhaomingming',
    url='https://github.com/pypa/sampleproject',  # Optional

    author_email = '13271929138@163.com',
    #package_dir={'': 'src'},  
    #packages = find_packages(),
    #py_modules=['nacla.nacla']
    packages=find_packages(),  # Required
    python_requires='>=3.5, <4',
     # If there are data files included in your packages that need to be
    # installed, specify them here.
    #package_data={  # Optional
    #    'src/model': ['rnn.pth'],
    #},
    include_package_data=True,
    #data_files=[('model', ['nacla/model/rnn.pth'])],

    #py_modules=['nacla.nacla']
    #packages=find_packages(where='nacla'),  # Required

)

