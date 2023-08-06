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
Package to test the openlp.core.widgets.widgets package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, call, patch

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.settings import ProxyMode
from openlp.core.display.screens import Screen
from openlp.core.widgets.widgets import ProxyWidget, ProxyDialog, ScreenButton, ScreenSelectionWidget
from tests.helpers.testmixin import TestMixin


def test_radio_button_exclusivity_no_proxy(settings):
    """
    Test that only one radio button can be checked at a time, and that the line edits are only enabled when the
    `manual_proxy_radio` is checked
    """
    # GIVEN: An instance of the `openlp.core.common.widgets.widgets.ProxyWidget` with a radio already checked
    proxy_widget = ProxyWidget()
    proxy_widget.manual_proxy_radio.setChecked(True)

    # WHEN: 'Checking' the `no_proxy_radio` button
    proxy_widget.no_proxy_radio.setChecked(True)

    # THEN: The other radio buttons should not be checked and the line edits should not be enabled
    assert proxy_widget.use_sysem_proxy_radio.isChecked() is False
    assert proxy_widget.manual_proxy_radio.isChecked() is False
    assert proxy_widget.http_edit.isEnabled() is False
    assert proxy_widget.https_edit.isEnabled() is False
    assert proxy_widget.username_edit.isEnabled() is False
    assert proxy_widget.password_edit.isEnabled() is False


def test_radio_button_exclusivity_system_proxy(settings):
    """
    Test that only one radio button can be checked at a time, and that the line edits are only enabled when the
    `manual_proxy_radio` is checked
    """
    # GIVEN: An instance of the `openlp.core.common.widgets.widgets.ProxyWidget` with a radio already checked
    proxy_widget = ProxyWidget()
    proxy_widget.manual_proxy_radio.setChecked(True)

    # WHEN: 'Checking' the `use_sysem_proxy_radio` button
    proxy_widget.use_sysem_proxy_radio.setChecked(True)

    # THEN: The other radio buttons should not be checked and the line edits should not be enabled
    assert proxy_widget.no_proxy_radio.isChecked() is False
    assert proxy_widget.manual_proxy_radio.isChecked() is False
    assert proxy_widget.http_edit.isEnabled() is False
    assert proxy_widget.https_edit.isEnabled() is False
    assert proxy_widget.username_edit.isEnabled() is False
    assert proxy_widget.password_edit.isEnabled() is False


def test_radio_button_exclusivity_manual_proxy(settings):
    """
    Test that only one radio button can be checked at a time, and that the line edits are only enabled when the
    `manual_proxy_radio` is checked
    """
    # GIVEN: An instance of the `openlp.core.common.widgets.widgets.ProxyWidget` with a radio already checked
    proxy_widget = ProxyWidget()
    proxy_widget.no_proxy_radio.setChecked(True)

    # WHEN: 'Checking' the `manual_proxy_radio` button
    proxy_widget.manual_proxy_radio.setChecked(True)

    # THEN: The other radio buttons should not be checked and the line edits should be enabled
    assert proxy_widget.no_proxy_radio.isChecked() is False
    assert proxy_widget.use_sysem_proxy_radio.isChecked() is False
    assert proxy_widget.http_edit.isEnabled() is True
    assert proxy_widget.https_edit.isEnabled() is True
    assert proxy_widget.username_edit.isEnabled() is True
    assert proxy_widget.password_edit.isEnabled() is True


def test_proxy_widget_load_default_settings(settings):
    """
    Test that the default settings are loaded from the config correctly
    """
    # GIVEN: And instance of the widget with default settings
    proxy_widget = ProxyWidget()

    # WHEN: Calling the `load` method
    proxy_widget.load()

    # THEN: The widget should be in its default state
    assert proxy_widget.use_sysem_proxy_radio.isChecked() is True
    assert proxy_widget.http_edit.text() == ''
    assert proxy_widget.https_edit.text() == ''
    assert proxy_widget.username_edit.text() == ''
    assert proxy_widget.password_edit.text() == ''


