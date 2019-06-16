
from setuptools import setup, find_packages

setup(
    name='nerus',
    version='1.0',
    install_requires=[],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nerus-ctl=nerus.ctl.__main__:main'
        ],
    }
)
