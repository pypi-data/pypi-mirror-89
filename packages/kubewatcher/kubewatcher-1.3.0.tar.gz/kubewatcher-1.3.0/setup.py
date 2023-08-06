import inspect
import os

from setuptools import setup, find_packages

from kubewatcher.kubewatcher import cli


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


def entry_point(name, func):
    module = inspect.getmodule(func)
    return f"{name}={module.__name__}:{func.__name__}"


setup(
    name='kubewatcher',
    version='1.3.0',
    description='See https://github.com/tonsV2/kubewatcher',
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=[
        'kubernetes~=12.0.1',
        'ruamel.yaml~=0.16.12',
        'envyaml~=1.1.201202'
    ],
    entry_points={
        'console_scripts': [entry_point("kubewatcher", cli)]
    },
    long_description=read('README.md'),
)
