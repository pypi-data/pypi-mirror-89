"""
@Date    : 2020-12-18
@Author  : liyachao
"""
import setuptools
from setuptools import setup

setup(name='py_ios_device',
      version="0.13",
      description='Get ios data and operate ios devices',
      author='chenpeijie & liyachao',
      author_email='me@aaronsw.com',
      maintainer='liyachao',
      maintainer_email='liyc_self@163.com',
      url='',
      package_data={'py_ios_device': ['src/*', 'util/*']},
      packages=setuptools.find_packages(),
      long_description="",
      license="Public domain",
      platforms=["any"],
      )
