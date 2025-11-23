# Copyright 2018-2022 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from typing import List

import setuptools


def find_version(*file_path_parts: str) -> str:
    """Get version from kfp.__init__.__version__."""

    file_path = os.path.join(os.path.dirname(__file__), *file_path_parts)
    with open(file_path, 'r') as f:
        version_file_text = f.read()

    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file_text,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError(f'Unable to find version string in file: {file_path}.')


def read_readme() -> str:
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    with open(readme_path) as f:
        return f.read()


_version = find_version('kfp', 'version.py')

# Dependencies
INSTALL_REQUIRES = [
    "click>=8.1.8",
    "click-option-group==0.5.7",
    "docstring-parser>=0.7.3,<1",
    "google-api-core>=1.31.5,<3.0.0dev,!=2.0.*,!=2.1.*,!=2.2.*,!=2.3.0",
    "google-auth>=1.6.1,<3",
    "google-cloud-storage>=2.2.1,<4",
    "certifi",
    "python-dateutil",
    "six>=1.10",
    "kubernetes>=8.0.0,<31",
    "protobuf>=6.31.1,<7.0",
    "PyYAML>=5.3,<7",
    "requests-toolbelt>=0.8.0,<2",
    "tabulate>=0.8.6,<1",
    "urllib3<3.0.0",
    "typing-extensions>=3.7.4,<5; python_version<'3.9'",
    "absl-py>=0.9,<2",
    "cloudpickle>=2.0.0,<3",
    "Deprecated>=1.2.7,<2",
    "fire>=0.3.1,<1",
    "jsonschema>=3.0.1,<4",
    "strip-hints>=0.1.8,<1",
    "uritemplate>=3.0.1,<4",
    "typer>=0.3.2,<1.0",
]

EXTRAS_REQUIRE = {
    'docker': ['docker'],
    'notebooks': [
        "nbclient>=0.10,<1",
        "ipykernel>=6,<7",
        "jupyter_client>=7,<9",
    ],
    'kubernetes': [],
    'dev': [
        "absl-py==1.4.0",
        "docformatter==1.4",
        "docker==5.0.3",
        "isort==5.10.1",
        "mypy==0.941",
        "nbformat==5.10.4",
        "pip-tools==6.0.0",
        "pre-commit==2.19.0",
        "pycln==2.1.1",
        "pylint==2.17.7",
        "pytest==7.1.2",
        "pytest-cov==3.0.0",
        "pytest-xdist==2.5.0",
        "types-protobuf==3.19.15",
        "types-PyYAML==6.0.5",
        "types-requests==2.27.14",
        "types-tabulate==0.8.6",
        "yapf==0.43.0",
    ]
}
EXTRAS_REQUIRE['all'] = EXTRAS_REQUIRE['docker'] + EXTRAS_REQUIRE['notebooks'] + EXTRAS_REQUIRE['kubernetes']

setuptools.setup(
    name='kfp',
    version=_version,
    description='Kubeflow Pipelines SDK',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='The Kubeflow Authors',
    url='https://github.com/kubeflow/pipelines',
    project_urls={
        'Documentation':
            'https://kubeflow-pipelines.readthedocs.io/en/stable/',
        'Bug Tracker':
            'https://github.com/kubeflow/pipelines/issues',
        'Source':
            'https://github.com/kubeflow/pipelines/tree/master/sdk',
        'Changelog':
            'https://github.com/kubeflow/pipelines/blob/master/sdk/RELEASE.md',
    },
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    packages=setuptools.find_packages(exclude=['*test*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.9.0',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'dsl-compile = kfp.cli.compile_:main',
            'kfp=kfp.cli.__main__:main',
        ]
    })
