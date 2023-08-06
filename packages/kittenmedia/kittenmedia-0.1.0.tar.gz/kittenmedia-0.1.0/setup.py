from setuptools import setup, find_packages

setup(
  name='kittenmedia',
  version='0.1.0',
  keywords=('kittenmedia'),
  license='MIT',
  author='riven',
  url='https://gitee.com/KittenTech/pylib_kittenmedia',
  author_email='riven@kittenbot.cc',
  packages=find_packages(exclude=('tests')),
  install_requires=['SimpleWebSocketServer'],
  description="a ws socket based multimedia bridge lib for kittencode IDE",
  platform='any'
)

