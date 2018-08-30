'''
Setup for the corenlpy, a utility for running corenlpy and reading CoreNLP 
annotation xml files into a Python AnnotatedArticle type, designed to make 
working with CoreNLP easy in Python.
'''

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'corenlpy/README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='corenlpy',
    version='0.0.6',
    description='Work with CoreNLP in Python',
    long_description=long_description,
    url='https://github.com/enewe101/corenlpy',
    author='Edward Newell',
    author_email='edward.newell@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords= (
		'NLP natrual language processing computational linguistics '
		'CoreNLP Stanford parser'
	),

    packages=['corenlpy'],

	#indlude_package_data=True,
	package_data={'': [
		'README.md',
		'data/AIDA/*',
		'data/CoreNLP/*',
		'data/raw-text/*',
	]},
	install_requires=['bs4','corenlp-xml-reader']
)
