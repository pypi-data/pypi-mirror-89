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
Package to test the openlp.core.ui.firsttimeform package.
"""
import datetime
from unittest.mock import patch

from openlp.core.ui.aboutform import AboutForm


@patch('openlp.core.ui.aboutform.webbrowser')
def test_on_contribute_button_clicked(mocked_webbrowser):
    """
    Test that clicking on the "Volunteer" button opens a web page.
    """
    # GIVEN: A new About dialog and a mocked out webbrowser module
    about_form = AboutForm(None)

    # WHEN: The "Volunteer" button is "clicked"
    about_form.on_contribute_button_clicked()

    # THEN: A web browser is opened
    mocked_webbrowser.open_new.assert_called_with('http://openlp.org/contribute')


@patch('openlp.core.ui.aboutform.get_version')
def test_about_form_build_number(mocked_get_version):
    """
    Test that the build number is added to the about form
    """
    # GIVEN: A mocked out get_version function
    mocked_get_version.return_value = {'version': '3.1.5', 'build': '3000'}

    # WHEN: The about form is created
    about_form = AboutForm(None)

    # THEN: The build number should be in the text
    assert 'OpenLP 3.1.5 build 3000' in about_form.about_text_edit.toPlainText(), \
        "The build number should be set correctly"


def test_about_form_date():
    """
    Test that the copyright date is included correctly
    """
    # GIVEN: A correct application date
    date_string = '2004-{year}'.format(year=datetime.date.today().year)

    # WHEN: The about form is created
    about_form = AboutForm(None)
    about_text = about_form.about_text_edit.toPlainText()

    # THEN: The date should be in the text twice.
    assert about_text.count(date_string, 0) == 1, "The text string should be added twice to the license string"
