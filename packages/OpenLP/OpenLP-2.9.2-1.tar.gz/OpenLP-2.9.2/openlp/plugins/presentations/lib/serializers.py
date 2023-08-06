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
This module contains some helpers for serializing Path objects in Pyro4
"""
from openlp.core.common.path import Path

from Pyro4.util import SerializerBase


def path_class_to_dict(obj):
    """
    Serialize a Path object for Pyro4
    """
    return {
        '__class__': 'Path',
        'parts': obj.parts
    }


def path_dict_to_class(classname, d):
    return Path(*d['parts'])


def register_classes():
    """
    Register the serializers
    """
    SerializerBase.register_class_to_dict(Path, path_class_to_dict)
    SerializerBase.register_dict_to_class('Path', path_dict_to_class)
