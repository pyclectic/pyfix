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

__author__ = "Alexander Metzner"

import os

import unittest
from mockito import mock, verify, when, any as any_value
from pyassert import assert_that

from pyfix.fixtures.temporary_directory_fixture import TemporaryDirectoryHandle

class TemporaryDirectoryHandleTest(unittest.TestCase):
    def setUp(self):
        self.handle = TemporaryDirectoryHandle()

    def tearDown(self):
        del self.handle

    def test_should_create_basedir(self):
        assert_that(os.path.exists(self.handle.basedir)).is_true()
        assert_that(os.path.isdir(self.handle.basedir)).is_true()

    def test_should_join_single_element(self):
        assert_that(self.handle.join("spam")).is_equal_to(os.path.join(self.handle.basedir, "spam"))

    def test_should_join_multiple_elements(self):
        assert_that(self.handle.join("spam", "eggs")).is_equal_to(os.path.join(self.handle.basedir, "spam", "eggs"))

    def test_should_touch_file(self):
        self.handle.touch("spam")

        assert_that(os.path.exists(self.handle.join("spam"))).is_true()
        assert_that(os.path.isfile(self.handle.join("spam"))).is_true()

    def test_should_touch_file_in_directory(self):
        self.handle.create_directory("spam")
        self.handle.touch("spam", "eggs")

        assert_that(os.path.exists(self.handle.join("spam", "eggs"))).is_true()
        assert_that(os.path.isfile(self.handle.join("spam", "eggs"))).is_true()

    def test_should_create_file(self):
        self.handle.create_file("spam", "eggs")

        assert_that(os.path.exists(self.handle.join("spam"))).is_true()
        assert_that(os.path.isfile(self.handle.join("spam"))).is_true()

        content = open(self.handle.join("spam")).read()

        assert_that(content).is_equal_to("eggs")

    def test_should_create_directory(self):
        self.handle.create_directory("spam")

        assert_that(os.path.exists(self.handle.join("spam"))).is_true()
        assert_that(os.path.isdir(self.handle.join("spam"))).is_true()

    def test_should_create_directory_with_parents(self):
        self.handle.create_directory("spam", "eggs")

        assert_that(os.path.exists(self.handle.join("spam"))).is_true()
        assert_that(os.path.isdir(self.handle.join("spam"))).is_true()

        assert_that(os.path.exists(self.handle.join("spam", "eggs"))).is_true()
        assert_that(os.path.isdir(self.handle.join("spam", "eggs"))).is_true()

