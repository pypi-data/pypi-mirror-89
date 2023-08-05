# -*- python -*-
#
# Copyright 2018, 2019, 2020 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class SetUpConfig(object):
    CLASSIFIERS = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database',
        'Topic :: System :: Archiving',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]

    @classmethod
    def getConfig(cls):
        config = {
            'name': 'djfim',
            'author': 'Liang Chen',
            'license': 'Apache License 2.0',
            'classifiers': cls.CLASSIFIERS,
            'keywords': ('Django', 'fixture', 'persistency'),
            'version': cls.find_version('djfim', '__init__.py'),
            'packages': ['djfim', 'djfim.management', 'djfim.management.commands'],
            'platforms': 'Any',
            'python_requires': '>=2.7',
            'install_requires': ['django',], #['django>=3.0',],
            'tests_require': ['flake8', 'pytest'],
            'description': 'Django extension for fixture import and merge',
            'long_description': cls.read_src_file('README.md'),
            'long_description_content_type': 'text/markdown',
        }
        return config

    @staticmethod
    def read_src_file(*parts):
        import codecs
        import os
        dir_path = os.path.abspath(os.path.dirname(__file__))
        with codecs.open(os.path.join(dir_path, *parts), 'r') as _f:
            return _f.read()

    @staticmethod
    def find_version(*file_paths):
        import re

        MSG_VERSION_STRING_NOTFOUND = 'Unable to find version string.'

        version_file = SetUpConfig.read_src_file(*file_paths)
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError(MSG_VERSION_STRING_NOTFOUND)


from setuptools import setup
setup(**(SetUpConfig.getConfig()))

