# Copyright 2020 Peter Bencze
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="silene",
    version="1.0.0",
    description="Silene is an open source web crawler framework built upon Pyppeteer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peterbencze/silene",
    author="Peter Bencze",
    author_email="benczepeter95@gmail.com",
    license="Apache License, Version 2.0",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="crawler scraper spider framework pyppeteer data",
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.7",
    install_requires=[
        "appdirs==1.4.4",
        "pyee==7.0.4",
        "pyppeteer==0.2.2",
        "syncer==1.3.0",
        "tld==0.12.3",
        "tqdm==4.54.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_full_version < '4.0.0'",
        "websockets==8.1; python_full_version >= '3.6.1'",
    ],
    extras_require={
        "dev": [
            "appdirs==1.4.4",
            "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "black==19.10b0; python_version >= '3.6'",
            "cached-property==1.5.2",
            "cerberus==1.3.2",
            "certifi==2020.12.5",
            "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "coverage==5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
            "distlib==0.3.1",
            "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "importlib-metadata==3.3.0; python_version < '3.8'",
            "iniconfig==1.1.1",
            "orderedmultidict==1.0.1",
            "packaging==20.8; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pathspec==0.8.1",
            "pep517==0.9.1",
            "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "pipenv-setup==3.1.1",
            "pipfile==0.0.2",
            "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pluggy==0.13.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "py==1.10.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "pytest==6.1.2",
            "pytest-cov==2.10.1",
            "pytest-httpserver==0.3.6",
            "pytest-mock==3.3.1",
            "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "regex==2020.11.13",
            "requests==2.25.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "requirementslib==1.5.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "typed-ast==1.4.1",
            "typing-extensions==3.7.4.3; python_version < '3.8'",
            "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_full_version < '4.0.0'",
            "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
            "werkzeug==1.0.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "wheel==0.36.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
            "zipp==3.4.0; python_version < '3.8'",
        ]
    },
    dependency_links=[],
    project_urls={
        "Bug Reports": "https://github.com/peterbencze/silene/issues",
        "Funding": "https://www.paypal.com/paypalme/peterbencze",
        "Source": "https://github.com/peterbencze/silene",
    },
)
