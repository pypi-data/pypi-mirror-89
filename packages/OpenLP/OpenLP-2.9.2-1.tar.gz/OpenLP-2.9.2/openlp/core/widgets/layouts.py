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
The :mod:`~openlp.core.widgets.layouts` module contains customised layout classes
"""
from PyQt5 import QtCore, QtWidgets


class AspectRatioLayout(QtWidgets.QLayout):
    """
    A layout that contains a single widget and maintains the aspect ratio of the widget

    This is based on the C++ example here: https://gist.github.com/pavel-perina/1324ff064aedede0e01311aab315f83d
    """
    resize = QtCore.pyqtSignal(QtCore.QSize)

    def __init__(self, parent=None, aspect_ratio=None):
        """
        Create a layout.

        :param QtWidgets.QWidget | None parent: The parent widget
        :param float aspect_ratio: The aspect ratio as a float (e.g. 16.0/9.0)
        """
        super().__init__(parent)
        self._aspect_ratio = aspect_ratio
        self._item = None
        self._margin = 0
        self.setContentsMargins(0, 0, 0, 0)

    def get_aspect_ratio(self):
        """
        Return the aspect ratio

        :return: The aspect ration
        :rtype: float
        """
        return self._aspect_ratio

    def set_aspect_ratio(self, aspect_ratio):
        """
        Set the aspect ratio

        :param float aspect_ratio: The aspect ratio to set
        """
        self._aspect_ratio = aspect_ratio
        # Update the layout/widget
        geo = self.geometry()
        self.setGeometry(geo)

    aspect_ratio = property(get_aspect_ratio, set_aspect_ratio)

    def get_margin(self):
        """
        Return the margin

        :return: The margin
        :rtype: int
        """
        return self._margin

    def set_margin(self, value):
        """
        Set the margin

        :param int value: The margin
        """
        self._margin = int(value)

    margin = property(get_margin, set_margin)

    def count(self):
        """
        Overridden Qt method
        """
        return 1 if self._item else 0

    def addItem(self, item):
        """
        Overridden Qt method
        """
        if self._item is not None:
            raise ValueError('AspectRatioLayout can contain only 1 widget')
        self._item = item
        # self._item.setAlignment(0)

    def itemAt(self, index):
        """
        Overridden Qt method
        """
        if index != 0:
            return None
        return self._item

    def takeAt(self, index):
        """
        Overridden Qt method
        """
        if index != 0:
            return None
        result = self._item
        self._item = None
        return result

    def expandingDirections(self):
        """
        Overridden Qt method
        """
        return QtCore.Qt.Horizontal | QtCore.Qt.Vertical

    def hasHeightForWidth(self):
        """
        Overridden Qt method
        """
        return False

    def heightForWidth(self, width):
        """
        Overridden Qt method
        """
        height = (width - 2 * self.margin) / (self._aspect_ratio + 2 * self.margin)
        return height

    def setGeometry(self, rect):
        """
        Overridden Qt method
        """
        super().setGeometry(rect)
        if self._item:
            widget = self._item.widget()
            available_width = rect.width() - 2 * self.margin
            available_height = rect.height() - 2 * self.margin
            height = available_height
            width = height * self._aspect_ratio
            if width > available_width:
                width = available_width
                height = width / self._aspect_ratio
                if self._item.alignment() & QtCore.Qt.AlignTop:
                    y = self.margin
                elif self._item.alignment() & QtCore.Qt.AlignBottom:
                    y = rect.height() - self.margin - height
                else:
                    y = self.margin + (available_height - height) / 2
                widget.setGeometry(rect.x() + self.margin, rect.y() + y, width, height)
            else:
                if self._item.alignment() & QtCore.Qt.AlignLeft:
                    x = self.margin
                elif self._item.alignment() & QtCore.Qt.AlignRight:
                    x = rect.width() - self.margin - width
                else:
                    x = self.margin + (available_width - width) / 2
                widget.setGeometry(rect.x() + int(x), rect.y() + self.margin, width, height)
            self.resize.emit(QtCore.QSize(width, height))

    def sizeHint(self):
        """
        Overridden Qt method
        """
        margins = 2 * self.margin
        return self._item.sizeHint() + QtCore.QSize(margins, margins) \
            if self._item else QtCore.QSize(margins, margins)

    def minimumSize(self):
        """
        Overridden Qt method
        """
        margins = 2 * self.margin
        return self._item.minimumSize() + QtCore.QSize(margins, margins) \
            if self._item else QtCore.QSize(margins, margins)
