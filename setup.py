from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(exclude = ['docs', 'tests*']),
    version='0.1.0',
    description='Exploring Retail Grocery Dataset',
    author='Ryan Johnson',
    license='MIT',
)