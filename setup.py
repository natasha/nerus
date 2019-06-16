
from setuptools import setup, find_packages

setup(
    name='nerus',
    version='1.2.0',
    install_requires=['pullenti_client>=0.2.0'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nerus-ctl=nerus.ctl.__main__:main'
        ],
    }
)
