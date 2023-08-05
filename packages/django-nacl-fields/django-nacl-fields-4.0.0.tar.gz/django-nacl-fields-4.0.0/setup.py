import os
import re
import codecs
from setuptools import find_packages, setup


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-nacl-fields',
    version=find_version('nacl_encrypted_fields', '__init__.py'),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'Django>=2.2',
        'PyNaCl>=1.4.0',
    ],
    extras_require={
        'test': [
            'psycopg2-binary',
        ],
        'lint': [
            'flake8',
        ],
        'docs': [
            'sphinx',
        ]
    },
    license='Apache License',
    description=(
        'This is a collection of Django Model Field classes that are encrypted'
        ' using PyNaCl.'
    ),
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/warpnet/django-nacl-fields',
    author='Warpnet B.V.',
    author_email='info@warpnet.nl',
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
