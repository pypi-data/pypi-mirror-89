# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2019 OpenLP Developers                              #
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
import logging

from openlp.core.api.endpoint.core import TRANSLATED_STRINGS
from openlp.core.api.http.endpoint import Endpoint


log = logging.getLogger(__name__)

remote_endpoint = Endpoint('remote', template_dir='remotes')


@remote_endpoint.route('{view}')
def index(request, view):
    """
    Handles requests for /remotes url

    :param request: The http request object.
    :param view: The view name to be servered.
    """
    return remote_endpoint.render_template('{view}.mako'.format(view=view), **TRANSLATED_STRINGS)
