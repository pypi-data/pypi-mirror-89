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
Package to test the openlp.core.ui.slidecontroller package.
"""
import datetime

from unittest.mock import MagicMock, patch, sentinel

from PyQt5 import QtCore, QtGui

from openlp.core.state import State
from openlp.core.common.registry import Registry
from openlp.core.lib import ServiceItemAction
from openlp.core.ui import HideMode
from openlp.core.ui.slidecontroller import NON_TEXT_MENU, WIDE_MENU, NARROW_MENU, InfoLabel, LiveController, \
    PreviewController, SlideController


def test_initial_slide_controller(registry):
    """
    Test the initial slide controller state .
    """
    # GIVEN: A new SlideController instance.
    slide_controller = SlideController(None)

    # WHEN: the default controller is built.
    # THEN: The controller should not be a live controller.
    assert slide_controller.is_live is False, 'The base slide controller should not be a live controller'


def test_slide_selected(settings):
    """
    Test the slide selected method
    """
    # GIVEN: A new SlideController instance on slide 4 of 10, and is not a command
    slide_controller = SlideController(None)
    slide_controller.update_preview = MagicMock()
    slide_controller.slide_selected_lock = MagicMock()
    slide_controller.service_item = MagicMock()
    slide_controller.service_item.is_command.return_value = False
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_widget.slide_count.return_value = 10
    slide_controller.preview_widget.current_slide_number.return_value = 4
    mocked_display = MagicMock()
    slide_controller.displays = [mocked_display]

    # WHEN: The slide_selected method is run
    slide_controller.slide_selected(True)

    # THEN: The display is updated with the slide number
    mocked_display.go_to_slide.assert_called_once_with(4)


def test_text_service_item_blank(settings):
    """
    Test that loading a text-based service item into the slide controller sets the correct blank menu
    """
    # GIVEN: A new SlideController instance.
    slide_controller = SlideController(None)
    service_item = MagicMock()
    toolbar = MagicMock()
    toolbar.set_widget_visible = MagicMock()
    slide_controller.toolbar = toolbar
    slide_controller.service_item = service_item

    # WHEN: a text based service item is used
    slide_controller.service_item.is_text = MagicMock(return_value=True)
    slide_controller.set_hide_mode_menu(narrow=False)

    # THEN: the call to set the visible items on the toolbar should be correct
    toolbar.set_widget_visible.assert_any_call(NARROW_MENU, False)
    toolbar.set_widget_visible.assert_called_with(WIDE_MENU, True)


def test_non_text_service_item_blank(settings):
    """
    Test that loading a non-text service item into the slide controller sets the correct blank menu
    """
    # GIVEN: A new SlideController instance.
    slide_controller = SlideController(None)
    service_item = MagicMock()
    toolbar = MagicMock()
    toolbar.set_widget_visible = MagicMock()
    slide_controller.toolbar = toolbar
    slide_controller.service_item = service_item

    # WHEN a non text based service item is used
    slide_controller.service_item.is_text = MagicMock(return_value=False)
    slide_controller.set_hide_mode_menu(narrow=False)

    # THEN: then call set up the toolbar to blank the display screen.
    toolbar.set_widget_visible.assert_any_call(NARROW_MENU, False)
    toolbar.set_widget_visible.assert_called_with(NON_TEXT_MENU, True)


def test_text_service_item_blank_narrow(settings):
    """
    Test that loading a text-based service item into the slide controller sets the correct blank menu
    """
    # GIVEN: A new SlideController instance.
    slide_controller = SlideController(None)
    service_item = MagicMock()
    toolbar = MagicMock()
    toolbar.set_widget_visible = MagicMock()
    slide_controller.toolbar = toolbar
    slide_controller.service_item = service_item

    # WHEN: a text based service item is used
    slide_controller.service_item.is_text = MagicMock(return_value=True)
    slide_controller.set_hide_mode_menu(narrow=True)

    # THEN: the call to set the visible items on the toolbar should be correct
    toolbar.set_widget_visible.assert_any_call(NARROW_MENU, True)
    toolbar.set_widget_visible.assert_any_call(WIDE_MENU, False)


def test_on_controller_size_changed_wide(settings):
    """
    Test that on_controller_size_changed
    """
    # GIVEN: A new SlideController instance where the toolbar has a lot of spare space.
    slide_controller = SlideController(None)
    slide_controller.is_live = True
    slide_controller.ignore_toolbar_resize_events = False
    slide_controller.controller = MagicMock(width=MagicMock(return_value=100))
    slide_controller.toolbar = MagicMock(size=MagicMock(return_value=MagicMock(width=MagicMock(return_value=10))))
    slide_controller.hide_menu = MagicMock(isVisible=MagicMock(return_value=False))
    slide_controller.set_hide_mode_menu = MagicMock()

    # WHEN: The on_controller_size_changed function is called
    slide_controller.on_controller_size_changed()

    # THEN: set_hide_mode_menu should have received the correct call
    slide_controller.set_hide_mode_menu.assert_called_with(narrow=False)


def test_on_controller_size_changed_narrow(settings):
    """
    Test that on_controller_size_changed
    """
    # GIVEN: A new SlideController instance where the toolbar has a lot of spare space.
    slide_controller = SlideController(None)
    slide_controller.is_live = True
    slide_controller.ignore_toolbar_resize_events = False
    slide_controller.controller = MagicMock(width=MagicMock(return_value=100))
    slide_controller.toolbar = MagicMock(size=MagicMock(return_value=MagicMock(width=MagicMock(return_value=110))))
    slide_controller.hide_menu = MagicMock(isVisible=MagicMock(return_value=False))
    slide_controller.set_hide_mode_menu = MagicMock()

    # WHEN: The on_controller_size_changed function is called
    slide_controller.on_controller_size_changed()

    # THEN: set_hide_mode_menu should have received the correct call
    slide_controller.set_hide_mode_menu.assert_called_with(narrow=True)


def test_on_controller_size_changed_can_not_expand(settings):
    """
    Test that on_controller_size_changed
    """
    # GIVEN: A new SlideController instance where the toolbar has a lot of spare space.
    slide_controller = SlideController(None)
    slide_controller.is_live = True
    slide_controller.ignore_toolbar_resize_events = False
    slide_controller.controller = MagicMock(width=MagicMock(return_value=100))
    slide_controller.toolbar = MagicMock(size=MagicMock(return_value=MagicMock(width=MagicMock(return_value=95))))
    slide_controller.hide_menu = MagicMock(isVisible=MagicMock(return_value=True))
    slide_controller.set_hide_mode_menu = MagicMock()

    # WHEN: The on_controller_size_changed function is called
    slide_controller.on_controller_size_changed()

    # THEN: set_hide_mode_menu should have received the correct call
    slide_controller.set_hide_mode_menu.assert_not_called()


def test_receive_spin_delay(mock_settings):
    """
    Test that the spin box is updated accordingly after a call to receive_spin_delay()
    """
    # GIVEN: A new SlideController instance.
    mock_settings.value.return_value = 1
    mocked_delay_spin_box = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.delay_spin_box = mocked_delay_spin_box

    # WHEN: The receive_spin_delay() method is called
    slide_controller.receive_spin_delay()

    # THEN: The settings value() and delay_spin_box.setValue() methods should have been called correctly
    msv = mock_settings.value
    msv.assert_called_with('core/loop delay')
    mocked_delay_spin_box.setValue.assert_called_with(1)


def test_toggle_display_blank(settings):
    """
    Check that the toggle_display('blank') method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode

    # WHEN: toggle_display() is called with an argument of "blank"
    slide_controller.toggle_display('blank')

    # THEN: set_hide_mode should have been called with an argument of HideMode.Blank
    mocked_set_hide_mode.assert_called_once_with(HideMode.Blank)


