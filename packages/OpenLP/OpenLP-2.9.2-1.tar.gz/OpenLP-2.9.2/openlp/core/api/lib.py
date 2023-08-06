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
import json
from flask import jsonify, Response, request
from functools import wraps
from openlp.core.common.registry import Registry


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Registry().get('settings_thread').value('api/authentication enabled'):
            return f(*args, **kwargs)
        token = request.headers.get('Authorization', '')
        if token == Registry().get('authentication_token'):
            return f(*args, **kwargs)
        else:
            return '', 401
    return decorated


def old_success_response():
    return jsonify({'results': {'success': True}})


def extract_request(json_string, name):
    try:
        if json_string:
            return json.loads(json_string)['request'][name]
    except KeyError:
        pass
    return None


# ----------------------- OLD AUTH SECTION ---------------------
def check_auth(username, password):
    return Registry().get('settings_thread').value('api/user id') == username and \
        Registry().get('settings_thread').value('api/password') == password


def old_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not Registry().get('settings_thread').value('api/authentication enabled'):
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response('', 401, {'WWW-Authenticate': 'Basic realm="OpenLP Login Required"'})
        else:
            return f(*args, **kwargs)
    return decorated
