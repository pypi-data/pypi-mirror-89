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
The :mod:`openlp.core.version` module downloads the version details for OpenLP.
"""
import logging
import platform
import sys
from collections import OrderedDict
from datetime import date

from PyQt5 import QtCore

from openlp.core.common.applocation import AppLocation
from openlp.core.common.httputils import get_web_page
from openlp.core.common.registry import Registry
from openlp.core.threading import ThreadWorker, run_thread


log = logging.getLogger(__name__)

APPLICATION_VERSION = {}
CONNECTION_TIMEOUT = 30
CONNECTION_RETRIES = 2
LIBRARIES = OrderedDict([
    ('Python', ('platform', 'python_version')),
    ('PyQt5', ('PyQt5.Qt', 'PYQT_VERSION_STR')),
    ('SQLAlchemy', ('sqlalchemy',)),
    ('Alembic', ('alembic',)),
    ('BeautifulSoup', ('bs4',)),
    ('lxml', ('lxml.etree',)),
    ('Chardet', ('chardet',)),
    ('PyEnchant', ('enchant',)),
    ('Mako', ('mako',)),
    ('VLC', ('openlp.core.ui.media.vlcplayer', 'VERSION')),
])
VERSION_BASE_URL = 'https://get.openlp.org/versions/'
VERSION_STABLE = 'version.txt'
VERSION_DEVELOP = 'dev_version.txt'
VERSION_NIGHTLY = 'nightly_version.txt'


class VersionWorker(ThreadWorker):
    """
    A worker class to fetch the version of OpenLP from the website. This is run from within a thread so that it
    doesn't affect the loading time of OpenLP.
    """
    new_version = QtCore.pyqtSignal(str)
    no_internet = QtCore.pyqtSignal()

    def __init__(self, last_check_date, current_version):
        """
        Constructor for the version check worker.

        :param string last_check_date: The last day we checked for a new version of OpenLP
        """
        log.debug('VersionWorker - Initialise')
        super(VersionWorker, self).__init__(None)
        self.last_check_date = last_check_date
        self.current_version = current_version

    def start(self):
        """
        Check the latest version of OpenLP against the version file on the OpenLP site.

        **Rules around versions and version files:**

        * If a version number has a revision hash (i.e. g9034d140b), then it is a nightly.
        * If a version number's minor version is an odd number, it is a development release.
        * If a version number's minor version is an even number, it is a stable release.
        """
        log.debug('VersionWorker - Start')
        download_url = VERSION_BASE_URL
        if self.current_version['build']:
            download_url += VERSION_NIGHTLY
        elif int(self.current_version['version'].split('.')[1]) % 2 != 0:
            download_url += VERSION_DEVELOP
        else:
            download_url += VERSION_STABLE
        headers = {
            'User-Agent': 'OpenLP/{version} {system}/{release}; '.format(version=self.current_version['full'],
                                                                         system=platform.system(),
                                                                         release=platform.release())
        }
        remote_version = None
        retries = 0
        while retries < 3:
            try:
                response = get_web_page(download_url, headers=headers)
                if response:
                    remote_version = response.strip()
                log.debug('New version found: %s', remote_version)
                break
            except OSError:
                log.exception('Unable to connect to OpenLP server to download version file')
                retries += 1
        else:
            self.no_internet.emit()
        if remote_version and (QtCore.QVersionNumber.fromString(remote_version) >
                               QtCore.QVersionNumber.fromString(self.current_version['full'])):
            self.new_version.emit(remote_version)
        self.quit.emit()


def update_check_date():
    """
    Save when we last checked for an update
    """
    Registry().get('settings').setValue('core/last version test', date.today().strftime('%Y-%m-%d'))


def check_for_update(main_window):
    """
    Run a thread to download and check the version of OpenLP

    :param MainWindow main_window: The OpenLP main window.
    """
    last_check_date = Registry().get('settings').value('core/last version test')
    if date.today().strftime('%Y-%m-%d') <= last_check_date:
        log.debug('Version check skipped, last checked today')
        return
    worker = VersionWorker(last_check_date, get_version())
    worker.new_version.connect(main_window.on_new_version)
    worker.quit.connect(update_check_date)
    # TODO: Use this to figure out if there's an Internet connection?
    # worker.no_internet.connect(parent.on_no_internet)
    run_thread(worker, 'version')


def get_version():
    """
    Returns the application version of the running instance of OpenLP::

        {'full': '2.9.0.dev2963+97ba02d1f', 'version': '2.9.0', 'build': '97ba02d1f'}
        or
        {'full': '2.9.0', 'version': '2.9.0', 'build': None}
    """
    global APPLICATION_VERSION
    if APPLICATION_VERSION:
        return APPLICATION_VERSION
    file_path = AppLocation.get_directory(AppLocation.VersionDir) / '.version'
    try:
        full_version = file_path.read_text().rstrip()
    except OSError:
        log.exception('Error in version file.')
        full_version = '0.0.0'
    bits = full_version.split('.dev')
    APPLICATION_VERSION = {
        'full': full_version,
        'version': bits[0],
        'build': full_version.split('+')[1] if '+' in full_version else None
    }
    if APPLICATION_VERSION['build']:
        log.info('OpenLP version {version} build {build}'.format(version=APPLICATION_VERSION['version'],
                                                                 build=APPLICATION_VERSION['build']))
    else:
        log.info('OpenLP version {version}'.format(version=APPLICATION_VERSION['version']))
    return APPLICATION_VERSION


def _get_lib_version(library, version_attr='__version__'):
    """
    Import a library and return the value of its version attribute.

    :param str library: The name of the library to import
    :param str version_attr: The name of the attribute containing the version number. Defaults to '__version__'
    :returns str: The version number as a string
    """
    if library not in sys.modules:
        try:
            __import__(library)
        except ImportError:
            return None
    if not hasattr(sys.modules[library], version_attr):
        return 'OK'
    else:
        attr = getattr(sys.modules[library], version_attr)
        if callable(attr):
            return str(attr())
        else:
            return str(attr)


def get_library_versions():
    """
    Read and return the versions of the libraries we use.

    :returns OrderedDict: A dictionary of {'library': 'version'}
    """
    library_versions = OrderedDict([(library, _get_lib_version(*args)) for library, args in LIBRARIES.items()])
    # Just update the dict for display purposes, changing the None to a '-'
    for library, version in library_versions.items():
        if version is None:
            library_versions[library] = '-'
    return library_versions
