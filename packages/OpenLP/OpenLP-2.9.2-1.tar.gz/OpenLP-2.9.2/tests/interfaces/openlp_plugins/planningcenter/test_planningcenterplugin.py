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
Package to test the openlp.plugins.planningcenter.planningcenterplugin package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from PyQt5 import QtWidgets

from openlp.core.common.registry import Registry
from openlp.core.common.settings import Settings
from openlp.core.state import State
from openlp.core.ui.icons import UiIcons
from openlp.core.ui.settingsform import SettingsForm
from openlp.plugins.planningcenter.planningcenterplugin import PlanningCenterPlugin
from tests.helpers.testmixin import TestMixin


class TestPlanningCenterPlugin(TestCase, TestMixin):
    """
    Test the PlanningcenterPlugin class
    """
    def setUp(self):
        """
        Create the UI
        """
        self.setup_application()
        self.registry = Registry()
        Registry.create()
        State().load_settings()
        Registry().register('settings', Settings())
        self.plugin = PlanningCenterPlugin()
        self.settings_form = SettingsForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.registry
        del self.plugin
        del self.settings_form

    def test_class_init_defaults(self):
        """
        Test that the plugin class is instantiated with the correct defaults
        """
        # GIVEN: A PlanningcenterPlugin Class
        # WHEN:  the class has been through __init__
        # THEN:
        # planningcenter form is set to None
        self.assertEqual(self.plugin.planningcenter_form, None, "Init plugin set to None")
        # icon is set correctly
        self.assertEqual(self.plugin.icon, UiIcons().planning_center, "Init icon set to planning_center icon")
        # weight is -1
        self.assertEqual(self.plugin.weight, -1, "Init weight set to -1")
        # the planning_center module is registered active
        self.assertEqual(State().is_module_active('planning_center'), True, "Init State() is active")

    def test_initialise(self):
        """
        Test that the initialise function can be called and it passes a call along
        to its parent class
        """
        # GIVEN: A PlanningcenterPlugin Class
        # WHEN:  initialise has been called on the class
        with patch('openlp.plugins.planningcenter.planningcenterplugin.PlanningCenterPlugin.import_planning_center',
                   create=True):
            return_value = self.plugin.initialise()
        # THEN:
        # the function returns and does not fail... it doesn't do much at this point, so this
        # is mainly to improve test coverage
        self.assertEqual(return_value, None, "Initialise was called on the class and it didn't crash")

    def test_import_menu_item_added(self):
        """
        Test that the add_import_menu_item function adds the menu item
        """
        # GIVEN: A PlanningcenterPlugin Class
        # WHEN:  add_import_menu_item is called
        import_menu = QtWidgets.QMenu()
        self.plugin.add_import_menu_item(import_menu)
        self.plugin.import_planning_center.setVisible(True)
        # THEN:
        # the menu should not be empty
        self.assertEqual(import_menu.isEmpty(), False, "Menu Item is populated")

    @patch('openlp.plugins.planningcenter.forms.selectplanform.SelectPlanForm.exec')
    @patch('openlp.core.ui.settingsform.SettingsForm.exec')
    def test_on_import_planning_center_triggered_with_auth_settings(self, mock_editauth_exec, mock_selectplan_exec):
        """
        Test that the on_import_planning_center_triggered function correctly returns
        the correct form to display.
        """
        # GIVEN: A PlanningCenterPlugin Class with mocked exec calls on both
        # PlanningCenter forms and settings set
        application_id = 'abc'
        secret = '123'
        Settings().setValue('planningcenter/application_id', application_id)
        Settings().setValue('planningcenter/secret', secret)
        # init the planning center plugin so we have default values defined for Settings()
        # WHEN:  on_import_planning_center_triggered is called
        self.plugin.on_import_planning_center_triggered()
        # THEN:
        self.assertEqual(mock_selectplan_exec.call_count, 1, "Select Plan Form was shown")
        self.assertEqual(mock_editauth_exec.call_count, 0, "Edit Auth Form was not shown")

    @patch('openlp.plugins.planningcenter.forms.selectplanform.SelectPlanForm.exec')
    @patch('openlp.core.ui.settingsform.SettingsForm.exec')
    def test_on_import_planning_center_triggered_without_auth_settings(self, mock_editauth_exec, mock_selectplan_exec):
        """
        Test that the on_import_planning_center_triggered function correctly returns
        the correct form to display.
        """
        # GIVEN: A PlanningCenterPlugin Class with mocked exec calls on both
        # PlanningCenter forms and settings set
        application_id = ''
        secret = ''
        Settings().setValue('planningcenter/application_id', application_id)
        Settings().setValue('planningcenter/secret', secret)
        # init the planning center plugin so we have default values defined for Settings()
        # WHEN:  on_import_planning_center_triggered is called
        self.plugin.on_import_planning_center_triggered()
        # THEN:
        self.assertEqual(mock_selectplan_exec.call_count, 0, "Select Plan Form was not shown")
        self.assertEqual(mock_editauth_exec.call_count, 1, "Edit Auth Form was shown")

    def test_about(self):
        """
        Test that the about function returns text.
        """
        # GIVEN: A PlanningCenterPlugin Class
        # WHEN:  about() is called
        return_value = self.plugin.about()
        # THEN:
        self.assertGreater(len(return_value), 0, "About function returned some text")

    def test_finalise(self):
        """
        Test that the finalise function cleans up after the plugin
        """
        # GIVEN: A PlanningcenterPlugin Class with a bunch of mocks
        self.plugin.import_planning_center = MagicMock()

        # WHEN: finalise has been called on the class
        self.plugin.finalise()

        # THEN: it cleans up after itself
        self.plugin.import_planning_center.setVisible.assert_called_once_with(False)
