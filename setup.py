from platform import python_version
from setuptools import setup, find_packages

setup(
    name = 'GLog',
    version='1.0',
    setup_requires=['wheel'],
    install_requires=['requests', 'structlog'],
    python_requires='>=3.8',
    packages=find_packages(),
)