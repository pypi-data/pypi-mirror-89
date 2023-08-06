"""
@Date    : 2020-12-18
@Author  : liyachao
"""
import setuptools
from setuptools import setup

# 第三方依赖
requires = [
    "pyOpenSSL>=20.0.1",
    "pyasn1>=0.4.8"
]
setup(name='py_ios_device',
      version="0.25",
      description='Get ios data and operate ios devices',
      author='chenpeijie & liyachao',
      author_email='me@aaronsw.com',
      maintainer='liyachao',
      maintainer_email='liyc_self@163.com',
      url='',
      package_data={"py_ios_device": ["src/*", "src/*/*", "src/*/*/*", "src/*/*/*/*", "utils/*"]},
      packages=["py_ios_device"],
      long_description="",
      license="Public domain",
      platforms=["any"],
      install_requires=requires,  # 第三方库依赖
      )
