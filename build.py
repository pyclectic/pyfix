#  pyfix
#  Copyright 2012 The pyfix team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
pyfix
-----

pyfix is a framework for writing and executing automated tests including unittests, integration tests or acceptance
tests. pyfix provides capabilities similar to other tools (such as unittest) but does not follow the xUnit semantics
to write tests.

pyfix Principals
````````````````

pyfix aims to make tests easy to read and understand while it encourages the use of accepted software design principles
such as favor composition over inheritance. pyfix also tries to reduce the amount of syntactic "waste" that some other
frameworks suffer from (i.e. putting self in front of almost everything).

Links
`````
* pyfix Github repository <https://github.com/pyclectic/pyfix>
"""

from pythonbuilder.core import init, use_plugin, Author

use_plugin("filter_resources")

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.integrationtest")
use_plugin("python.coverage")
use_plugin("python.pychecker")
use_plugin("python.distutils")

use_plugin("python.install_dependencies")

default_task = ["analyze", "publish"]

version = "0.2.0"
summary = "A framework for writing automated software tests (non xUnit based)"
description = __doc__
authors = (Author("Alexander Metzner", "halimath.wilanthaou@gmail.com"),)
url = "https://github.com/pyclectic/pyfix"
license = "Apache Software License"

@init
def init (project):
    project.build_depends_on("mockito")
    project.depends_on("pyassert")

    project.get_property("filter_resources_glob").append("**/pyfix/__init__.py")

    project.set_property("dir_source_unittest_python", "src/unittest")
    project.set_property("dir_source_integrationtest_python", "src/integrationtest")

    project.set_property("pychecker_break_build", True)
    project.set_property("pychecker_break_build_threshold", 1)
    
    project.set_property("coverage_threshold_warn", 85)
    project.set_property("coverage_break_build", False)
    project.get_property("coverage_exceptions").append("pyfix.cli")

    project.get_property("distutils_commands").append("bdist_egg")
    project.set_property("distutils_classifiers", [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing'])