@patch.object(ProxyWidget, 'load')
def test_proxy_widget_save_no_proxy_settings(proxy_widget_load_patcher, qapp, mock_settings):
    """
    Test that the settings are saved correctly
    """
    # GIVEN: A Mocked settings instance of the proxy widget with some known values set
    proxy_widget = ProxyWidget()
    proxy_widget.no_proxy_radio.setChecked(True)
    proxy_widget.http_edit.setText('')
    proxy_widget.https_edit.setText('')
    proxy_widget.username_edit.setText('')
    proxy_widget.password_edit.setText('')

    # WHEN: Calling save
    proxy_widget.save()

    # THEN: The settings should be set as expected
    mock_settings.setValue.assert_has_calls(
        [call('advanced/proxy mode', ProxyMode.NO_PROXY),
         call('advanced/proxy http', ''),
         call('advanced/proxy https', ''),
         call('advanced/proxy username', ''),
         call('advanced/proxy password', '')])


@patch.object(ProxyWidget, 'load')
def test_proxy_widget_save_manual_settings(proxy_widget_load_patcher, qapp, mock_settings):
    """
    Test that the settings are saved correctly
    """
    # GIVEN: A Mocked and instance of the proxy widget with some known values set
    proxy_widget = ProxyWidget()
    proxy_widget.manual_proxy_radio.setChecked(True)
    proxy_widget.http_edit.setText('http_proxy_server:port')
    proxy_widget.https_edit.setText('https_proxy_server:port')
    proxy_widget.username_edit.setText('username')
    proxy_widget.password_edit.setText('password')

    # WHEN: Calling save
    proxy_widget.save()

    # THEN: The settings should be set as expected
    mock_settings.setValue.assert_has_calls(
        [call('advanced/proxy mode', ProxyMode.MANUAL_PROXY),
         call('advanced/proxy http', 'http_proxy_server:port'),
         call('advanced/proxy https', 'https_proxy_server:port'),
         call('advanced/proxy username', 'username'),
         call('advanced/proxy password', 'password')])


def test_proxy_dialog_init(settings):
    """Test that the ProxyDialog is created successfully"""
    # GIVEN: ProxyDialog class
    # WHEN: It is instantiated
    # THEN: There should be no problems
    ProxyDialog()


def test_proxy_dialog_accept(settings):
    """Test that the accept() method of the ProxyDialog works correctly"""
    # GIVEN: An instance of a ProxyDialog with a mocked out widget
    dlg = ProxyDialog()
    dlg.proxy_widget = MagicMock()

    # WHEN: accept() is called
    dlg.accept()

    # THEN: The save() method on the widget should have been called
    dlg.proxy_widget.save.assert_called_once()


def test_screen_button_initialisation():
    """
    Test the initialisation of the ScreenButton object
    """
    # GIVEN: A mocked screen object
    screen_mock = MagicMock(spec=Screen)
    screen_mock.number = 0
    screen_mock.__str__.return_value = 'Mocked Screen Object'

    # WHEN: initialising the ScreenButton object
    instance = ScreenButton(None, screen_mock)

    # THEN: The ScreenButton should have been initalised correctly with the data from the mocked screen object
    assert isinstance(instance, QtWidgets.QPushButton)
    assert instance.objectName() == 'screen_0_button'
    assert instance.isCheckable() is True
    assert instance.text() == 'Mocked Screen Object'


