from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='MNIST2',  # 包名
      version='1.0.0',  # 版本号
      description='A MNIST OCR package',
      long_description=long_description,
      author='Taolar',
      author_email='Taolar9458@163.com',
      url='https://www.bilibili.com/video/BV164411b7dx?p=12',
      install_requires=['numpy'],
      license='MIT',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Topic :: Software Development :: Libraries'
      ],
      )