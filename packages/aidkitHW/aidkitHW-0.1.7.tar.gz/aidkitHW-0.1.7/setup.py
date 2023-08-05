from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='aidkitHW',
    version='0.1.7',    
    description='Python package for coding challenge',
    url='https://github.com/hududed',
    author='Hud Wahab',
    author_email='hudwahab@gmail.com',
    license='Apache License 2.0',
    packages=['aidkitHW'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['fastai',
                      'fastcore',
                      'fastinferenz[all]',
                      'timm',
                      'tensorflow==1.15',
                      'onnx', 
                      'onnxruntime',                
                      ],
    )

