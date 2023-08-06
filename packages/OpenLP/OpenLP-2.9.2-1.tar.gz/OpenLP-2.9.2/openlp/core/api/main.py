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

import os

from flask import Blueprint, send_from_directory
from openlp.core.common.applocation import AppLocation

main_views = Blueprint('main', __name__)


@main_views.route('/', defaults={'path': ''})
@main_views.route('/<path>')
def index(path):
    if os.path.isfile(AppLocation.get_section_data_path('remotes') / path):
        return send_from_directory(str(AppLocation.get_section_data_path('remotes')), path)
    else:
        return send_from_directory(str(AppLocation.get_section_data_path('remotes')), 'index.html')


@main_views.route('/assets/<path>')
def assets(path):
    return send_from_directory(str(AppLocation.get_section_data_path('remotes') / 'assets'), path)


@main_views.route('/stage/<path>/')
def stages(path):
    return send_from_directory(str(AppLocation.get_section_data_path('stages') / path), 'stage.html')


@main_views.route('/stage/<path>/<file>')
def stage_assets(path, file):
    return send_from_directory(str(AppLocation.get_section_data_path('stages') / path), file)
