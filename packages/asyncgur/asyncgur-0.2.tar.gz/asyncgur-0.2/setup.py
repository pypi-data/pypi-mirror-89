import setuptools
from distutils.core import setup

setup(
    name='asyncgur',
    version='0.2',
    packages=['asyncgur',],
    license='MIT License',
    install_requires=['aiohttp', 'dacite',],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Dylee',
    author_email='oyinxdoubx@gmail.com',
    url='https://github.com/dyleee/asyncgur',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
