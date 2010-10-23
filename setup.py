import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'django-thumbnailer',
    version = '0.1',
    license = 'GPL',
    description = 'A Django application that currently wraps another '
                  'to produce and deliver thumbnails in parallel to '
                  'avoid the first page load being impossibly slow',
    long_description = read('README'),
    author = 'Stefan Haflidason',
    author_email = 'stefan@stallic.com',

    package_dir = {'': 'src'},
    packages = find_packages('src'),
    include_package_data = True,
    zip_safe = False,

    install_requires = ['setuptools'],
)
