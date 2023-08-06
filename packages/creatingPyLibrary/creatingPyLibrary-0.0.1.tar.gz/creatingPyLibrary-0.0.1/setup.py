from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education', 
    'Operating System :: Microsoft :: Windows :: Windows 10', 
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3'
]

setup(
    name = 'creatingPyLibrary',
    version = '0.0.1',
    description = 'A very basic calculator', 
    Long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author = 'Omar Miah', 
    author_email='Omiahcs@gmail.com', 
    License ='MIT',
    classifiers = classifiers,
    keywords='calculator',
    pachakes = find_packages(),
    install_requires=['']    
)