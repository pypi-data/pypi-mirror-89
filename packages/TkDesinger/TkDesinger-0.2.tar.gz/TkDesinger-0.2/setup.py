from setuptools import setup
import os

__path__ = os.getcwd() + '\\setup.py'

setup (
    name='TkDesinger',
	long_description=open('README.rst').read(),
    version='0.2',
    packages=['tkdesinger'],
    url='http://ppbe.ru',
    license='MIT',
    author='FotonPC',
    author_email='fototn-pc@inbox.ru',
    description='Tkinter Desinger to Python 3',
)
