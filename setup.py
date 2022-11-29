from setuptools import setup, find_packages

setup(name='badboybot', version='1.0', packages=find_packages(), extras_require = {'dev':['requests'], 'build': ['requests']})