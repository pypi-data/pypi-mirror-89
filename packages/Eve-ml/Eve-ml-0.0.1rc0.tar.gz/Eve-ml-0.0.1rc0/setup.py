'''
python setup.py sdist bdist_wheel
python -m twine upload dist/*
'''
import setuptools
import glob
import os

from setuptools import find_packages
from setuptools import setup
import sys
from eve.version import __version__

install_requires = """
gym==0.18.0
numpy==1.18.5
optuna==2.3.0
seaborn==0.11.0
stable-baselines3==0.10.0
tensorboard==2.4.0
tensorboard-plugin-wit==1.7.0
torch==1.7.0
torchfile==0.1.0
torchnet==0.0.4
torchvision==0.8.1"""

setup(
    install_requires=install_requires,
    name="Eve-ml",
    version=__version__,
    author="densechen",
    author_email="densechen@foxmail.com",
    description="Eve: make deep learning more interesting.",
    long_description_content_type="text/markdown",
    url="https://github.com/densechen/eve",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires='>=3.6',
)