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
import tempfile
import shutil

from pyfix import Fixture

# Python 3 compatibility
try:
    unicode
except NameError:
    basestring = unicode = str

class TemporaryDirectoryHandle(object):
    """
    Handle for working in a temporary directory.

    Each instance of this handle creates a new and empty temporary directory (basedir)
    which can be used to add files and sub-directories for filesystem testing.

    Upon deletion the temporary directory and all its children are removed.
    """

    def __init__(self, prefix=None, suffix=None):
        if prefix is None:
            prefix = __name__
        if suffix is None:
            suffix = ""
        self.basedir = tempfile.mkdtemp(prefix=prefix, suffix=suffix)

    def __del__(self):
        if os.path.exists(self.basedir):
            shutil.rmtree(self.basedir)

    def join(self, *path_elements):
        "Convenience method for os.path.join-ing the basedir with all given elements"
        path_elements = [self.basedir] + list(path_elements)
        return os.path.join(*path_elements)

    def touch(self, *path_elements):
        "Touches the named file inside the basedir."
        f = open(self.join(*path_elements), "w")
        try:
            f.write("")
        finally:
            f.close()

    def create_directory(self, *path_elements):
        "Creates the directory and all its intermediate parents inside the basedir"
        os.makedirs(self.join(*path_elements))

    def create_file(self, name_parts, content, binary=False):
        "Creates a file inside the basedir using the given content."
        if isinstance(name_parts, basestring):
            name_parts = [name_parts]
        open_flags = "w" + ("b" if binary else "")

        with open(self.join(*name_parts), open_flags) as f:
            f.write(content)


class TemporaryDirectoryFixture(Fixture):
    """
    Fixture that creates/ deletes a TempDirHandle.
    """

    def __init__(self, prefix=None, suffix=None):
        self._prefix = prefix
        self._suffix = suffix

    def reclaim(self, temp_dir_handle):
        del temp_dir_handle

    def provide(self):
        return [TemporaryDirectoryHandle(self._prefix, self._suffix)]