def test_toggle_display_hide(settings):
    """
    Check that the toggle_display('hide') method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode

    # WHEN: toggle_display() is called with an argument of "hide"
    slide_controller.toggle_display('hide')

    # THEN: set_hide_mode should have been called with an argument of HideMode.Blank
    mocked_set_hide_mode.assert_called_once_with(HideMode.Blank)


def test_toggle_display_theme(settings):
    """
    Check that the toggle_display('theme') method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode

    # WHEN: toggle_display() is called with an argument of "theme"
    slide_controller.toggle_display('theme')

    # THEN: set_hide_mode should have been called with an argument of HideMode.Theme
    mocked_set_hide_mode.assert_called_once_with(HideMode.Theme)


def test_toggle_display_desktop(settings):
    """
    Check that the toggle_display('desktop') method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode

    # WHEN: toggle_display() is called with an argument of "desktop"
    slide_controller.toggle_display('desktop')

    # THEN: set_hide_mode should have been called with an argument of HideMode.Screen
    mocked_set_hide_mode.assert_called_once_with(HideMode.Screen)


def test_toggle_display_show(settings):
    """
    Check that the toggle_display('show') method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode

    # WHEN: toggle_display() is called with an argument of "show"
    slide_controller.toggle_display('show')

    # THEN: set_hide_mode should have been called with an argument of None
    mocked_set_hide_mode.assert_called_once_with(None)


def test_on_toggle_blank(settings):
    """
    Check that the on_toggle_blank method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns none.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=None)

    # WHEN: on_toggle_blank() is called
    slide_controller.on_toggle_blank()

    # THEN: set_hide_mode should have been called with an argument of HideMode.Blank
    mocked_set_hide_mode.assert_called_once_with(HideMode.Blank)


def test_on_toggle_blank_off(settings):
    """
    Check that the on_toggle_blank method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns blank.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=HideMode.Blank)

    # WHEN: on_toggle_blank() is called
    slide_controller.on_toggle_blank()

    # THEN: set_hide_mode should have been called with an argument of None
    mocked_set_hide_mode.assert_called_once_with(None)


def test_on_toggle_theme(settings):
    """
    Check that the on_toggle_theme method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns none.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=None)

    # WHEN: on_toggle_theme() is called
    slide_controller.on_toggle_theme()

    # THEN: set_hide_mode should have been called with an argument of HideMode.Theme
    mocked_set_hide_mode.assert_called_once_with(HideMode.Theme)


def test_on_toggle_theme_off(settings):
    """
    Check that the on_toggle_theme method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns Theme.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=HideMode.Theme)

    # WHEN: on_toggle_theme() is called
    slide_controller.on_toggle_theme()

    # THEN: set_hide_mode should have been called with an argument of None
    mocked_set_hide_mode.assert_called_once_with(None)


