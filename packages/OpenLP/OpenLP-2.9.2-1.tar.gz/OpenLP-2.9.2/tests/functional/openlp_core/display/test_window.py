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
Package to test the openlp.core.display.window package.
"""
import sys
import time
import pytest

from unittest.mock import MagicMock, patch

from PyQt5 import QtCore

# Mock QtWebEngineWidgets
sys.modules['PyQt5.QtWebEngineWidgets'] = MagicMock()

from openlp.core.display.window import DisplayWindow, DisplayWatcher
from openlp.core.common.enum import ServiceItemType
from openlp.core.lib.theme import Theme
from openlp.core.ui import HideMode


@pytest.fixture
def mock_geometry():
    mocked_screen = MagicMock()
    mocked_screen.display_geometry = QtCore.QRect(10, 20, 400, 600)
    mocked_screenlist = MagicMock()
    mocked_screenlist.current = mocked_screen
    screenlist_patcher = patch('openlp.core.lib.theme.ScreenList', return_value=mocked_screenlist)
    screenlist_patcher.start()
    yield
    screenlist_patcher.stop()


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_x11_override_on(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test that the x11 override option bit is set
    """
    # GIVEN: x11 bypass is on
    mock_settings.value.return_value = True

    # WHEN: A DisplayWindow is generated
    display_window = DisplayWindow()

    # THEN: The x11 override flag should be set
    x11_bit = display_window.windowFlags() & QtCore.Qt.X11BypassWindowManagerHint
    assert x11_bit == QtCore.Qt.X11BypassWindowManagerHint


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_x11_override_off(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test that the x11 override option bit is not set when setting if off
    """
    # GIVEN: x11 bypass is off
    mock_settings.value.return_value = False

    # WHEN: A DisplayWindow is generated
    display_window = DisplayWindow()

    # THEN: The x11 override flag should not be set
    x11_bit = display_window.windowFlags() & QtCore.Qt.X11BypassWindowManagerHint
    assert x11_bit != QtCore.Qt.X11BypassWindowManagerHint


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
def test_set_scale_not_initialised(mocked_addWidget, mock_settings):
    """
    Test that the scale js is not run if the page is not initialised
    """
    # GIVEN: A display window not yet initialised
    display_window = DisplayWindow()
    display_window._is_initialised = False
    display_window.run_javascript = MagicMock()

    # WHEN: set scale is run
    display_window.set_scale(0.5)

    # THEN: javascript should not be run
    display_window.run_javascript.assert_not_called()


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_set_scale_initialised(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test that the scale js is not run if the page is not initialised
    """
    # GIVEN: A display window not yet initialised
    display_window = DisplayWindow()
    display_window._is_initialised = True
    display_window.run_javascript = MagicMock()

    # WHEN: set scale is run
    display_window.set_scale(0.5)

    # THEN: javascript should not be run
    display_window.run_javascript.assert_called_once_with('Display.setScale(50.0);')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_after_loaded(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test the correct steps are taken when the webview is loaded
    """
    # GIVEN: An initialised display window and settings for item transitions and hide mouse returns true
    display_window = DisplayWindow()
    display_window.is_display = True
    mock_settings.value.return_value = True
    display_window.scale = 2
    display_window._is_initialised = True
    display_window.run_javascript = MagicMock()
    display_window.set_scale = MagicMock()
    display_window.set_startup_screen = MagicMock()

    # WHEN: after_loaded is run
    display_window.after_loaded()

    # THEN: The following functions should have been called
    display_window.run_javascript.assert_called_once_with('Display.init({'
                                                          'isDisplay: true,'
                                                          'doItemTransitions: true,'
                                                          'hideMouse: true'
                                                          '});')
    display_window.set_scale.assert_called_once_with(2)
    display_window.set_startup_screen.assert_called_once()


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_after_loaded_hide_mouse_not_display(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test the mouse is showing even if the `hide mouse` setting is set while is_display=false
    """
    # GIVEN: An initialised display window and settings for item transitions and hide mouse returns true
    display_window = DisplayWindow()
    display_window.is_display = False
    mock_settings.value.return_value = True
    display_window.scale = 2
    display_window._is_initialised = True
    display_window.run_javascript = MagicMock()
    display_window.set_scale = MagicMock()
    display_window.set_startup_screen = MagicMock()

    # WHEN: after_loaded is run
    display_window.after_loaded()

    # THEN: Display.init should be called where is_display=false, do_item_transitions=true, show_mouse=false
    display_window.run_javascript.assert_called_once_with('Display.init({'
                                                          'isDisplay: false,'
                                                          'doItemTransitions: true,'
                                                          'hideMouse: false'
                                                          '});')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch.object(time, 'time')
def test_run_javascript_no_sync_no_wait(mock_time, mocked_webengine, mocked_addWidget, mock_settings):
    """
    test a script is run on the webview
    """
    # GIVEN: A (fake) webengine page
    display_window = DisplayWindow()
    webengine_page = MagicMock()
    display_window.webview.page = MagicMock(return_value=webengine_page)

    # WHEN: javascript is requested to run
    display_window.run_javascript('javascript to execute')

    # THEN: javascript should be run with no delay
    webengine_page.runJavaScript.assert_called_once_with('javascript to execute')
    mock_time.sleep.assert_not_called()


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch.object(time, 'time')
def test_run_javascript_sync_no_wait(mock_time, mocked_webengine, mocked_addWidget, mock_settings):
    """
    test a synced script is run on the webview and immediately returns a result
    """
    # GIVEN: A (fake) webengine page with a js callback fn
    def save_callback(script, callback):
        callback(1234)
    display_window = DisplayWindow()
    display_window.webview = MagicMock()
    webengine_page = MagicMock()
    webengine_page.runJavaScript.side_effect = save_callback
    display_window.webview.page.return_value = webengine_page

    # WHEN: javascript is requested to run
    result = display_window.run_javascript('javascript to execute', True)

    # THEN: javascript should be run with no delay and return with the correct result
    assert result == 1234
    webengine_page.runJavaScript.assert_called_once()
    mock_time.sleep.assert_not_called()


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.is_win')
def test_fix_font_bold_windows(mocked_is_win, mocked_webengine, mocked_layout, mock_settings):
    """
    Test that on Windows, fonts that end with "Bold" are handled
    """
    # GIVEN: A display window and a font name
    mocked_is_win.return_value = True
    display_window = DisplayWindow()
    display_window.is_display = True
    display_window.run_javascript = MagicMock()
    font_name = 'Arial Rounded MT Bold'

    # WHEN: The font is processed
    result = display_window._fix_font_name(font_name)

    # Then the font name should be fixed
    assert result == 'Arial Rounded MT'


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.is_win')
def test_fix_font_bold_not_windows(mocked_is_win, mocked_webengine, mocked_layout, mock_settings):
    """
    Test that on NOT Windows, fonts that end with "Bold" are ignored
    """
    # GIVEN: A display window and a font name
    mocked_is_win.return_value = False
    display_window = DisplayWindow()
    display_window.is_display = True
    display_window.run_javascript = MagicMock()
    font_name = 'Arial Rounded MT Bold'

    # WHEN: The font is processed
    result = display_window._fix_font_name(font_name)

    # Then the font name should be fixed
    assert result == 'Arial Rounded MT Bold'


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.is_win')
def test_fix_font_foundry(mocked_is_win, mocked_webengine, mocked_layout, mock_settings):
    """
    Test that a font with a foundry name in it has the foundry removed
    """
    # GIVEN: A display window and a font name
    mocked_is_win.return_value = False
    display_window = DisplayWindow()
    display_window.is_display = True
    display_window.run_javascript = MagicMock()
    font_name = 'CMG Sans [Foundry]'

    # WHEN: The font is processed
    result = display_window._fix_font_name(font_name)

    # Then the font name should be fixed
    assert result == 'CMG Sans'


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_set_theme_is_display_video(mocked_webengine, mocked_addWidget, mock_settings, mock_geometry):
    """
    Test the set_theme function
    """
    # GIVEN: A display window and a video theme
    display_window = DisplayWindow()
    display_window.is_display = True
    display_window.run_javascript = MagicMock()
    theme = Theme()
    theme.background_type = 'video'
    result_theme = Theme()
    result_theme.background_type = 'transparent'
    result_theme = result_theme.export_theme(is_js=True)

    # WHEN: The set theme function is called
    display_window.set_theme(theme, is_sync=False, service_item_type=ServiceItemType.Text)

    # THEN: The final theme should be transparent
    display_window.run_javascript.assert_called_once_with('Display.setTheme({theme});'.format(theme=result_theme),
                                                          is_sync=False)


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_set_theme_not_display_video(mocked_webengine, mocked_addWidget, mock_settings, mock_geometry):
    """
    Test the set_theme function
    """
    # GIVEN: A display window and a video theme
    display_window = DisplayWindow()
    display_window.is_display = False
    display_window.run_javascript = MagicMock()
    theme = Theme()
    theme.background_type = 'video'
    theme.background_border_color = 'border_colour'
    result_theme = Theme()
    result_theme.background_type = 'solid'
    result_theme.background_border_color = 'border_colour'
    result_theme.background_start_color = 'border_colour'
    result_theme.background_end_color = 'border_colour'
    result_theme.background_main_color = 'border_colour'
    result_theme.background_footer_color = 'border_colour'
    result_theme.background_color = 'border_colour'
    result_theme = result_theme.export_theme(is_js=True)

    # WHEN: The set theme function is called
    display_window.set_theme(theme, is_sync=False, service_item_type=False)

    # THEN: The final theme should use 'border_colour' for it's colour values
    display_window.run_javascript.assert_called_once_with('Display.setTheme({theme});'.format(theme=result_theme),
                                                          is_sync=False)


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_set_theme_not_display_live(mocked_webengine, mocked_addWidget, mock_settings, mock_geometry):
    """
    Test the set_theme function
    """
    # GIVEN: A display window and a video theme
    display_window = DisplayWindow()
    display_window.is_display = False
    display_window.run_javascript = MagicMock()
    theme = Theme()
    theme.background_type = 'live'
    result_theme = Theme()
    result_theme.background_type = 'solid'
    result_theme.background_start_color = '#590909'
    result_theme.background_end_color = '#590909'
    result_theme.background_main_color = '#090909'
    result_theme.background_footer_color = '#090909'
    result_theme = result_theme.export_theme(is_js=True)

    # WHEN: The set theme function is called
    display_window.set_theme(theme, is_sync=False, service_item_type=False)

    # THEN: The final theme should use the preset colour values
    display_window.run_javascript.assert_called_once_with('Display.setTheme({theme});'.format(theme=result_theme),
                                                          is_sync=False)


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.Registry.execute')
@patch('openlp.core.display.window.ScreenList')
def test_show_display(mocked_screenlist, mocked_registry_execute, mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test show_display function
    """
    # GIVEN: Display window as the active display
    display_window = DisplayWindow()
    display_window.is_display = True
    display_window.isHidden = MagicMock(return_value=True)
    display_window.setVisible = MagicMock()
    display_window.run_javascript = MagicMock()
    mocked_screenlist.screens = [1, 2]

    # WHEN: Show display is run
    display_window.show_display()

    # THEN: Should show the display and set the hide mode to none
    display_window.setVisible.assert_called_once_with(True)
    display_window.run_javascript.assert_called_once_with('Display.show();')
    mocked_registry_execute.assert_called_once_with('live_display_active')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.ScreenList')
def test_show_display_no_display(mocked_screenlist, mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test show_display function when no displays are available
    """
    # GIVEN: A Display window, one screen and core/display on monitor disabled
    display_window = DisplayWindow()
    display_window.run_javascript = MagicMock()
    display_window.is_display = True
    mocked_screenlist.return_value = [1]
    mock_settings.value.return_value = False

    # WHEN: Show display is run
    display_window.show_display()

    # THEN: Shouldn't run the js show fn
    assert display_window.run_javascript.call_count == 0


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_hide_display_to_screen(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test hide to screen in the hide_display function
    """
    # GIVEN: Display window and setting advanced/disable transparent display = False
    display_window = DisplayWindow()
    display_window.run_javascript = MagicMock()
    display_window.setVisible = MagicMock()
    mock_settings.value.return_value = False

    # WHEN: Hide display is run with no mode (should default to Screen)
    display_window.hide_display()

    # THEN: Should hide the display with the js transparency function (not setVisible)
    display_window.setVisible.call_count == 0
    display_window.run_javascript.assert_called_once_with('Display.toTransparent();')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_hide_display_to_blank(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test hide to screen in the hide_display function
    """
    # GIVEN: Display window and setting advanced/disable transparent display = False
    display_window = DisplayWindow()
    display_window.run_javascript = MagicMock()
    mock_settings.value.return_value = False

    # WHEN: Hide display is run with HideMode.Blank
    display_window.hide_display(HideMode.Blank)

    # THEN: Should run the correct javascript on the display and set the hide mode
    display_window.run_javascript.assert_called_once_with('Display.toBlack();')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_hide_display_to_theme(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test hide to screen in the hide_display function
    """
    # GIVEN: Display window and setting advanced/disable transparent display = False
    display_window = DisplayWindow()
    display_window.run_javascript = MagicMock()
    mock_settings.value.return_value = False

    # WHEN: Hide display is run with HideMode.Theme
    display_window.hide_display(HideMode.Theme)

    # THEN: Should run the correct javascript on the display and set the hide mode
    display_window.run_javascript.assert_called_once_with('Display.toTheme();')


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_hide_display_to_transparent(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test hide to screen in the hide_display function
    """
    # GIVEN: Display window and setting advanced/disable transparent display = False
    display_window = DisplayWindow()
    display_window.run_javascript = MagicMock()
    display_window.setVisible = MagicMock()
    mock_settings.value.return_value = False

    # WHEN: Hide display is run with HideMode.Screen
    display_window.hide_display(HideMode.Screen)

    # THEN: Should run the correct javascript on the display and not set the visiblity
    display_window.run_javascript.assert_called_once_with('Display.toTransparent();')
    assert display_window.setVisible.call_count == 0


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
def test_hide_transparent_to_screen(mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test that when going transparent, and the disable transparent setting is enabled,
    the screen mode should be used.
    """
    # GIVEN: Display window and setting advanced/disable transparent display = True
    display_window = DisplayWindow()
    display_window.setVisible = MagicMock()
    mock_settings.value.return_value = True

    # WHEN: Hide display is run with HideMode.Screen
    display_window.hide_display(HideMode.Screen)

    # THEN: Should run setVisible(False)
    display_window.setVisible.assert_called_once_with(False)


@patch('openlp.core.display.window.QtWidgets.QVBoxLayout')
@patch('openlp.core.display.webengine.WebEngineView')
@patch('openlp.core.display.window.ScreenList')
def test_hide_display_no_display(mocked_screenlist, mocked_webengine, mocked_addWidget, mock_settings):
    """
    Test show_display function when no displays are available
    """
    # GIVEN: A Display window, one screen and core/display on monitor disabled
    display_window = DisplayWindow()
    display_window.hide_mode = None
    display_window.is_display = True
    mocked_screenlist.return_value = [1]
    mock_settings.value.return_value = False

    # WHEN: Hide display is run
    display_window.hide_display(HideMode.Screen)

    # THEN: Hide mode should still be none
    assert display_window.hide_mode is None


def test_display_watcher_set_initialised():
    """
    Test that the initialised signal is emitted
    """
    # GIVEN: A DisplayWatcher instance
    display_watcher = DisplayWatcher(None)

    # WHEN: setInitialised is called
    with patch.object(display_watcher, 'initialised') as mocked_initialised:
        display_watcher.setInitialised(True)

        # THEN: initialised should have been emitted
        mocked_initialised.emit.assert_called_once_with(True)
