# Copyright (c) 2020, Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import os
import unittest
from unittest import mock

from sf2cf import sf2cf


class TestUtils(unittest.TestCase):
    def test_default_config_file(self):
        def fake_expanduser(path):
            return path.replace('~', '/home/user')

        with mock.patch.dict(os.environ, {}), \
             mock.patch('os.path.expanduser', side_effect=fake_expanduser):
            self.assertEqual(sf2cf.default_config_file(),
                             '/home/user/.config/sf2cf/config')

        with mock.patch.dict(os.environ, {'XDG_CONFIG_HOME': '/foo/bar'}):
            self.assertEqual(sf2cf.default_config_file(),
                             '/foo/bar/sf2cf/config')
