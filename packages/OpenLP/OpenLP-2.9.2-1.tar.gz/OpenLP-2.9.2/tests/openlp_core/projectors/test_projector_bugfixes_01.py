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
Package to test the openlp.core.projectors.pjlink base package.
"""


def test_bug_1550891_process_clss_nonstandard_reply_1():
    """
    Bugfix 1550891: CLSS request returns non-standard reply with Optoma/Viewsonic projector
    """
    # Test now part of test_projector_pjlink_commands_01
    # Keeping here for bug reference
    pass


def test_bug_1550891_process_clss_nonstandard_reply_2():
    """
    Bugfix 1550891: CLSS request returns non-standard reply with BenQ projector
    """
    # Test now part of test_projector_pjlink_commands_01
    # Keeping here for bug reference
    pass


def test_bug_1593882_no_pin_authenticated_connection():
    """
    Test bug 1593882 no pin and authenticated request exception
    """
    # Test now part of test_projector_pjlink_commands_02
    # Keeping here for bug reference
    pass


def test_bug_1593883_pjlink_authentication():
    """
    Test bugfix 1593883 pjlink authentication and ticket 92187
    """
    # Test now part of test_projector_pjlink_commands_02
    # Keeping here for bug reference
    pass


def test_bug_1734275_process_lamp_nonstandard_reply():
    """
    Test bugfix 17342785 non-standard LAMP response with one lamp hours only
    """
    # Test now part of test_projector_pjlink_commands_01
    # Keeping here for bug reference
    pass
