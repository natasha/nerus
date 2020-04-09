
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


setup(
    name='nerus',
    version='1.7.0',
    description='Large silver standart Russian corpus with NER, morphology and syntax markup',
    long_description=description,
    long_description_content_type='text/markdown',
    url='https://github.com/natasha/nerus',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='russian, nlp, datasets, ner, morphology, syntax',
    install_requires=[],
    packages=find_packages(),
)
