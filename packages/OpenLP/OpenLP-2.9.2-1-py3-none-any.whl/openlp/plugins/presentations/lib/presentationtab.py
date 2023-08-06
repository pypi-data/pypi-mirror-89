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

from PyQt5 import QtWidgets

from openlp.core.common.i18n import UiStrings, translate
from openlp.core.lib.settingstab import SettingsTab


class PresentationTab(SettingsTab):
    """
    PresentationsTab is the Presentations settings tab in the settings dialog.
    """
    def __init__(self, parent, title, visible_title, controllers, icon_path):
        """
        Constructor
        """
        self.controllers = controllers
        super(PresentationTab, self).__init__(parent, title, visible_title, icon_path)
        self.activated = False

    def setup_ui(self):
        """
        Create the controls for the settings tab
        """
        self.setObjectName('PresentationTab')
        super(PresentationTab, self).setup_ui()
        self.controllers_group_box = QtWidgets.QGroupBox(self.left_column)
        self.controllers_group_box.setObjectName('controllers_group_box')
        self.controllers_layout = QtWidgets.QVBoxLayout(self.controllers_group_box)
        self.controllers_layout.setObjectName('ccontrollers_layout')
        self.presenter_check_boxes = {}
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = QtWidgets.QCheckBox(self.controllers_group_box)
            checkbox.setObjectName(controller.name + 'CheckBox')
            self.presenter_check_boxes[controller.name] = checkbox
            self.controllers_layout.addWidget(checkbox)
        self.left_layout.addWidget(self.controllers_group_box)
        # Advanced
        self.advanced_group_box = QtWidgets.QGroupBox(self.left_column)
        self.advanced_group_box.setObjectName('advanced_group_box')
        self.advanced_layout = QtWidgets.QVBoxLayout(self.advanced_group_box)
        self.advanced_layout.setObjectName('advanced_layout')
        self.override_app_check_box = QtWidgets.QCheckBox(self.advanced_group_box)
        self.override_app_check_box.setObjectName('override_app_check_box')
        self.advanced_layout.addWidget(self.override_app_check_box)
        self.left_layout.addWidget(self.advanced_group_box)
        # PowerPoint
        self.powerpoint_group_box = QtWidgets.QGroupBox(self.left_column)
        self.powerpoint_group_box.setObjectName('powerpoint_group_box')
        self.powerpoint_layout = QtWidgets.QVBoxLayout(self.powerpoint_group_box)
        self.powerpoint_layout.setObjectName('powerpoint_layout')
        self.ppt_slide_click_check_box = QtWidgets.QCheckBox(self.powerpoint_group_box)
        self.ppt_slide_click_check_box.setObjectName('ppt_slide_click_check_box')
        self.powerpoint_layout.addWidget(self.ppt_slide_click_check_box)
        self.ppt_window_check_box = QtWidgets.QCheckBox(self.powerpoint_group_box)
        self.ppt_window_check_box.setObjectName('ppt_window_check_box')
        self.powerpoint_layout.addWidget(self.ppt_window_check_box)
        self.left_layout.addWidget(self.powerpoint_group_box)
        # setup layout
        self.left_layout.addStretch()
        self.right_column.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.right_layout.addStretch()

    def retranslate_ui(self):
        """
        Make any translation changes
        """
        self.controllers_group_box.setTitle(translate('PresentationPlugin.PresentationTab', 'Available Controllers'))
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            self.set_controller_text(checkbox, controller)
        self.advanced_group_box.setTitle(UiStrings().Advanced)
        self.powerpoint_group_box.setTitle(translate('PresentationPlugin.PresentationTab', 'PowerPoint options'))
        self.override_app_check_box.setText(
            translate('PresentationPlugin.PresentationTab', 'Allow presentation application to be overridden'))
        self.ppt_slide_click_check_box.setText(
            translate('PresentationPlugin.PresentationTab',
                      'Clicking on the current slide advances to the next effect'))
        self.ppt_window_check_box.setText(
            translate('PresentationPlugin.PresentationTab',
                      'Let PowerPoint control the size and monitor of the presentations\n'
                      '(This may fix PowerPoint scaling issues in Windows 8 and 10)'))

    def set_controller_text(self, checkbox, controller):
        if checkbox.isEnabled():
            checkbox.setText(controller.display_name)
        else:
            checkbox.setText(translate('PresentationPlugin.PresentationTab',
                                       '{name} (unavailable)').format(name=controller.display_name))

    def load(self):
        """
        Load the settings.
        """
        powerpoint_available = False
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            checkbox.setChecked(self.settings.value('presentations/' + controller.name))
            if controller.name == 'Powerpoint' and controller.is_available():
                powerpoint_available = True
        self.override_app_check_box.setChecked(self.settings.value('presentations/override app'))
        # Load PowerPoint settings
        self.ppt_slide_click_check_box.setChecked(self.settings.value('presentations/powerpoint slide click advance'))
        self.ppt_slide_click_check_box.setEnabled(powerpoint_available)
        self.ppt_window_check_box.setChecked(self.settings.value('presentations/powerpoint control window'))
        self.ppt_window_check_box.setEnabled(powerpoint_available)

    def save(self):
        """
        Save the settings. If the tab hasn't been made visible to the user then there is nothing to do, so exit. This
        removes the need to start presentation applications unnecessarily.
        """
        if not self.activated:
            return
        changed = False
        for key in self.controllers:
            controller = self.controllers[key]
            if controller.is_available():
                checkbox = self.presenter_check_boxes[controller.name]
                setting_key = 'presentations/' + controller.name
                if self.settings.value(setting_key) != checkbox.checkState():
                    changed = True
                    self.settings.setValue(setting_key, checkbox.checkState())
                    if checkbox.isChecked():
                        controller.start_process()
                    else:
                        controller.kill()
        setting_key = 'presentations/override app'
        if self.settings.value(setting_key) != self.override_app_check_box.checkState():
            self.settings.setValue(setting_key, self.override_app_check_box.checkState())
            changed = True
        # Save powerpoint settings
        setting_key = 'presentations/powerpoint slide click advance'
        if self.settings.value(setting_key) != self.ppt_slide_click_check_box.checkState():
            self.settings.setValue(setting_key, self.ppt_slide_click_check_box.checkState())
            changed = True
        setting_key = 'presentations/powerpoint control window'
        if self.settings.value(setting_key) != self.ppt_window_check_box.checkState():
            self.settings.setValue(setting_key, self.ppt_window_check_box.checkState())
            changed = True
        if changed:
            self.settings_form.register_post_process('mediaitem_suffix_reset')
            self.settings_form.register_post_process('mediaitem_presentation_rebuild')
            self.settings_form.register_post_process('mediaitem_suffixes')

    def tab_visible(self):
        """
        Tab has just been made visible to the user
        """
        self.activated = True
        for key in self.controllers:
            controller = self.controllers[key]
            checkbox = self.presenter_check_boxes[controller.name]
            checkbox.setEnabled(controller.is_available())
            self.set_controller_text(checkbox, controller)
