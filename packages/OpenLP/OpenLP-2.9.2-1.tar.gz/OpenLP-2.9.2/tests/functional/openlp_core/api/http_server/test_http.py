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
Functional tests to test the Http Server Class.
"""
from unittest.mock import patch

from openlp.core.api.http.server import HttpServer
from openlp.core.common.registry import Registry


@patch('openlp.core.api.http.server.HttpWorker')
@patch('openlp.core.api.http.server.run_thread')
def test_server_start(mocked_run_thread, MockHttpWorker, registry):
    """
    Test the starting of the Waitress Server with the disable flag set off
    """
    # GIVEN: A new httpserver
    # WHEN: I start the server
    Registry().set_flag('no_web_server', False)
    HttpServer()

    # THEN: the api environment should have been created
    assert mocked_run_thread.call_count == 1, 'The qthread should have been called once'
    assert MockHttpWorker.call_count == 1, 'The http thread should have been called once'


@patch('openlp.core.api.http.server.HttpWorker')
@patch('openlp.core.api.http.server.run_thread')
def test_server_start_not_required(mocked_run_thread, MockHttpWorker, registry):
    """
    Test the starting of the Waitress Server with the disable flag set off
    """
    # GIVEN: A new httpserver
    # WHEN: I start the server
    Registry().set_flag('no_web_server', True)
    HttpServer()

    # THEN: the api environment should have been created
    assert mocked_run_thread.call_count == 0, 'The qthread should not have have been called'
    assert MockHttpWorker.call_count == 0, 'The http thread should not have been called'
