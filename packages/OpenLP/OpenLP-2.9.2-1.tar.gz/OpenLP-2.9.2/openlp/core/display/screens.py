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
The :mod:`screen` module provides management functionality for a machines'
displays.
"""
import logging
import copy
from functools import cmp_to_key

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Singleton
from openlp.core.common.i18n import translate
from openlp.core.common.registry import Registry


log = logging.getLogger(__name__)


class Screen(object):
    """
    A Python representation of a screen
    """
    def __init__(self, number=None, geometry=None, custom_geometry=None, is_primary=False, is_display=False):
        """
        Set up the screen object

        :param int number: The Qt number of this screen
        :param QRect geometry: The geometry of this screen as a QRect object
        :param QRect custom_geometry: The custom geometry of this screen as a QRect object
        :param bool is_primary: Whether or not this screen is the primary screen
        :param bool is_display: Whether or not this screen should be used to display lyrics
        """
        self.number = int(number)
        self.geometry = geometry
        self.custom_geometry = custom_geometry
        self.is_primary = is_primary
        self.is_display = is_display

    def __str__(self):
        """
        Return a string for displaying this screen

        :return str: A nicely formatted string
        """
        name = '{screen} {number:d}'.format(screen=translate('OpenLP.ScreenList', 'Screen'), number=self.number + 1)
        if self.is_primary:
            name = '{name} ({primary})'.format(name=name, primary=translate('OpenLP.ScreenList', 'primary'))
        return name

    def __repr__(self):
        """
        Return a string representation of the object
        """
        return '<{screen}>'.format(screen=self)

    @property
    def display_geometry(self):
        """
        Returns the geometry to use when displaying. This property decides between the native and custom geometries
        """
        # If custom geometry is used, convert to absolute position
        if self.custom_geometry:
            adjusted_custom_geometry = copy.deepcopy(self.custom_geometry)
            adjusted_custom_geometry.moveTo(self.geometry.x() + adjusted_custom_geometry.x(),
                                            self.geometry.y() + adjusted_custom_geometry.y())
            return adjusted_custom_geometry
        else:
            return self.geometry

    @classmethod
    def from_dict(cls, screen_dict):
        """
        Create a screen object from a dictionary

        :param dict screen_dict: The dictionary from which to make the Screen object
        :return: A Screen object with the values from screen_dict
        :rtype: openlp.core.display.screens.Screen
        """
        screen_dict['geometry'] = QtCore.QRect(screen_dict['geometry']['x'], screen_dict['geometry']['y'],
                                               screen_dict['geometry']['width'], screen_dict['geometry']['height'])
        if 'custom_geometry' in screen_dict:
            screen_dict['custom_geometry'] = QtCore.QRect(screen_dict['custom_geometry']['x'],
                                                          screen_dict['custom_geometry']['y'],
                                                          screen_dict['custom_geometry']['width'],
                                                          screen_dict['custom_geometry']['height'])
        return cls(**screen_dict)

    def to_dict(self):
        """
        Convert a screen object to a dictionary

        :return: A dictionary of this screen
        :rtype: dict
        """
        screen_dict = {
            'number': self.number,
            'geometry': {
                'x': self.geometry.x(),
                'y': self.geometry.y(),
                'width': self.geometry.width(),
                'height': self.geometry.height()
            },
            'is_primary': self.is_primary,
            'is_display': self.is_display
        }
        if self.custom_geometry is not None:
            screen_dict['custom_geometry'] = {
                'x': self.custom_geometry.x(),
                'y': self.custom_geometry.y(),
                'width': self.custom_geometry.width(),
                'height': self.custom_geometry.height()
            }
        return screen_dict

    def update(self, screen_dict):
        """
        Update this instance from a dictionary

        :param dict screen_dict: The dictionary which we want to apply to the screen
        """
        self.number = int(screen_dict['number']) if 'number' in screen_dict else self.number
        self.is_display = screen_dict.get('is_display', self.is_display)
        self.is_primary = screen_dict.get('is_primary', self.is_primary)
        if 'geometry' in screen_dict:
            try:
                self.geometry = QtCore.QRect(screen_dict['geometry']['x'], screen_dict['geometry']['y'],
                                             screen_dict['geometry']['width'], screen_dict['geometry']['height'])
            except KeyError:
                # Preserve the current values as this has come from the settings update which does not have
                # the geometry information
                pass
        if 'custom_geometry' in screen_dict:
            self.custom_geometry = QtCore.QRect(screen_dict['custom_geometry']['x'],
                                                screen_dict['custom_geometry']['y'],
                                                screen_dict['custom_geometry']['width'],
                                                screen_dict['custom_geometry']['height'])

    def on_geometry_changed(self, geometry):
        """
        Callback function for when the screens geometry changes
        """
        self.geometry = geometry
        Registry().execute('config_screen_changed')


class ScreenList(metaclass=Singleton):
    """
    Wrapper to handle the parameters of the display screen.

    To get access to the screen list call ``ScreenList()``.
    """
    log.info('Screen loaded')
    screens = []

    def __iter__(self):
        """
        Convert this object into an iterable, so that we can iterate over it instead of the inner list
        """
        for screen in self.screens:
            yield screen

    def __getitem__(self, key):
        """
        Make sure this object is indexable, e.g. screen_list[1] => Screen(number=1)
        """
        for screen in self:
            if screen.number == key:
                return screen
        else:
            raise IndexError('No screen with number {number} in list'.format(number=key))

    def __len__(self):
        """
        Make sure we can call "len" on this object
        """
        return len(self.screens)

    @property
    def current(self):
        """
        Return the first "current" desktop

        NOTE: This is a HACK to ease the upgrade process
        """
        # Get the first display screen
        for screen in self.screens:
            if screen.is_display:
                return screen
        # If there's no display screen, get the first primary screen
        for screen in self.screens:
            if screen.is_primary:
                return screen
        # Otherwise just return the first screen
        if len(self.screens) > 0:
            return self.screens[0]
        else:
            return None

    @classmethod
    def create(cls, application):
        """
        Initialise the screen list.

        :param desktop:  A QApplication object.
        """
        screen_list = cls()
        screen_list.application = application
        screen_list.application.primaryScreenChanged.connect(screen_list.on_primary_screen_changed)
        screen_list.application.screenAdded.connect(screen_list.on_screen_added)
        screen_list.application.screenRemoved.connect(screen_list.on_screen_removed)
        screen_list.update_screens()
        cls.settings = Registry().get('settings')
        screen_list.load_screen_settings()
        return screen_list

    def find_new_display_screen(self):
        """
        If more than 1 screen, set first non-primary screen to display, otherwise just set the available screen as
        display.
        """
        if len(self) > 1:
            for screen in self:
                if not screen.is_primary:
                    screen.is_display = True
                    break
        else:
            self[0].is_display = True

    def load_screen_settings(self):
        """
        Loads the screen size and the screen number from the settings.
        """
        screen_settings = self.settings.value('core/screens')
        if screen_settings:
            need_new_display_screen = False
            for number, screen_dict in screen_settings.items():
                # Sometimes this loads as a string instead of an int
                number = int(number)
                # Compare geometry, primary of screen from settings with available screens
                if self.has_screen(screen_dict):
                    # If match was found, we're all happy, update with custom geometry, display info, if available
                    self[number].update(screen_dict)
                else:
                    # If no match, ignore this screen, also need to find new display screen if the discarded screen was
                    # marked as such.
                    if screen_dict['is_display']:
                        need_new_display_screen = True
            if need_new_display_screen:
                QtWidgets.QMessageBox.warning(None, translate('OpenLP.Screen',
                                                              'Screen settings and screen setup is not the same'),
                                              translate('OpenLP.Screen',
                                                        'There is a mismatch between screens and screen settings. '
                                                        'OpenLP will try to automatically select a display screen, but '
                                                        'you should consider updating the screen settings.'),
                                              QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Ok))
                self.find_new_display_screen()
        else:
            # if no settings we need to set a display
            self.find_new_display_screen()

    def save_screen_settings(self):
        """
        Saves the screen size and screen settings
        """
        self.settings.setValue('core/screens', {screen.number: screen.to_dict() for screen in self.screens})

    def get_display_screen_list(self):
        """
        Returns a list with the screens. This should only be used to display available screens to the user::

            ['Screen 1 (primary)', 'Screen 2']
        """
        screen_list = []
        for screen in self.screens:
            screen_name = '{name} {number:d}'.format(name=translate('OpenLP.ScreenList', 'Screen'),
                                                     number=screen.number + 1)
            if screen.is_primary:
                screen_name = '{name} ({primary})'.format(name=screen_name,
                                                          primary=translate('OpenLP.ScreenList', 'primary'))
            screen_list.append(screen_name)
        return screen_list

    def get_number_for_window(self, window):
        """
        Return the screen number that the centre of the passed window is in.

        :param window: A QWidget we are finding the location of.
        """
        for screen in self.screens:
            if screen.geometry == window.geometry() or screen.display_geometry == window.geometry():
                return screen
        return None

    def set_display_screen(self, number, can_save=False):
        """
        Set screen number ``number`` to be the display screen.

        At the moment, this is forced to be only a single screen, but later when we support multiple monitors it
        will need to be updated.

        :param int number: The number of the screen
        :param bool can_save: If the screen settings should be saved, defaults to False.
        """
        for screen in self.screens:
            if screen.number == number:
                screen.is_display = True
            else:
                screen.is_display = False
        if can_save:
            self.save_screen_settings()

    def has_screen(self, screen_dict):
        """
        Confirms a screen is known.

        :param screen_dict: The dict descrebing the screen.
        """
        for screen in self.screens:
            if screen.to_dict()['geometry'] == screen_dict['geometry'] \
                    and screen.is_primary == screen_dict['is_primary']:
                return True
        return False

    def update_screens(self):
        """
        Update the list of screens
        """
        def _screen_compare(this, other):
            """
            Compare screens. Can't use a key here because of the nested property and method to be called
            """
            if this.geometry().x() < other.geometry().x():
                return -1
            elif this.geometry().x() > other.geometry().x():
                return 1
            else:
                if this.geometry().y() < other.geometry().y():
                    return -1
                elif this.geometry().y() > other.geometry().y():
                    return 1
                else:
                    return 0
        self.screens = []
        os_screens = self.application.screens()
        os_screens.sort(key=cmp_to_key(_screen_compare))
        for number, screen in enumerate(os_screens):
            self.screens.append(
                Screen(number, screen.geometry(), is_primary=self.application.primaryScreen() == screen))
            screen.geometryChanged.connect(self.screens[-1].on_geometry_changed)

    def on_screen_added(self, changed_screen):
        """
        Called when a screen has been added

        :param changed_screen: The screen which has been plugged.
        """
        number = len(self.screens)
        self.screens.append(Screen(number, changed_screen.geometry(),
                                   is_primary=self.application.primaryScreen() == changed_screen))
        changed_screen.geometryChanged.connect(self.screens[-1].on_geometry_changed)
        Registry().execute('config_screen_changed')

    def on_screen_removed(self, removed_screen):
        """
        Called when a screen has been removed.

        :param changed_screen: The screen which has been unplugged.
        """
        # Remove screens
        removed_screen_number = -1
        for screen in self.screens:
            # once the screen that must be removed has been found, update numbering
            if removed_screen_number >= 0:
                screen.number -= 1
            # find the screen that is removed
            if removed_screen.geometry() == screen.geometry:
                removed_screen_number = screen.number
        removed_screen_is_display = self.screens[removed_screen_number].is_display
        self.screens.pop(removed_screen_number)
        if removed_screen_is_display:
            self.find_new_display_screen()
        Registry().execute('config_screen_changed')

    def on_primary_screen_changed(self):
        """
        The primary screen has changed, let's sort it out and then notify everyone
        """
        for screen in self.screens:
            screen.is_primary = self.application.primaryScreen().geometry() == screen.geometry
        Registry().execute('config_screen_changed')
