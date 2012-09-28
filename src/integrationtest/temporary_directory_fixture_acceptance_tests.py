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

from pyassert import assert_that

from pyfix import test, given, run_tests
from pyfix.fixtures import TemporaryDirectoryFixture

@test
@given(temp_dir=TemporaryDirectoryFixture)
def ensure_that_directory_exists(temp_dir):
    assert_that(os.path.exists(temp_dir.basedir)).is_true()
    assert_that(os.path.isdir(temp_dir.basedir)).is_true()


@test
@given(temp_dir=TemporaryDirectoryFixture(prefix="spam", suffix="eggs"))
def ensure_that_directory_contains_prefix_and_suffix(temp_dir):
    assert_that(temp_dir.basedir).contains("spam")
    assert_that(temp_dir.basedir).ends_with("eggs")

if __name__ == "__main__":
    run_tests()
