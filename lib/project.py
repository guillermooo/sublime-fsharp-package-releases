# Copyright (c) 2014, Guillermo López-Anglada. Please see the AUTHORS file for details.
# All rights reserved. Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.)

import os

from FSharp.sublime_plugin_lib.path import find_file_by_extension
from FSharp.sublime_plugin_lib.path import extension_equals


def find_fsproject(start):
    """
    Find a .fsproject file starting at @start path.

    Returns the path to the file or `None` if not found.
    """

    return find_file_by_extension(start, 'fsproj')


class FileInfo(object):
    """
    Inspects a file for interesting properties from the plugin's POV.
    """

    def __init__(self, view_or_fname):
        """
        @view_or_fname
          A Sublime Text view or a file name.
        """
        assert view_or_fname, 'wrong arg: %s' % view_or_fname
        self.view_or_fname = view_or_fname

    def __str__(self):
        return self.path

    @property
    def path(self):
        try:
            # The returned path can be None, for example, if the view is unsaved.
            return self.view_or_fname.file_name()
        except AttributeError:
            return self.view_or_fname

    @property
    def is_fsharp_file(self):
        return any((self.is_fsharp_code_file,
                   self.is_fsharp_script_file,
                   self.is_fsharp_project_file))

    @property
    def is_fsharp_code(self):
        '''
        Returns `True` if `self` is any sort of F# code file.
        '''
        return (self.is_fsharp_code_file or self.is_fsharp_script_file)

    @property
    def is_fsharp_code_file(self):
        '''
        Returns `True` if `self` is a .fs file.
        '''
        return self.path and extension_equals(self.path, '.fs')

    @property
    def is_fsharp_script_file(self):
        '''
        Returns `True` if `self` is a .fsx/.fsi/.fsscript file.
        '''
        return self.path and (extension_equals(self.path, '.fsx')
                or extension_equals(self.path, '.fsscript'))

    @property
    def is_fsharp_project_file(self):
        return self.path and extension_equals(self.path, '.fsproj')


class FSharpProjectFile(object):
    def __init__(self, path):
        assert path.endswith('.fsproj'), 'wrong fsproject path: %s' % path
        self.path = path
        self.parent = os.path.dirname(self.path)

    def __eq__(self, other):
        # todo: improve comparison
        return os.path.normpath(self.path) == os.path.normpath(other.path)

    def governs(self, fname):
        return fname.startswith(self.parent)

    @classmethod
    def from_path(cls, path):
        '''
        @path
          A path to a file or directory.
        '''
        fs_project = find_fsproject(path)
        if not fs_project:
            return None
        return FSharpProjectFile(fs_project)
