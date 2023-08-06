#!/usr/bin/env python

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()


setup(
    name='myquerytutor',
    version='2.1.1',
    license='LGPL-3.0-or-later',
    description='Educational tool to teach SQL',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Steven Tucker',
    author_email='tuxta2@gmail.com',
    url='https://gitlab.com/tuxta/myquerytutor',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
    ],
    project_urls={
        'Changelog': 'https://gitlab.com/tuxta/myquerytutor/blob/master/CHANGELOG.rst',
        'Issue Tracker': 'https://gitlab.com/tuxta/myquerytutor/issues',
    },
    keywords=[
    ],
    python_requires='>=3.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
    install_requires=[
        'PyQt5>=5.13.1', 'PyQtWebEngine>=5.13.2', 'beautifulsoup4>=4.8.2', 'requests>=2.20.1',
    ],
    extras_require={
    },
    entry_points={
        'console_scripts': [
            'myquerytutor = myquerytutor.cli:main',
        ]
    },
)
