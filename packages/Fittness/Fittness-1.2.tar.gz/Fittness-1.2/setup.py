from setuptools import setup, find_packages
setup(
name='Fittness',
version='1.2', 
packages=find_packages(exclude=['tests*']), 
license='MIT',
description="A test python package",
install_requires=['bokeh','pygal'],
url='https://github.com/RaineShen/data533Lab4.git', 
author='YuxuanIsme,raineShen',
author_email='cuiyuuxuan@gmail.com,rain.ya1213@gmail.com'
)
 