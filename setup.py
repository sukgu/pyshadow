import setuptools
from setuptools import setup


setup(
    name='pyshadow',
    description='Selenium plugin to manage shadow DOM elements on web page.',
    version='0.0.5',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache License 2",
    author='Sushil Gupta',
    author_email='sushil106768@gmail.com',
    url='https://github.com/sukgu/pyshadow/',
    install_requires=['multipledispatch>=0.6.0', 'selenium>=3.141.0', 'webdriver-manager>=2.5.3'],
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    package_data={
        # And include any *.dat files found in the "data" subdirectory
        # of the "mypkg" package, also:
        "pyshadow": ["resources/test/*", "resources/*"],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
