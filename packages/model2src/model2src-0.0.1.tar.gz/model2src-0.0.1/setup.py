import re
import setuptools
from setuptools import setup

with open('model2src/version.py') as fid:
    try:
        __version__, = re.findall( '__version__ = "(.*)"', fid.read() )
    except:
        raise ValueError("could not find version number")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='model2src',
    version=__version__,
    description='Model2src - Convert pytorch model to source file.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/misads/model2src',
    author='Haoyu Xu',
    author_email='xuhaoyu@tju.edu.cn',
    license='MIT',
    install_requires=[
        "torch",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.5',
)
