import os
from distutils.core import setup

this_directory = os.path.abspath(os.path.dirname(__file__))


def read_file(filename):
    with open(os.path.join(this_directory, filename))as f:
        long_description = f.read()
    return long_description


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


setup(
    name='NetworkLiteratureDownloader',
    python_requires='>=3.8.6',
    version='1.1.0',
    license='MIT',
    description='A Multi-Coroutine Downloader',
    long_description=read_file('README.md'),
    long_description_content_type="text/markdown",
    author='suyu',
    author_email='halfxianhuman@hotmail.com',
    packages=['Downloader'],
    url="https://https://test.pypi.org/legacy/NetworkLiteratureDownloader",
)
