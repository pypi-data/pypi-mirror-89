# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='pip_beacons_sample_python',
    version='1.0.4',
    url='https://github.com/pip-services-samples/pip-samples-beacons-python',
    license='MIT',
    description='Sample Beacons microservice in Python',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    long_description=__doc__,
    packages=find_packages(exclude=['config', 'test', 'docker', 'k8s', 'process']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'iso8601',
        'PyYAML',
        'pystache',
        'pytest',
        'pytz',
        'bottle',
        'pybars3',
        'requests',
        'pymongo',
        'netifaces',
        'pip_services3_commons',
        'pip_services3_components',
        'pip_services3_container',
        'pip_services3_data',
        'pip_services3_messaging',
        'pip_services3_mongodb',
        'pip_services3_rpc'
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
