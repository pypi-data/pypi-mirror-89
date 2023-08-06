# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2020 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
"""
Functional tests to test the AppLocation class and related methods.
"""

from openlp.core.common import is_not_image_file
from tests.utils.constants import RESOURCE_PATH


def test_is_not_image_empty():
    """
    Test the method handles an empty string
    """
    # Given and empty string
    file_name = ""

    # WHEN testing for it
    result = is_not_image_file(file_name)

    # THEN the result is false
    assert result is True, 'The missing file test should return True'


def test_is_not_image_with_image_file():
    """
    Test the method handles an image file
    """
    # Given and empty string
    file_path = RESOURCE_PATH / 'church.jpg'

    # WHEN testing for it
    result = is_not_image_file(file_path)

    # THEN the result is false
    assert result is False, 'The file is present so the test should return False'


def test_is_not_image_with_none_image_file():
    """
    Test the method handles a non image file
    """
    # Given and empty string
    file_path = RESOURCE_PATH / 'presentations' / 'test.ppt'

    # WHEN testing for it
    result = is_not_image_file(file_path)

    # THEN the result is false
    assert result is True, 'The file is not an image file so the test should return True'
