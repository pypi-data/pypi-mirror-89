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
The splash screen
"""

from PyQt5 import QtCore, QtGui, QtWidgets


class SplashScreen(QtWidgets.QSplashScreen):
    """
    The splash screen
    """
    def __init__(self):
        """
        Constructor
        """
        super(SplashScreen, self).__init__()
        self.setup_ui()

    def setup_ui(self):
        """
        Set up the UI
        """
        self.setObjectName('splashScreen')
        self.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        splash_image = QtGui.QPixmap(':/graphics/openlp-splash-screen.png')
        self.setPixmap(splash_image)
        self.setMask(splash_image.mask())
        self.resize(370, 370)
