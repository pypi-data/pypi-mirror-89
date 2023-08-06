"""
Pip.Services Facade
----------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_facade provides reusable primitives to quickly build sophisticated client 
facades via composition of multiple routes and middleware components.

Links
`````

* `website <http://github.com/pip-services-python/>`_
* `development version <http://github.com/pip-services3-python/pip-services3-facade-python>`

"""

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_services3_facade',
    version='3.0.0',
    url='http://github.com/pip-services3-python/pip-services3-facade-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='Facade components for Pip.Services in Python',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601',
        'PyYAML',
        'pystache',
        'pytest',
        'numpy',
        'pytz',
        'bottle',
        'requests',
        'cheroot',
        'beaker',
        'netifaces',
        'pip-services3-commons',
        'pip-services3-components',
        'pip-services3-rpc'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