class TestScreenSelectionWidget(TestCase, TestMixin):

    def setUp(self):
        """Test setup"""
        self.setup_application()
        self.build_settings()

    def tearDown(self):
        """Tear down tests"""
        del self.app

    def test_init_default_args(self):
        """
        Test the initialisation of ScreenSelectionWidget, when initialised with default arguments
        """
        # GIVEN: The ScreenSelectionWidget class
        # WHEN: Initialising ScreenSelectionWidget with default arguments
        with patch('openlp.core.widgets.widgets.QtCore.QTimer') as MockTimer:
            mocked_timer = MagicMock()
            MockTimer.return_value = mocked_timer
            instance = ScreenSelectionWidget()

        # THEN: ScreenSelectionWidget should be an instance of QWidget and the screens attribute should be an empty list
        assert isinstance(instance, QtWidgets.QWidget)
        assert instance.screens == []
        mocked_timer.setSingleShot.assert_called_once_with(True)
        mocked_timer.setInterval.assert_called_once_with(3000)

    def test_init_with_args(self):
        """
        Test the initialisation of ScreenSelectionWidget, when initialised with the screens keyword arg set
        """
        # GIVEN: The ScreenSelectionWidget class
        screens_object_mock = MagicMock()

        # WHEN: Initialising ScreenSelectionWidget with the screens keyword arg set
        with patch('openlp.core.widgets.widgets.QtCore.QTimer') as MockTimer:
            mocked_timer = MagicMock()
            MockTimer.return_value = mocked_timer
            instance = ScreenSelectionWidget(screens=screens_object_mock)

        # THEN: ScreenSelectionWidget should be an instance of QWidget and the screens attribute should the mock used
        assert isinstance(instance, QtWidgets.QWidget)
        assert instance.screens is screens_object_mock
        mocked_timer.setSingleShot.assert_called_once_with(True)
        mocked_timer.setInterval.assert_called_once_with(3000)

    def test_save_screen_none(self):
        """
        Test ScreenSelectionWidget._save_screen when called with the screen arg set as None
        """
        # GIVEN: An instance of the ScreenSelectionWidget
        instance = ScreenSelectionWidget()
        instance.display_group_box = MagicMock(spec=QtWidgets.QGroupBox)

        # WHEN: Calling _save_screen and no screen is selected
        instance._save_screen(None)

        # THEN: _save_screen should return without attempting to write to the screen object
        instance.display_group_box.isChecked.assert_not_called()

    def test_save_screen_not_display(self):
        """
        Test ScreenSelectionWidget._save_screen when the display_group_box is not checked.
        """
        # GIVEN: An instance of the ScreenSelectionWidget, and a mocked group_box
        instance = ScreenSelectionWidget()
        instance.display_group_box = MagicMock(spec=QtWidgets.QGroupBox)
        instance.custom_geometry_button = MagicMock(spec=QtWidgets.QRadioButton, **{'isChecked.return_value': False})
        mocked_screen_object = MagicMock(spec=Screen)
        mocked_screen_object.is_dislpay = True

        # WHEN: display_group_box isn't checked and _save_screen is called with a mocked Screen object.
        instance.display_group_box.isChecked.return_value = False
        instance._save_screen(mocked_screen_object)

        # THEN: _save_screen should should be set to False
        assert mocked_screen_object.is_display is False

    def test_save_screen_display(self):
        """
        Test ScreenSelectionWidget._save_screen when the display_group_box is checked.
        """
        # GIVEN: An instance of the ScreenSelectionWidget, and a mocked group_box
        instance = ScreenSelectionWidget()
        instance.display_group_box = MagicMock(spec=QtWidgets.QGroupBox)
        instance.custom_geometry_button = MagicMock(spec=QtWidgets.QRadioButton, **{'isChecked.return_value': False})
        mocked_screen_object = MagicMock(spec=Screen)

        # WHEN: display_group_box is checked and _save_screen is called with a mocked Screen object.
        instance.display_group_box.isChecked.return_value = True
        instance._save_screen(mocked_screen_object)

        # THEN: _save_screen should should be set to True
        assert mocked_screen_object.is_display is True

    @patch('openlp.core.widgets.widgets.QtCore.QRect')
    def test_save_screen_full_screen(self, mocked_q_rect):
        """
        Test ScreenSelectionWidget._save_screen when the display is set to full screen
        """
        # GIVEN: An instance of the ScreenSelectionWidget, and a mocked custom_geometry_button
        instance = ScreenSelectionWidget()
        instance.display_group_box = MagicMock(spec=QtWidgets.QGroupBox)
        instance.custom_geometry_button = MagicMock(spec=QtWidgets.QRadioButton)
        mocked_screen_object = MagicMock(spec=Screen)

        # WHEN: custom_geometry_button isn't checked and _save_screen is called with a mocked Screen object.
        instance.custom_geometry_button.isChecked.return_value = False
        instance._save_screen(mocked_screen_object)

        # THEN: _save_screen should not attempt to save a custom geometry
        mocked_q_rect.assert_not_called()

    @patch('openlp.core.widgets.widgets.QtCore.QRect')
    def test_save_screen_custom_geometry(self, mocked_q_rect):
        """
        Test ScreenSelectionWidget._save_screen when a custom geometry is set
        """
        # GIVEN: An instance of the ScreenSelectionWidget, and a mocked custom_geometry_button
        instance = ScreenSelectionWidget()
        instance.display_group_box = MagicMock(spec=QtWidgets.QGroupBox)
        instance.custom_geometry_button = MagicMock(spec=QtWidgets.QRadioButton)
        instance.left_spin_box = MagicMock(spec=QtWidgets.QSpinBox, **{'value.return_value': 100})
        instance.top_spin_box = MagicMock(spec=QtWidgets.QSpinBox, **{'value.return_value': 200})
        instance.width_spin_box = MagicMock(spec=QtWidgets.QSpinBox, **{'value.return_value': 300})
        instance.height_spin_box = MagicMock(spec=QtWidgets.QSpinBox, **{'value.return_value': 400})
        mocked_screen_object = MagicMock(spec=Screen)

        # WHEN: custom_geometry_button is checked and _save_screen is called with a mocked Screen object.
        instance.custom_geometry_button.isChecked.return_value = True
        instance._save_screen(mocked_screen_object)

        # THEN: _save_screen should save the custom geometry
        mocked_q_rect.assert_called_once_with(100, 200, 300, 400)

    def test_setup_spin_box(self):
        """
        Test that ScreenSelectionWidget._setup_spin_box sets up the given spinbox correctly
        """
        # GIVEN: An instance of the ScreenSelectionWidget class and a mocked spin box object
        instance = ScreenSelectionWidget()
        spin_box_mock = MagicMock(spec=QtWidgets.QSpinBox)

        # WHEN: Calling _setup_spin_box with the mocked spin box object and some sample values
        instance._setup_spin_box(spin_box_mock, 0, 100, 50)

        # THEN: The mocked spin box object should have been set up with the specified values
        spin_box_mock.setMinimum.assert_called_once_with(0)
        spin_box_mock.setMaximum.assert_called_once_with(100)
        spin_box_mock.setValue.assert_called_once_with(50)

    def test_load(self):
        """
        Test that ScreenSelectionWidget.load() loads the screens correctly
        """
        # GIVEN: An instance of the ScreenSelectionWidget and a whole bunch o' mocks
        instance = ScreenSelectionWidget()
        mocked_widget = MagicMock()
        mocked_item = MagicMock()
        mocked_item.widget.return_value = mocked_widget
        mocked_screen_frame_layout = MagicMock()
        mocked_screen_frame_layout.count.side_effect = [1, 0]
        mocked_screen_frame_layout.takeAt.return_value = mocked_item
        mocked_screen_button_group = MagicMock()
        mocked_screen_button_group.buttons.return_value = [mocked_widget]
        instance.screen_frame_layout = mocked_screen_frame_layout
        instance.screen_button_group = mocked_screen_button_group
        instance.screens = [Screen(number=0)]

        # WHEN: load() is called
        with patch('openlp.core.widgets.widgets.ScreenButton'):
            instance.load()

        # THEN: The mocks should have been called
        mocked_widget.setParent.assert_called_once_with(None)
        mocked_widget.deleteLater.assert_called_once()
        mocked_screen_button_group.removeButton.assert_called_once_with(mocked_widget)

    def test_on_identify_timer_shot(self):
        """
        Test that the _on_identify_timer_shot() method removes the labels from the screens
        """
        # GIVEN: A ScreenSelectionWidget and a bunch o' mocks
        instance = ScreenSelectionWidget()
        mocked_label = MagicMock()
        instance.identify_labels = [mocked_label]

        # WHEN: _on_identify_timer_shot() is called
        instance._on_identify_timer_shot()

        # THEN: The labels should be cleared
        mocked_label.hide.assert_called_once()
        mocked_label.setParent.assert_called_once_with(None)
        mocked_label.deleteLater.assert_called_once()
        assert instance.identify_labels == []

    def test_on_identify_button_clicked(self):
        """
        Test that the on_identify_button_clicked() method shows a label on each screen
        """
        # GIVEN: A ScreenSelectionWidget and a bunch o' mocks
        instance = ScreenSelectionWidget()
        mocked_screen = MagicMock()
        mocked_screen.geometry.x.return_value = 0
        mocked_screen.geometry.y.return_value = 0
        mocked_screen.geometry.width.return_value = 1920
        mocked_screen.__str__.return_value = 'Screen 1'
        instance.screens = [mocked_screen]
        instance.timer = MagicMock()

        # WHEN: on_identify_button_clicked() is called
        with patch('openlp.core.widgets.widgets.QtWidgets.QLabel') as MockLabel:
            mocked_label = MagicMock()
            MockLabel.return_value = mocked_label
            instance.on_identify_button_clicked()

        # THEN: The labels should be cleared
        MockLabel.assert_called_once_with(None)
        mocked_label.setAlignment.assert_called_once_with(QtCore.Qt.AlignCenter)
        mocked_label.setText.assert_called_once_with('Screen 1')
        mocked_label.setStyleSheet.assert_called_once_with('font-size: 24pt; font-weight: bold; '
                                                           'background-color: #0C0; color: #000; '
                                                           'border: 5px solid #000;')
        mocked_label.setGeometry.assert_called_once_with(QtCore.QRect(0, 0, 1920, 100))
        mocked_label.setWindowFlags.assert_called_once_with(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool |
                                                            QtCore.Qt.WindowStaysOnTopHint |
                                                            QtCore.Qt.WindowDoesNotAcceptFocus)
        mocked_label.show.assert_called_once()
        assert instance.identify_labels == [mocked_label]
        instance.timer.start.assert_called_once()

    def test_on_display_clicked_with_checked(self):
        """
        Test that the on_display_clicked() sets the first screen as display when the checkbx is checked
        """
        # GIVEN: A ScreenSelectionWidget and a bunch o' mocks
        instance = ScreenSelectionWidget()
        mocked_screen_1 = MagicMock()
        mocked_screen_2 = MagicMock()
        mocked_screen_2.is_display = True
        instance.screens = [mocked_screen_1, mocked_screen_2]
        instance.current_screen = mocked_screen_1

        # WHEN: on_display_clicked() is called when the checkbox is checked
        instance.on_display_clicked(True)

        # THEN: The first screen should be marked as a display
        assert mocked_screen_1.is_display is True
        assert mocked_screen_2.is_display is False

    def test_on_display_clicked_with_unchecked(self):
        """
        Test that the on_display_clicked() disallows the checkbox to be unchecked
        """
        # GIVEN: A ScreenSelectionWidget and a bunch o' mocks
        instance = ScreenSelectionWidget()
        mocked_screen_1 = MagicMock()
        mocked_screen_2 = MagicMock()
        mocked_screen_2.is_display = True
        instance.screens = [mocked_screen_1, mocked_screen_2]
        instance.current_screen = mocked_screen_2

        # WHEN: on_display_clicked() is called when the checkbox is checked
        with patch('openlp.core.widgets.widgets.translate') as mocked_translate, \
                patch('openlp.core.widgets.widgets.critical_error_message_box') as mocked_error:
            mocked_translate.side_effect = lambda c, s: s
            instance.on_display_clicked(False)

        # THEN: The first screen should be marked as a display
        mocked_error.assert_called_once_with('Select a Display',
                                             'You need to select at least one screen to be used as a display. '
                                             'Select the screen you wish to use as a display, and check the '
                                             'checkbox for that screen.', parent=instance, question=False)
        assert instance.use_screen_check_box.isChecked() is True
        assert instance.display_group_box.isChecked() is True


def test_screen_selection_save(mock_settings):
    """
    Test that the save() method saves the screens
    """
    # GIVEN: A ScreenSelectionWidget and a bunch o' mocks
    mocked_screen = MagicMock(**{'number': 0, 'to_dict.return_value': {'number': 0}})
    instance = ScreenSelectionWidget()
    instance._save_screen = MagicMock()
    instance.screens = [mocked_screen]
    instance.current_screen = mocked_screen

    instance.save()

    # THEN: The right things should happen
    instance._save_screen.assert_called_once_with(mocked_screen)
    mocked_screen.to_dict.assert_called_once()
    mock_settings.setValue.assert_called_once_with('core/screens', {0: {'number': 0}})