def test_on_toggle_desktop(settings):
    """
    Check that the on_toggle_desktop method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns none.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=None)

    # WHEN: on_toggle_desktop() is called
    slide_controller.on_toggle_desktop()

    # THEN: set_hide_mode should have been called with an argument of HideMode.Screen
    mocked_set_hide_mode.assert_called_once_with(HideMode.Screen)


def test_on_toggle_desktop_off(settings):
    """
    Check that the on_toggle_desktop method calls set_hide_mode with the correct HideMode
    """
    # GIVEN: A new SlideController instance, and get_hide_mode returns Screen.
    mocked_set_hide_mode = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.set_hide_mode = mocked_set_hide_mode
    slide_controller.get_hide_mode = MagicMock(return_value=HideMode.Screen)

    # WHEN: on_toggle_desktop() is called
    slide_controller.on_toggle_desktop()

    # THEN: set_hide_mode should have been called with an argument of None
    mocked_set_hide_mode.assert_called_once_with(None)


def test_on_go_live_live_controller(registry):
    """
    Test that when the on_go_live() method is called the message is sent to the live controller and focus is
    set correctly.
    """
    # GIVEN: A new SlideController instance and plugin preview then pressing go live should respond
    mocked_display = MagicMock()
    mocked_live_controller = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_service_item = MagicMock()
    mocked_service_item.from_service = False
    mocked_preview_widget.current_slide_number.return_value = 1
    mocked_preview_widget.slide_count = MagicMock(return_value=2)
    mocked_live_controller.preview_widget = MagicMock()
    Registry().register('live_controller', mocked_live_controller)
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_service_item
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller.displays = [mocked_display]

    # WHEN: on_go_live() is called
    slide_controller.on_go_live()

    # THEN: the live controller should have the service item and the focus set to live
    mocked_live_controller.add_service_manager_item.assert_called_once_with(mocked_service_item, 1)
    mocked_live_controller.preview_widget.setFocus.assert_called_once_with()


def test_on_go_live_service_manager(registry):
    """
    Test that when the on_go_live() method is called the message is sent to the live controller and focus is
    set correctly.
    """
    # GIVEN: A new SlideController instance and service manager preview then pressing go live should respond
    mocked_display = MagicMock()
    mocked_service_manager = MagicMock()
    mocked_live_controller = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_service_item = MagicMock()
    mocked_service_item.from_service = True
    mocked_service_item.unique_identifier = 42
    mocked_preview_widget.current_slide_number.return_value = 1
    mocked_preview_widget.slide_count = MagicMock(return_value=2)
    mocked_live_controller.preview_widget = MagicMock()
    Registry().register('live_controller', mocked_live_controller)
    Registry().register('service_manager', mocked_service_manager)
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_service_item
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller.displays = [mocked_display]

    # WHEN: on_go_live() is called
    slide_controller.on_go_live()

    # THEN: the service manager should have the service item and the focus set to live
    mocked_service_manager.preview_live.assert_called_once_with(42, 1)
    mocked_live_controller.preview_widget.setFocus.assert_called_once_with()


def test_service_previous(settings):
    """
    Check that calling the service_previous() method adds the previous key to the queue and processes the queue
    """
    # GIVEN: A new SlideController instance.
    mocked_keypress_queue = MagicMock()
    mocked_process_queue = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.keypress_queue = mocked_keypress_queue
    slide_controller._process_queue = mocked_process_queue

    # WHEN: The service_previous() method is called
    slide_controller.service_previous()

    # THEN: The keypress is added to the queue and the queue is processed
    mocked_keypress_queue.append.assert_called_once_with(ServiceItemAction.Previous)
    mocked_process_queue.assert_called_once_with()


def test_service_next(settings):
    """
    Check that calling the service_next() method adds the next key to the queue and processes the queue
    """
    # GIVEN: A new SlideController instance and mocked out methods
    mocked_keypress_queue = MagicMock()
    mocked_process_queue = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.keypress_queue = mocked_keypress_queue
    slide_controller._process_queue = mocked_process_queue

    # WHEN: The service_next() method is called
    slide_controller.service_next()

    # THEN: The keypress is added to the queue and the queue is processed
    mocked_keypress_queue.append.assert_called_once_with(ServiceItemAction.Next)
    mocked_process_queue.assert_called_once_with()


def test_update_slide_limits(mock_settings):
    """
    Test that calling the update_slide_limits() method updates the slide limits
    """
    # GIVEN: A mocked out Settings object, a new SlideController and a mocked out main_window
    mock_settings.value.return_value = 10
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    slide_controller = SlideController(None)

    # WHEN: update_slide_limits() is called
    slide_controller.update_slide_limits()

    # THEN: The value of slide_limits should be 10
    msv = mock_settings.value
    msv.assert_called_once_with('advanced/slide limits')
    assert 10 == slide_controller.slide_limits, 'Slide limits should have been updated to 10'


def test_enable_tool_bar_live(settings):
    """
    Check that when enable_tool_bar on a live slide controller is called, enable_live_tool_bar is called
    """
    # GIVEN: Mocked out enable methods and a real slide controller which is set to live
    mocked_enable_live_tool_bar = MagicMock()
    mocked_enable_preview_tool_bar = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.is_live = True
    slide_controller.enable_live_tool_bar = mocked_enable_live_tool_bar
    slide_controller.enable_preview_tool_bar = mocked_enable_preview_tool_bar
    mocked_service_item = MagicMock()

    # WHEN: enable_tool_bar() is called
    slide_controller.enable_tool_bar(mocked_service_item)

    # THEN: The enable_live_tool_bar() method is called, not enable_preview_tool_bar()
    mocked_enable_live_tool_bar.assert_called_once_with(mocked_service_item)
    assert 0 == mocked_enable_preview_tool_bar.call_count, 'The preview method should not have been called'


def test_enable_tool_bar_preview(settings):
    """
    Check that when enable_tool_bar on a preview slide controller is called, enable_preview_tool_bar is called
    """
    # GIVEN: Mocked out enable methods and a real slide controller which is set to live
    mocked_enable_live_tool_bar = MagicMock()
    mocked_enable_preview_tool_bar = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.is_live = False
    slide_controller.enable_live_tool_bar = mocked_enable_live_tool_bar
    slide_controller.enable_preview_tool_bar = mocked_enable_preview_tool_bar
    mocked_service_item = MagicMock()

    # WHEN: enable_tool_bar() is called
    slide_controller.enable_tool_bar(mocked_service_item)

    # THEN: The enable_preview_tool_bar() method is called, not enable_live_tool_bar()
    mocked_enable_preview_tool_bar.assert_called_once_with(mocked_service_item)
    assert 0 == mocked_enable_live_tool_bar.call_count, 'The live method should not have been called'


def test_refresh_service_item_text(settings):
    """
    Test that the refresh_service_item() method refreshes a text service item
    """
    # GIVEN: A mock service item and a fresh slide controller
    mocked_service_item = MagicMock()
    mocked_service_item.is_text.return_value = True
    mocked_service_item.is_image.return_value = False
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_service_item
    slide_controller._process_item = mocked_process_item
    slide_controller.selected_row = 5

    # WHEN: The refresh_service_item method() is called
    slide_controller.refresh_service_item()

    # THEN: The item should be re-processed
    mocked_service_item.is_text.assert_called_once_with()
    assert 0 == mocked_service_item.is_image.call_count, 'is_image should not have been called'
    mocked_service_item.render.assert_called_once_with()
    mocked_process_item.assert_called_once_with(mocked_service_item, 5)


def test_refresh_service_item_image(settings):
    """
    Test that the refresh_service_item() method refreshes a image service item
    """
    # GIVEN: A mock service item and a fresh slide controller
    mocked_service_item = MagicMock()
    mocked_service_item.is_text.return_value = False
    mocked_service_item.is_image.return_value = True
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_service_item
    slide_controller._process_item = mocked_process_item
    slide_controller.selected_row = 5

    # WHEN: The refresh_service_item method() is called
    slide_controller.refresh_service_item()

    # THEN: The item should be re-processed
    mocked_service_item.is_text.assert_called_once_with()
    mocked_service_item.is_image.assert_called_once_with()
    mocked_service_item.render.assert_called_once_with()
    mocked_process_item.assert_called_once_with(mocked_service_item, 5)


def test_refresh_service_item_not_image_or_text(settings):
    """
    Test that the refresh_service_item() method does not refresh a service item if it's neither text or an image
    """
    # GIVEN: A mock service item and a fresh slide controller
    mocked_service_item = MagicMock()
    mocked_service_item.is_text.return_value = False
    mocked_service_item.is_image.return_value = False
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_service_item
    slide_controller._process_item = mocked_process_item
    slide_controller.selected_row = 5

    # WHEN: The refresh_service_item method() is called
    slide_controller.refresh_service_item()

    # THEN: The item should be re-processed
    mocked_service_item.is_text.assert_called_once_with()
    mocked_service_item.is_image.assert_called_once_with()
    assert 0 == mocked_service_item.render.call_count, 'The render() method should not have been called'
    assert 0 == mocked_process_item.call_count, 'The mocked_process_item() method should not have been called'


def test_add_service_item_with_song_edit(settings):
    """
    Test the add_service_item() method when song_edit is True
    """
    # GIVEN: A slide controller and a new item to add
    mocked_item = MagicMock()
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller._process_item = mocked_process_item
    slide_controller.song_edit = True
    slide_controller.selected_row = 2

    # WHEN: The item is added to the service
    slide_controller.add_service_item(mocked_item)

    # THEN: The item is processed, the slide number is correct, and the song is not editable (or something)
    assert slide_controller.song_edit is False, 'song_edit should be False'
    mocked_process_item.assert_called_once_with(mocked_item, 2)


def test_add_service_item_without_song_edit(settings):
    """
    Test the add_service_item() method when song_edit is False
    """
    # GIVEN: A slide controller and a new item to add
    mocked_item = MagicMock()
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller._process_item = mocked_process_item
    slide_controller.song_edit = False
    slide_controller.selected_row = 2

    # WHEN: The item is added to the service
    slide_controller.add_service_item(mocked_item)

    # THEN: The item is processed, the slide number is correct, and the song is not editable (or something)
    assert slide_controller.song_edit is False, 'song_edit should be False'
    mocked_process_item.assert_called_once_with(mocked_item, 0)


def test_replace_service_manager_item_different_items(settings):
    """
    Test that when the service items are not the same, nothing happens
    """
    # GIVEN: A slide controller and a new item to add
    mocked_item = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller._process_item = mocked_process_item
    slide_controller.service_item = None

    # WHEN: The service item is replaced
    slide_controller.replace_service_manager_item(mocked_item)

    # THEN: The service item should not be processed
    assert 0 == mocked_process_item.call_count, 'The _process_item() method should not have been called'
    assert 0 == mocked_preview_widget.current_slide_number.call_count, \
        'The preview_widget current_slide_number.() method should not have been called'


def test_replace_service_manager_item_same_item(settings):
    """
    Test that when the service item is the same, the service item is reprocessed
    """
    # GIVEN: A slide controller and a new item to add
    mocked_item = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_preview_widget.current_slide_number.return_value = 7
    mocked_process_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller._process_item = mocked_process_item
    slide_controller.service_item = mocked_item

    # WHEN: The service item is replaced
    slide_controller.replace_service_manager_item(mocked_item)

    # THEN: The service item should not be processed
    mocked_preview_widget.current_slide_number.assert_called_with()
    mocked_process_item.assert_called_once_with(mocked_item, 7)


def test_on_slide_selected_index_no_service_item(settings):
    """
    Test that when there is no service item, the on_slide_selected_index() method returns immediately
    """
    # GIVEN: A mocked service item and a slide controller without a service item
    mocked_item = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = None

    # WHEN: The method is called
    slide_controller.on_slide_selected_index([10])

    # THEN: It should have exited early
    assert 0 == mocked_item.is_command.call_count, 'The service item should have not been called'


@patch.object(Registry, 'execute')
def test_on_slide_selected_index_service_item_command(mocked_execute, registry):
    """
    Test that when there is a command service item, the command is executed
    """
    # GIVEN: A mocked service item and a slide controller with a service item
    mocked_item = MagicMock()
    mocked_item.is_command.return_value = True
    mocked_item.name = 'Mocked Item'
    mocked_update_preview = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_slide_selected = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_item
    slide_controller.update_preview = mocked_update_preview
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller.slide_selected = mocked_slide_selected
    slide_controller.is_live = True

    # WHEN: The method is called
    slide_controller.on_slide_selected_index([9])

    # THEN: It should have sent a notification
    mocked_item.is_command.assert_called_once_with()
    mocked_execute.assert_called_once_with('mocked item_slide', [mocked_item, True, 9])
    mocked_update_preview.assert_called_once_with()
    assert 0 == mocked_preview_widget.change_slide.call_count, 'Change slide should not have been called'
    assert 0 == mocked_slide_selected.call_count, 'slide_selected should not have been called'


@patch.object(Registry, 'execute')
def test_on_slide_selected_index_service_item_not_command(mocked_execute, registry):
    """
    Test that when there is a service item but it's not a command, the preview widget is updated
    """
    # GIVEN: A mocked service item and a slide controller with a service item
    mocked_item = MagicMock()
    mocked_item.is_command.return_value = False
    mocked_item.name = 'Mocked Item'
    mocked_update_preview = MagicMock()
    mocked_preview_widget = MagicMock()
    mocked_slide_selected = MagicMock()
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_item
    slide_controller.update_preview = mocked_update_preview
    slide_controller.preview_widget = mocked_preview_widget
    slide_controller.slide_selected = mocked_slide_selected

    # WHEN: The method is called
    slide_controller.on_slide_selected_index([7])

    # THEN: It should have sent a notification
    mocked_item.is_command.assert_called_once_with()
    assert 0 == mocked_execute.call_count, 'Execute should not have been called'
    assert 0 == mocked_update_preview.call_count, 'Update preview should not have been called'
    mocked_preview_widget.change_slide.assert_called_once_with(7)
    mocked_slide_selected.assert_called_once_with()


def test_set_background_image(registry):
    """
    Test that the display and preview background are set
    """
    # GIVEN: A slide controller
    slide_controller = SlideController(None)
    slide_controller.preview_display = MagicMock()
    mock_display = MagicMock()
    slide_controller.displays = [mock_display]

    # WHEN: set_background_image is called
    slide_controller.set_background_image(sentinel.image)

    # THEN: The preview and main display are called with the new colour and image
    slide_controller.preview_display.set_background_image.assert_called_once_with(sentinel.image)
    mock_display.set_background_image.assert_called_once_with(sentinel.image)


def test_theme_updated(mock_settings):
    """
    Test that the theme_updated function updates the service if hot reload is on
    """
    # GIVEN: A slide controller and settings return true
    slide_controller = SlideController(None)
    slide_controller.service_item = sentinel.service_item
    slide_controller._process_item = MagicMock()
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_widget.current_slide_number.return_value = 14
    mock_settings.value.return_value = True

    # WHEN: theme_updated is called
    slide_controller.theme_updated()

    # THEN: process_item is called with the current service_item and slide number
    slide_controller._process_item.assert_called_once_with(sentinel.service_item, 14)


def test_theme_updated_no_reload(mock_settings):
    """
    Test that the theme_updated function does not update the service if hot reload is off
    """
    # GIVEN: A slide controller and settings return false
    slide_controller = SlideController(None)
    slide_controller.service_item = sentinel.service_item
    slide_controller._process_item = MagicMock()
    slide_controller.preview_widget = MagicMock()
    mock_settings.value.return_value = False

    # WHEN: theme_updated is called
    slide_controller.theme_updated()

    # THEN: process_item is not called
    assert slide_controller._process_item.call_count == 0


def test_reload_theme(mock_settings):
    """
    Test that the reload_theme function triggers the reload_theme function for the displays
    """
    # GIVEN: A slide controller and mocked displays
    slide_controller = SlideController(None)
    slide_controller.preview_display = MagicMock()
    mock_display = MagicMock()
    slide_controller.displays = [mock_display]

    # WHEN: reload_theme is called
    slide_controller.reload_theme()

    # THEN: reload_theme is called with the preview and main display
    slide_controller.preview_display.reload_theme.assert_called_once_with()
    mock_display.reload_theme.assert_called_once_with()


@patch.object(Registry, 'execute')
def test_process_item(mocked_execute, registry, state_media):
    """
    Test that presentation service-items is closed when followed by a media service-item
    """
    # GIVEN: A mocked presentation service item, a mocked media service item, a mocked Registry.execute
    #        and a slide controller with many mocks.
    mocked_pres_item = MagicMock()
    mocked_pres_item.name = 'mocked_presentation_item'
    mocked_pres_item.is_command.return_value = True
    mocked_pres_item.is_media.return_value = False
    mocked_pres_item.is_image.return_value = False
    mocked_pres_item.from_service = False
    mocked_pres_item.get_frames.return_value = []
    mocked_media_item = MagicMock()
    mocked_media_item.name = 'mocked_media_item'
    mocked_media_item.is_command.return_value = True
    mocked_media_item.is_media.return_value = True
    mocked_media_item.is_image.return_value = False
    mocked_media_item.from_service = False
    mocked_media_item.get_frames.return_value = []
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('media_controller', MagicMock())
    Registry().register('application', MagicMock())
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_pres_item
    slide_controller.is_live = False
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_display = MagicMock()
    slide_controller.enable_tool_bar = MagicMock()
    slide_controller.on_media_start = MagicMock()
    slide_controller.slide_selected = MagicMock()
    slide_controller.on_stop_loop = MagicMock()
    slide_controller.info_label = MagicMock()
    slide_controller.displays = [MagicMock()]
    slide_controller.split = 0
    slide_controller.type_prefix = 'test'

    # WHEN: _process_item is called
    slide_controller._process_item(mocked_media_item, 0)

    # THEN: Registry.execute should have been called to stop the presentation
    assert 1 == mocked_execute.call_count, 'Execute should have been called once'
    assert 'mocked_presentation_item_stop' == mocked_execute.call_args_list[0][0][0], \
        'The presentation should have been stopped.'


@patch.object(Registry, 'execute')
def test_process_item_transition(mocked_execute, registry, state_media):
    """
    Test that the correct actions are taken when a media service-item is closed followed by a image service-item
    """
    # GIVEN: A mocked presentation service item, a mocked media service item, a mocked Registry.execute
    #        and a slide controller with many mocks.
    #        and the setting 'themes/item transitions' = True
    mocked_pres_item = MagicMock()
    mocked_pres_item.name = 'mocked_image_item'
    mocked_pres_item.is_command.return_value = True
    mocked_pres_item.is_media.return_value = True
    mocked_pres_item.is_image.return_value = False
    mocked_pres_item.from_service = False
    mocked_pres_item.get_frames.return_value = []
    mocked_media_item = MagicMock()
    mocked_media_item.name = 'mocked_media_item'
    mocked_media_item.get_transition_delay.return_value = 0
    mocked_media_item.is_text.return_value = False
    mocked_media_item.is_command.return_value = False
    mocked_media_item.is_media.return_value = False
    mocked_media_item.requires_media.return_value = False
    mocked_media_item.is_image.return_value = True
    mocked_media_item.from_service = False
    mocked_media_item.get_frames.return_value = []
    mocked_settings = MagicMock()
    mocked_settings.value.return_value = True
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('media_controller', MagicMock())
    Registry().register('application', MagicMock())
    Registry().register('settings', mocked_settings)
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_pres_item
    slide_controller.is_live = True
    slide_controller._reset_blank = MagicMock()
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_display = MagicMock()
    slide_controller.enable_tool_bar = MagicMock()
    slide_controller.on_controller_size_changed = MagicMock()
    slide_controller.on_media_start = MagicMock()
    slide_controller.on_media_close = MagicMock()
    slide_controller.slide_selected = MagicMock()
    slide_controller.new_song_menu = MagicMock()
    slide_controller.on_stop_loop = MagicMock()
    slide_controller.info_label = MagicMock()
    slide_controller.song_menu = MagicMock()
    slide_controller.displays = [MagicMock()]
    slide_controller.toolbar = MagicMock()
    slide_controller.split = 0
    slide_controller.type_prefix = 'test'
    slide_controller.screen_capture = 'old_capture'

    # WHEN: _process_item is called
    slide_controller._process_item(mocked_media_item, 0)

    # THEN: Registry.execute should have been called to start the live item
    #       Media should be closed
    #       Controller size change should be called (because it's a live item and the interface might have changed)
    #       The screen capture should have been reset to none
    assert 1 == mocked_execute.call_count, 'Execute should have been called once'
    slide_controller.on_media_close.assert_called_once_with()
    slide_controller.on_controller_size_changed.assert_called_once()
    assert slide_controller.screen_capture is None


@patch.object(Registry, 'execute')
def test_process_item_text(mocked_execute, registry, state_media):
    """
    Test that the correct actions are taken a text item is processed
    """
    # GIVEN: A mocked presentation service item, a mocked media service item, a mocked Registry.execute
    #        and a slide controller with many mocks.
    #        and the setting 'themes/item transitions' = True
    mocked_media_item = MagicMock()
    mocked_media_item.name = 'mocked_media_item'
    mocked_media_item.get_transition_delay.return_value = 0
    mocked_media_item.is_text.return_value = True
    mocked_media_item.is_command.return_value = False
    mocked_media_item.is_media.return_value = False
    mocked_media_item.requires_media.return_value = False
    mocked_media_item.is_image.return_value = False
    mocked_media_item.from_service = False
    mocked_media_item.get_frames.return_value = []
    mocked_media_item.display_slides = [{'verse': 'Verse name'}]
    mocked_settings = MagicMock()
    mocked_settings.value.return_value = True
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('media_controller', MagicMock())
    Registry().register('application', MagicMock())
    Registry().register('settings', mocked_settings)
    slide_controller = SlideController(None)
    slide_controller.service_item = None
    slide_controller.is_live = True
    slide_controller._reset_blank = MagicMock()
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_display = MagicMock()
    slide_controller.enable_tool_bar = MagicMock()
    slide_controller.on_controller_size_changed = MagicMock()
    slide_controller.on_media_start = MagicMock()
    slide_controller.on_media_close = MagicMock()
    slide_controller.slide_selected = MagicMock()
    slide_controller.new_song_menu = MagicMock()
    slide_controller.on_stop_loop = MagicMock()
    slide_controller.info_label = MagicMock()
    slide_controller.song_menu = MagicMock()
    slide_controller.displays = [MagicMock()]
    slide_controller.toolbar = MagicMock()
    slide_controller.split = 0
    slide_controller.type_prefix = 'test'
    slide_controller.screen_capture = 'old_capture'

    # WHEN: _process_item is called
    slide_controller._process_item(mocked_media_item, 0)

    # THEN: Registry.execute should have been called to start the live item
    #       Controller size change should be called (because it's a live item and the interface might have changed)
    #       The screen capture should have been reset to none
    #       The slide should have been added to the slide list with the correct index
    assert 1 == mocked_execute.call_count, 'Execute should have been called once'
    slide_controller.on_controller_size_changed.assert_called_once()
    assert slide_controller.screen_capture is None
    assert slide_controller.slide_list['Verse name'] == 0


@patch.object(Registry, 'execute')
def test_process_item_song_vlc(mocked_execute, registry, state_media):
    """
    Test that media is started if VLC is present.
    """
    # GIVEN: A mocked presentation service item, a mocked media service item, a mocked Registry.execute
    #        and a slide controller with many mocks.
    mocked_pres_item = MagicMock()
    mocked_pres_item.name = 'mocked_song_item'
    mocked_pres_item.is_command.return_value = False
    mocked_pres_item.is_media.return_value = True
    mocked_pres_item.is_image.return_value = False
    mocked_pres_item.from_service = False
    mocked_pres_item.get_frames.return_value = []
    mocked_media_item = MagicMock()
    mocked_media_item.name = 'mocked_media_item'
    mocked_media_item.is_command.return_value = True
    mocked_media_item.is_media.return_value = True
    mocked_media_item.is_image.return_value = False
    mocked_media_item.from_service = False
    mocked_media_item.get_frames.return_value = []
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('media_controller', MagicMock())
    Registry().register('application', MagicMock())
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_pres_item
    slide_controller.is_live = False
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_display = MagicMock()
    slide_controller.enable_tool_bar = MagicMock()
    slide_controller.slide_selected = MagicMock()
    slide_controller.on_stop_loop = MagicMock()
    slide_controller.info_label = MagicMock()
    slide_controller.displays = [MagicMock()]
    slide_controller.split = 0
    slide_controller.type_prefix = 'test'

    # WHEN: _process_item is called
    slide_controller._process_item(mocked_media_item, 0)

    # THEN: Registry.execute should have been called to stop the presentation
    assert 1 == slide_controller.media_controller.load_video.call_count, ' Load_video should have been called 1 times'
    assert 2 == slide_controller.preview_display.load_verses.call_count, 'Execute should have been called 2 times'


@patch.object(Registry, 'execute')
def test_process_item_song_no_vlc(mocked_execute, registry, state_media):
    """
    Test that media is started if VLC is present.
    """
    # GIVEN: A mocked presentation service item, a mocked media service item, a mocked Registry.execute
    #        and a slide controller with many mocks.
    State().update_pre_conditions("media", False)
    State().flush_preconditions()
    mocked_pres_item = MagicMock()
    mocked_pres_item.name = 'mocked_song_item'
    mocked_pres_item.is_command.return_value = False
    mocked_pres_item.is_media.return_value = True
    mocked_pres_item.is_image.return_value = False
    mocked_pres_item.from_service = False
    mocked_pres_item.get_frames.return_value = []
    mocked_media_item = MagicMock()
    mocked_media_item.name = 'mocked_media_item'
    mocked_media_item.is_command.return_value = True
    mocked_media_item.is_media.return_value = True
    mocked_media_item.is_image.return_value = False
    mocked_media_item.from_service = False
    mocked_media_item.get_frames.return_value = []
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    Registry().register('media_controller', MagicMock())
    Registry().register('application', MagicMock())
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_pres_item
    slide_controller.is_live = False
    slide_controller.preview_widget = MagicMock()
    slide_controller.preview_display = MagicMock()
    slide_controller.enable_tool_bar = MagicMock()
    slide_controller.slide_selected = MagicMock()
    slide_controller.on_stop_loop = MagicMock()
    slide_controller.info_label = MagicMock()
    slide_controller.displays = [MagicMock()]
    slide_controller.split = 0
    slide_controller.type_prefix = 'test'

    # WHEN: _process_item is called
    slide_controller._process_item(mocked_media_item, 0)

    # THEN: Registry.execute should have been called to stop the presentation
    assert 0 == slide_controller.media_controller.load_video.call_count, ' Load_video should have been called 0 times'
    assert 2 == slide_controller.preview_display.load_verses.call_count, 'Execute should have been called 2 times'


def test_live_stolen_focus_shortcuts(settings):
    """
    Test that all the needed shortcuts are available in scenarios where Live has stolen focus.
    These are found under def __add_actions_to_widget(self, widget): in slidecontroller.py
    """
    # GIVEN: A slide controller, actions needed
    slide_controller = SlideController(None)
    mocked_widget = MagicMock()
    slide_controller.previous_item = MagicMock()
    slide_controller.next_item = MagicMock()
    slide_controller.previous_service = MagicMock()
    slide_controller.next_service = MagicMock()
    slide_controller.show_screen = MagicMock()
    slide_controller.desktop_screen = MagicMock()
    slide_controller.blank_screen = MagicMock()
    slide_controller.theme_screen = MagicMock()

    # WHEN: __add_actions_to_widget is called
    slide_controller._SlideController__add_actions_to_widget(mocked_widget)

    # THEN: The call to addActions should be correct
    mocked_widget.addActions.assert_called_with([
        slide_controller.previous_item, slide_controller.next_item,
        slide_controller.previous_service, slide_controller.next_service,
        slide_controller.show_screen, slide_controller.desktop_screen,
        slide_controller.theme_screen, slide_controller.blank_screen
    ])


def test_on_preview_double_click_unblank_display(mock_settings):
    # GIVEN: A slide controller, actions needed, settings set to True.
    slide_controller = SlideController(None)
    mocked_settings = MagicMock()
    mocked_settings.return_value = True
    mock_settings.return_value = mocked_settings
    slide_controller.service_item = MagicMock()
    slide_controller.service_item.is_media = MagicMock()
    slide_controller.on_media_close = MagicMock()
    slide_controller.on_go_live = MagicMock()
    slide_controller.on_preview_add_to_service = MagicMock()
    slide_controller.media_reset = MagicMock()
    Registry().set_flag('has doubleclick added item to service', True)

    # WHEN: on_preview_double_click is called
    slide_controller.on_preview_double_click()

    # THEN: The call to addActions should be correct
    assert 1 == slide_controller.on_go_live.call_count, 'on_go_live should have been called once.'
    assert 0 == slide_controller.on_preview_add_to_service.call_count, 'Should have not been called.'


def test_on_preview_double_click_add_to_service(mock_settings):
    # GIVEN: A slide controller, actions needed, settings set to False.
    slide_controller = SlideController(None)
    mock_settings.value.return_value = False
    slide_controller.service_item = MagicMock()
    slide_controller.service_item.is_media = MagicMock()
    slide_controller.on_media_close = MagicMock()
    slide_controller.on_go_live = MagicMock()
    slide_controller.on_preview_add_to_service = MagicMock()
    slide_controller.media_reset = MagicMock()
    Registry().set_flag('has doubleclick added item to service', False)

    # WHEN: on_preview_double_click is called
    slide_controller.on_preview_double_click()

    # THEN: The call to addActions should be correct
    assert 0 == slide_controller.on_go_live.call_count, 'on_go_live Should have not been called.'
    assert 1 == slide_controller.on_preview_add_to_service.call_count, 'Should have been called once.'


@patch(u'PyQt5.QtCore.QTimer.singleShot')
def test_update_preview_live(mocked_singleShot, registry):
    """
    Test that the preview screen is updated with a screen grab for live service items
    """
    # GIVEN: A mocked live service item, a mocked Registry,
    #        and a slide controller with many mocks.
    # Mocked Live Item
    mocked_live_item = MagicMock()
    mocked_live_item.get_rendered_frame.return_value = ''
    mocked_live_item.is_capable = MagicMock()
    mocked_live_item.is_capable.side_effect = [True, True]
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    # Mock SlideController
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_live_item
    slide_controller.is_live = True
    slide_controller.log_debug = MagicMock()
    slide_controller.selected_row = MagicMock()
    slide_controller.screens = MagicMock()
    slide_controller.screens.current = {'primary': ''}
    slide_controller.displays = [MagicMock()]
    slide_controller.display.preview.return_value = QtGui.QImage()
    slide_controller.display_maindisplay = MagicMock()
    slide_controller.slide_preview = MagicMock()
    slide_controller.slide_count = 0
    slide_controller.slide_changed_time = datetime.datetime.now()

    # WHEN: update_preview is called
    slide_controller.update_preview()

    # THEN: A screen_grab should have been called
    assert 0 == slide_controller.slide_preview.setPixmap.call_count, 'setPixmap should not be called'
    assert 0 == slide_controller.display.preview.call_count, 'display.preview() should not be called'
    assert 2 == mocked_singleShot.call_count, 'Timer to display_maindisplay should have been called 2 times'


@patch(u'PyQt5.QtCore.QTimer.singleShot')
def test_update_preview_pres(mocked_singleShot, registry):
    """
    Test that the preview screen is updated with the correct preview for presentation service items
    """
    # GIVEN: A mocked presentation service item, a mocked Registry,
    #        and a slide controller with many mocks.
    # Mocked Presentation Item
    mocked_pres_item = MagicMock()
    mocked_pres_item.get_rendered_frame.return_value = ''
    mocked_pres_item.is_capable = MagicMock()
    mocked_pres_item.is_capable.side_effect = [True, True]
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    # Mock SlideController
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_pres_item
    slide_controller.is_live = False
    slide_controller.log_debug = MagicMock()
    slide_controller.selected_row = MagicMock()
    slide_controller.screens = MagicMock()
    slide_controller.screens.current = {'primary': ''}
    slide_controller.displays = [MagicMock()]
    slide_controller.display.preview.return_value = QtGui.QImage()
    slide_controller.display_maindisplay = MagicMock()
    slide_controller.slide_preview = MagicMock()
    slide_controller.slide_count = 0
    slide_controller.preview_display = MagicMock()

    # WHEN: update_preview is called
    slide_controller.update_preview()

    # THEN: setPixmap should have been called
    assert 1 == slide_controller.preview_display.set_single_image.call_count, 'set_single_image should be called'
    assert 0 == mocked_singleShot.call_count, 'Timer to display_maindisplay should not be called'


@patch(u'PyQt5.QtCore.QTimer.singleShot')
def test_update_preview_media(mocked_singleShot, registry):
    """
    Test that the preview screen is updated with the correct preview for media service items
    """
    # GIVEN: A mocked media service item, a mocked Registry,
    #        and a slide controller with many mocks.
    # Mocked Media Item
    mocked_media_item = MagicMock()
    mocked_media_item.get_rendered_frame.return_value = ''
    mocked_media_item.is_capable = MagicMock()
    mocked_media_item.is_capable.side_effect = [True, False]
    # Mock Registry
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    # Mock SlideController
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_media_item
    slide_controller.is_live = False
    slide_controller.log_debug = MagicMock()
    slide_controller.selected_row = MagicMock()
    slide_controller.screens = MagicMock()
    slide_controller.screens.current = {'primary': ''}
    slide_controller.displays = [MagicMock()]
    slide_controller.display.preview.return_value = QtGui.QImage()
    slide_controller.display_maindisplay = MagicMock()
    slide_controller.slide_preview = MagicMock()
    slide_controller.slide_count = 0
    slide_controller.preview_display = MagicMock()

    # WHEN: update_preview is called
    slide_controller.update_preview()

    # THEN: setPixmap should have been called
    assert 1 == slide_controller.preview_display.set_single_image.call_count, 'set_single_image should be called'
    assert 0 == mocked_singleShot.call_count, 'Timer to display_maindisplay should not be called'


@patch(u'PyQt5.QtCore.QTimer.singleShot')
def test_update_preview_image(mocked_singleShot, registry):
    """
    Test that the preview screen is updated with the correct preview for image service items
    """
    # GIVEN: A mocked image service item, a mocked Registry,
    #        and a slide controller with many mocks.
    # Mocked Image Item
    mocked_img_item = MagicMock()
    mocked_img_item.get_rendered_frame.return_value = ''
    mocked_img_item.is_capable = MagicMock()
    mocked_img_item.is_capable.side_effect = [False, True]
    # Mock Registry
    mocked_main_window = MagicMock()
    Registry().register('main_window', mocked_main_window)
    # Mock SlideController
    slide_controller = SlideController(None)
    slide_controller.service_item = mocked_img_item
    slide_controller.is_live = False
    slide_controller.log_debug = MagicMock()
    slide_controller.selected_row = MagicMock()
    slide_controller.screens = MagicMock()
    slide_controller.screens.current = {'primary': ''}
    slide_controller.displays = [MagicMock()]
    slide_controller.display_maindisplay = MagicMock()
    slide_controller.slide_preview = MagicMock()
    slide_controller.slide_count = 0
    slide_controller.preview_display = MagicMock()

    # WHEN: update_preview is called
    slide_controller.update_preview()

    # THEN: setPixmap and display.preview should have been called
    assert 1 == slide_controller.preview_display.go_to_slide.call_count, 'go_to_slide should be called'
    assert 0 == mocked_singleShot.call_count, 'Timer to display_maindisplay should not be called'


@patch(u'openlp.core.ui.slidecontroller.image_to_byte')
def test_display_maindisplay(mocked_image_to_byte, registry):
    """
    Test the display_maindisplay method
    Here a string is substituted for what would be a screen capture of the display
    The `image_to_byte` mocked funtion just adds " bytified" to the string
    """
    # GIVEN: A mocked slide controller, with mocked functions
    slide_controller = SlideController(None)
    slide_controller._capture_maindisplay = MagicMock(return_value='placeholder')
    slide_controller.preview_display = MagicMock()
    mocked_image_to_byte.side_effect = lambda x: '{} bytified'.format(x)

    # WHEN: display_maindisplay is called
    slide_controller.display_maindisplay()

    # THEN: Should have grabbed the maindisplay and set to placeholder with a black background
    slide_controller._capture_maindisplay.assert_called_once()
    slide_controller.preview_display.set_single_image_data.assert_called_once_with('#000', 'placeholder bytified')


@patch(u'openlp.core.ui.slidecontroller.image_to_byte')
@patch(u'openlp.core.ui.slidecontroller.ScreenList')
@patch(u'openlp.core.ui.slidecontroller.QtWidgets.QApplication')
def test__capture_maindisplay(mocked_application, mocked_screenlist, mocked_image_to_byte, registry):
    """
    Test the _capture_maindisplay method
    """
    # GIVEN: A mocked slide controller, with mocked functions
    slide_controller = SlideController(None)
    mocked_display_geometry = MagicMock(
        x=MagicMock(return_value=34),
        y=MagicMock(return_value=67),
        width=MagicMock(return_value=77),
        height=MagicMock(return_value=42)
    )
    mocked_screenlist_instance = MagicMock()
    mocked_screenlist.return_value = mocked_screenlist_instance
    mocked_screenlist_instance.current = MagicMock(display_geometry=mocked_display_geometry)
    mocked_primary_screen = MagicMock()
    mocked_application.primaryScreen = MagicMock(return_value=mocked_primary_screen)
    mocked_application.desktop = MagicMock(return_value=MagicMock(
        winId=MagicMock(return_value=23)
    ))
    slide_controller.preview_display = MagicMock()

    # WHEN: _capture_maindisplay is called
    slide_controller._capture_maindisplay()

    # THEN: Screenshot should have been taken with correct winId and dimensions
    mocked_primary_screen.grabWindow.assert_called_once_with(23, 34, 67, 77, 42)


@patch(u'openlp.core.ui.slidecontroller.image_to_byte')
def test_grab_maindisplay(mocked_image_to_byte, registry):
    """
    Test the grab_maindisplay method
    """
    # GIVEN: A mocked slide controller, with mocked functions
    slide_controller = SlideController(None)
    slide_controller._capture_maindisplay = MagicMock(return_value='placeholder')
    slide_controller.preview_display = MagicMock()
    slide_controller.fetching_screenshot = False
    slide_controller.screen_capture = None
    slide_controller.service_item = MagicMock(get_transition_delay=MagicMock(return_value=1))
    slide_controller.slide_changed_time = datetime.datetime.now() - datetime.timedelta(seconds=10)
    mocked_image_to_byte.side_effect = lambda x: '{} bytified'.format(x)

    # WHEN: grab_maindisplay is called
    grabbed_stuff = slide_controller.grab_maindisplay()

    # THEN: Should have grabbed the maindisplay and ran image_to_byte on it
    slide_controller._capture_maindisplay.assert_called_once()
    assert grabbed_stuff == 'placeholder bytified'


@patch(u'openlp.core.ui.slidecontroller.image_to_byte')
def test_grab_maindisplay_cached(mocked_image_to_byte, registry):
    """
    Test the grab_maindisplay method with pre-cached screenshot
    """
    # GIVEN: A mocked slide controller, with mocked functions
    slide_controller = SlideController(None)
    slide_controller._capture_maindisplay = MagicMock(return_value='placeholder')
    slide_controller.preview_display = MagicMock()
    slide_controller.fetching_screenshot = False
    slide_controller.screen_capture = 'cached screen_capture'
    mocked_image_to_byte.side_effect = lambda x: '{} bytified'.format(x)

    # WHEN: grab_maindisplay is called
    grabbed_stuff = slide_controller.grab_maindisplay()

    # THEN: Should have not grabbed the maindisplay and returned the cached image
    assert slide_controller._capture_maindisplay.call_count == 0
    assert grabbed_stuff == 'cached screen_capture'


def test_paint_event_text_fits():
    """
    Test the paintEvent method when text fits the label
    """
    font = QtGui.QFont()
    metrics = QtGui.QFontMetrics(font)

    with patch('openlp.core.ui.slidecontroller.QtWidgets.QLabel'), \
            patch('openlp.core.ui.slidecontroller.QtGui.QPainter') as mocked_qpainter:

        # GIVEN: An instance of InfoLabel, with mocked text return, width and rect methods
        info_label = InfoLabel()
        test_string = 'Label Text'
        mocked_rect = MagicMock()
        mocked_text = MagicMock()
        mocked_width = MagicMock()
        mocked_text.return_value = test_string
        info_label.rect = mocked_rect
        info_label.text = mocked_text
        info_label.width = mocked_width

        # WHEN: The instance is wider than its text, and the paintEvent method is called
        info_label.width.return_value = metrics.boundingRect(test_string).width() + 20
        info_label.paintEvent(MagicMock())

        # THEN: The text should be drawn left with the complete test_string
        mocked_qpainter().drawText.assert_called_once_with(mocked_rect(), QtCore.Qt.AlignLeft, test_string)


def test_paint_event_text_doesnt_fit():
    """
    Test the paintEvent method when text fits the label
    """
    font = QtGui.QFont()
    metrics = QtGui.QFontMetrics(font)

    with patch('openlp.core.ui.slidecontroller.QtWidgets.QLabel'), \
            patch('openlp.core.ui.slidecontroller.QtGui.QPainter') as mocked_qpainter:

        # GIVEN: An instance of InfoLabel, with mocked text return, width and rect methods
        info_label = InfoLabel()
        test_string = 'Label Text'
        mocked_rect = MagicMock()
        mocked_text = MagicMock()
        mocked_width = MagicMock()
        mocked_text.return_value = test_string
        info_label.rect = mocked_rect
        info_label.text = mocked_text
        info_label.width = mocked_width

        # WHEN: The instance is narrower than its text, and the paintEvent method is called
        label_width = metrics.boundingRect(test_string).width() - 20
        info_label.width.return_value = label_width
        info_label.paintEvent(MagicMock())

        # THEN: The text should be drawn aligned left with an elided test_string
        elided_test_string = metrics.elidedText(test_string, QtCore.Qt.ElideRight, label_width)
        mocked_qpainter().drawText.assert_called_once_with(mocked_rect(), QtCore.Qt.AlignLeft, elided_test_string)


@patch('builtins.super')
def test_set_text(mocked_super):
    """
    Test the reimplemented setText method
    """
    # GIVEN: An instance of InfoLabel and mocked setToolTip method
    info_label = InfoLabel()
    set_tool_tip_mock = MagicMock()
    info_label.setToolTip = set_tool_tip_mock

    # WHEN: Calling the instance method setText
    info_label.setText('Label Text')

    # THEN: The setToolTip and super class setText methods should have been called with the same text
    set_tool_tip_mock.assert_called_once_with('Label Text')
    mocked_super().setText.assert_called_once_with('Label Text')


def test_initial_live_controller(registry):
    """
    Test the initial live slide controller state .
    """
    # GIVEN: A new SlideController instance.
    live_controller = LiveController(None)

    # WHEN: the default controller is built.
    # THEN: The controller should not be a live controller.
    assert live_controller.is_live is True, 'The slide controller should be a live controller'


def test_initial_preview_controller(registry):
    """
    Test the initial preview slide controller state.
    """
    # GIVEN: A new SlideController instance.
    preview_controller = PreviewController(None)

    # WHEN: the default controller is built.
    # THEN: The controller should not be a live controller.
    assert preview_controller.is_live is False, 'The slide controller should be a Preview controller'
