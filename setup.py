import setuptools
from setuptools import setup


setup(
    name='pyshadow',
    description='Selenium plugin to manage shadow DOM elements on web page.',
    version='0.0.1',
    long_description=open("README.md").read(),
    license="Apache License 2",
    author='Sushil Gupta',
    author_email='sushil106768@gmail.com',
    url='https://github.com/sukgu/pyshadow/',
    install_requires=['multipledispatch>=0.6.0'],
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Testers',
        'License :: Apache License 2',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Testing :: Automation',
        'Topic :: Software Testing :: Shadow DOM',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
