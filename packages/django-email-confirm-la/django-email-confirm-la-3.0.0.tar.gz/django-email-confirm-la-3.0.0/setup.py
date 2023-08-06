#!/usr/bin/env python
# coding: utf-8

import os
import sys

from setuptools import find_packages, setup


if sys.argv[-1] == 'wheel':
    os.system('rm -rf dist/*')
    os.system('pip install wheel')
    os.system('python setup.py bdist_wheel')
    sys.exit(0)

if sys.argv[-1] == 'publish':
    os.system('python setup.py wheel')
    os.system('pip install twine')
    os.system('twine upload dist/*')
    sys.exit(0)

version = __import__('email_confirm_la').get_version()

long_description = ''

license = open('LICENSE').read()

requirements_lines = [line.strip() for line in open('requirements.txt').readlines()]
install_requires = list(filter(None, requirements_lines))

setup(
    name='django-email-confirm-la',
    version=version,
    description='Django email confirmation for any Model and any Field.',
    long_description=long_description,
    keywords=('django', 'email', 'mail', 'confirm', 'confirmation', 'content type'),
    author='Vinta Chen',
    author_email='vinta.chen@gmail.com',
    url='https://github.com/vinta/django-email-confirm-la',
    license=license,
    install_requires=install_requires,
    include_package_data=True,
    packages=find_packages(exclude=['test_project.*', 'test_project']),
    test_suite='run_tests.main',
    zip_safe=False,
    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Email',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ),
)
