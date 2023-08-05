from setuptools import setup

setup(
    name='aidkitHW',
    version='0.1.5',    
    description='Python package for coding challenge',
    url='https://github.com/hududed',
    author='Hud Wahab',
    author_email='hudwahab@gmail.com',
    license='Apache License 2.0',
    packages=['aidkitHW'],
    install_requires=['fastai',
                      'fastcore',
                      'fastinferenz[all]',
                      'timm',
                      'tensorflow==1.15',
                      'onnx', 
                      'onnxruntime',                
                      ],
    )

