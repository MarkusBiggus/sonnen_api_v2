from setuptools import setup, find_packages
import os


def read_file(file):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, file), mode='r', encoding='UTF-8') as file:
        return file.read()


def get_version(file):
    for line in read_file(file).splitlines():
        if line.startswith('__version__'):
            delimiter = '"' if '"' in line else "'"
            return line.split(delimiter)[1]
    else:
        raise RuntimeError('Version not found!')

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='sonnen_api_v2',
#    use_scm_version=True,
    version=get_version('sonnen_api_v2/__init__.py'),
    packages=find_packages(exclude='tests'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Katamave/sonnen_api_v2.git',
    license="MIT",
    author='Vaclav Silhan',
    author_email='katamave@gmail.com',
#    description=read_file('README.md'),
    description="Sonnen batterie API V2. Compatible with Home Assistant integrations.",
    install_requires=[
        'requests~=2.32.3',
        'aiohttp>=3.11.11',
        'isal~=1.7.1',
        'aiohttp-fast-zlib>=0.2.0,<4.0.0',
        'urllib3>=1.26.20,<2.0.0',
        'yarl~=1.18.3',
        "setuptools~=75.7.0",
        "propcache~=0.2.1",
        "attrs~=24.2.0",
        "pytest-asyncio~=0.24.0",
    ],
    python_requires=">=3.12",
)
