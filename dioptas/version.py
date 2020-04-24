# -*- coding: utf-8 -*-
# Dioptas - GUI program for fast processing of 2D X-ray diffraction data
# Principal author: Clemens Prescher (clemens.prescher@gmail.com)
# Copyright (C) 2014-2019 GSECARS, University of Chicago, USA
# Copyright (C) 2015-2018 Institute for Geology and Mineralogy, University of Cologne, Germany
# Copyright (C) 2019-2020 DESY, Hamburg, Germany
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from ._version import get_versions as _get_version

def get_version():
    """
    Uses the versioneer code to generate a version string based on the last git tag and subsequent commits afterwards.
    For packaging reasons, this version string will also be saved in a file called __version__. This ensure, that the
    frozen version can also be used in the executables produced by pyinstaller
    :return:
    """
    version = _get_version()['version']
    dir_path = os.path.dirname(os.path.realpath(__file__))
    if version == "0+unknown":
        try:
            with open(os.path.join(dir_path, '__version__'), 'r') as fp:
                version = fp.readline()
        except ImportError:
            version = "0.5.0"
    else:
        # trying to freeze the current version into a python file which gets loaded in case it is not accessible
        with open(os.path.join(dir_path, '__version__'), 'w+') as fp:
            fp.write(version)

    return version