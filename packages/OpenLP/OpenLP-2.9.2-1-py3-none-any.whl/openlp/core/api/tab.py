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
The :mod:`~openlp.core.api.tab` module contains the settings tab for the API
"""
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets

from openlp.core.api.deploy import download_and_check, download_version_info
from openlp.core.common import get_network_interfaces
from openlp.core.common.i18n import translate
from openlp.core.common.registry import Registry
from openlp.core.lib.settingstab import SettingsTab
from openlp.core.ui.icons import UiIcons
from openlp.core.widgets.dialogs import DownloadProgressDialog


ZERO_URL = '0.0.0.0'


class ApiTab(SettingsTab):
    """
    RemoteTab is the Remotes settings tab in the settings dialog.
    """
    def __init__(self, parent):
        self.icon_path = UiIcons().remote
        advanced_translated = translate('OpenLP.APITab', 'API')
        self._master_version = None
        super(ApiTab, self).__init__(parent, 'api', advanced_translated)

    def setup_ui(self):
        self.setObjectName('ApiTab')
        super(ApiTab, self).setup_ui()
        self.server_settings_group_box = QtWidgets.QGroupBox(self.left_column)
        self.server_settings_group_box.setObjectName('server_settings_group_box')
        self.server_settings_layout = QtWidgets.QFormLayout(self.server_settings_group_box)
        self.server_settings_layout.setObjectName('server_settings_layout')
        self.address_label = QtWidgets.QLabel(self.server_settings_group_box)
        self.address_label.setObjectName('address_label')
        self.address_edit = QtWidgets.QLineEdit(self.server_settings_group_box)
        self.address_edit.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.address_edit.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'),
                                       self))
        self.address_edit.setObjectName('address_edit')
        self.server_settings_layout.addRow(self.address_label, self.address_edit)
        self.twelve_hour_check_box = QtWidgets.QCheckBox(self.server_settings_group_box)
        self.twelve_hour_check_box.setObjectName('twelve_hour_check_box')
        self.server_settings_layout.addRow(self.twelve_hour_check_box)
        self.thumbnails_check_box = QtWidgets.QCheckBox(self.server_settings_group_box)
        self.thumbnails_check_box.setObjectName('thumbnails_check_box')
        self.server_settings_layout.addRow(self.thumbnails_check_box)
        self.left_layout.addWidget(self.server_settings_group_box)
        self.http_settings_group_box = QtWidgets.QGroupBox(self.left_column)
        self.http_settings_group_box.setObjectName('http_settings_group_box')
        self.http_setting_layout = QtWidgets.QFormLayout(self.http_settings_group_box)
        self.http_setting_layout.setObjectName('http_setting_layout')
        self.port_label = QtWidgets.QLabel(self.http_settings_group_box)
        self.port_label.setObjectName('port_label')
        self.port_spin_box = QtWidgets.QLabel(self.http_settings_group_box)
        self.port_spin_box.setObjectName('port_spin_box')
        self.http_setting_layout.addRow(self.port_label, self.port_spin_box)
        self.remote_url_label = QtWidgets.QLabel(self.http_settings_group_box)
        self.remote_url_label.setObjectName('remote_url_label')
        self.remote_url = QtWidgets.QLabel(self.http_settings_group_box)
        self.remote_url.setObjectName('remote_url')
        self.remote_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.remote_url_label, self.remote_url)
        self.stage_url_label = QtWidgets.QLabel(self.http_settings_group_box)
        self.stage_url_label.setObjectName('stage_url_label')
        self.stage_url = QtWidgets.QLabel(self.http_settings_group_box)
        self.stage_url.setObjectName('stage_url')
        self.stage_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.stage_url_label, self.stage_url)
        self.chords_url_label = QtWidgets.QLabel(self.http_settings_group_box)
        self.chords_url_label.setObjectName('chords_url_label')
        self.chords_url = QtWidgets.QLabel(self.http_settings_group_box)
        self.chords_url.setObjectName('chords_url')
        self.chords_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.chords_url_label, self.chords_url)
        self.live_url_label = QtWidgets.QLabel(self.http_settings_group_box)
        self.live_url_label.setObjectName('live_url_label')
        self.live_url = QtWidgets.QLabel(self.http_settings_group_box)
        self.live_url.setObjectName('live_url')
        self.live_url.setOpenExternalLinks(True)
        self.http_setting_layout.addRow(self.live_url_label, self.live_url)
        self.left_layout.addWidget(self.http_settings_group_box)
        self.user_login_group_box = QtWidgets.QGroupBox(self.left_column)
        self.user_login_group_box.setCheckable(True)
        self.user_login_group_box.setChecked(False)
        self.user_login_group_box.setObjectName('user_login_group_box')
        self.user_login_layout = QtWidgets.QFormLayout(self.user_login_group_box)
        self.user_login_layout.setObjectName('user_login_layout')
        self.user_id_label = QtWidgets.QLabel(self.user_login_group_box)
        self.user_id_label.setObjectName('user_id_label')
        self.user_id = QtWidgets.QLineEdit(self.user_login_group_box)
        self.user_id.setObjectName('user_id')
        self.user_login_layout.addRow(self.user_id_label, self.user_id)
        self.password_label = QtWidgets.QLabel(self.user_login_group_box)
        self.password_label.setObjectName('password_label')
        self.password = QtWidgets.QLineEdit(self.user_login_group_box)
        self.password.setObjectName('password')
        self.user_login_layout.addRow(self.password_label, self.password)
        self.left_layout.addWidget(self.user_login_group_box)
        self.web_remote_group_box = QtWidgets.QGroupBox(self.left_column)
        self.web_remote_group_box.setObjectName('web_remote_group_box')
        self.web_remote_layout = QtWidgets.QGridLayout(self.web_remote_group_box)
        self.web_remote_layout.setObjectName('web_remote_layout')
        self.current_version_label = QtWidgets.QLabel(self.web_remote_group_box)
        self.web_remote_layout.addWidget(self.current_version_label, 0, 0)
        self.current_version_label.setObjectName('current_version_label')
        self.current_version_value = QtWidgets.QLabel(self.web_remote_group_box)
        self.current_version_value.setObjectName('current_version_value')
        self.web_remote_layout.addWidget(self.current_version_value, 0, 1)
        self.upgrade_button = QtWidgets.QPushButton(self.web_remote_group_box)
        self.upgrade_button.setEnabled(False)
        self.upgrade_button.setObjectName('upgrade_button')
        self.web_remote_layout.addWidget(self.upgrade_button, 0, 2)
        self.master_version_label = QtWidgets.QLabel(self.web_remote_group_box)
        self.master_version_label.setObjectName('master_version_label')
        self.web_remote_layout.addWidget(self.master_version_label, 1, 0)
        self.master_version_value = QtWidgets.QLabel(self.web_remote_group_box)
        self.master_version_value.setObjectName('master_version_value')
        self.web_remote_layout.addWidget(self.master_version_value, 1, 1)
        self.check_version_button = QtWidgets.QPushButton(self.web_remote_group_box)
        self.check_version_button.setObjectName('check_version_button')
        self.web_remote_layout.addWidget(self.check_version_button, 1, 2)
        self.left_layout.addWidget(self.web_remote_group_box)
        self.app_group_box = QtWidgets.QGroupBox(self.right_column)
        self.app_group_box.setObjectName('app_group_box')
        self.right_layout.addWidget(self.app_group_box)
        self.app_qr_layout = QtWidgets.QVBoxLayout(self.app_group_box)
        self.app_qr_layout.setObjectName('app_qr_layout')
        self.app_qr_code_label = QtWidgets.QLabel(self.app_group_box)
        self.app_qr_code_label.setPixmap(QtGui.QPixmap(':/remotes/app_qr.svg'))
        self.app_qr_code_label.setAlignment(QtCore.Qt.AlignCenter)
        self.app_qr_code_label.setObjectName('app_qr_code_label')
        self.app_qr_layout.addWidget(self.app_qr_code_label)
        self.app_qr_description_label = QtWidgets.QLabel(self.app_group_box)
        self.app_qr_description_label.setObjectName('app_qr_description_label')
        self.app_qr_description_label.setOpenExternalLinks(True)
        self.app_qr_description_label.setWordWrap(True)
        self.app_qr_layout.addWidget(self.app_qr_description_label)
        self.left_layout.addStretch()
        self.right_layout.addStretch()
        self.twelve_hour_check_box.stateChanged.connect(self.on_twelve_hour_check_box_changed)
        self.thumbnails_check_box.stateChanged.connect(self.on_thumbnails_check_box_changed)
        self.address_edit.textChanged.connect(self.set_urls)
        self.upgrade_button.clicked.connect(self.on_upgrade_button_clicked)
        self.check_version_button.clicked.connect(self.on_check_version_button_clicked)

    def retranslate_ui(self):
        self.tab_title_visible = translate('RemotePlugin.RemoteTab', 'Remote Interface')
        self.server_settings_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'Server Settings'))
        self.address_label.setText(translate('RemotePlugin.RemoteTab', 'IP address:'))
        self.port_label.setText(translate('RemotePlugin.RemoteTab', 'Port number:'))
        self.remote_url_label.setText(translate('RemotePlugin.RemoteTab', 'Remote URL:'))
        self.stage_url_label.setText(translate('RemotePlugin.RemoteTab', 'Stage view URL:'))
        self.live_url_label.setText(translate('RemotePlugin.RemoteTab', 'Live view URL:'))
        self.chords_url_label.setText(translate('RemotePlugin.RemoteTab', 'Chords view URL:'))
        self.twelve_hour_check_box.setText(translate('RemotePlugin.RemoteTab', 'Display stage time in 12h format'))
        self.thumbnails_check_box.setText(translate('RemotePlugin.RemoteTab',
                                                    'Show thumbnails of non-text slides in remote and stage view.'))
        self.app_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'Remote App'))
        self.app_qr_description_label.setText(
            translate('RemotePlugin.RemoteTab',
                      'Scan the QR code or click <a href="{qr}">download</a> to download an app for your mobile device'
                      ).format(qr='https://openlp.org/#mobile-app-downloads'))
        self.user_login_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'User Authentication'))
        self.web_remote_group_box.setTitle(translate('RemotePlugin.RemoteTab', 'Web Remote'))
        self.check_version_button.setText(translate('RemotePlugin.RemoteTab', 'Check for Updates'))
        self.upgrade_button.setText(translate('RemotePlugin.RemoteTab', 'Upgrade'))
        self.user_id_label.setText(translate('RemotePlugin.RemoteTab', 'User id:'))
        self.password_label.setText(translate('RemotePlugin.RemoteTab', 'Password:'))
        self.current_version_label.setText(translate('RemotePlugin.RemoteTab', 'Current version:'))
        self.master_version_label.setText(translate('RemotePlugin.RemoteTab', 'Latest version:'))
        self._unknown_version = translate('RemotePlugin.RemoteTab', '(unknown)')

    @property
    def master_version(self):
        """
        Property getter for the remote master version
        """
        return self._master_version

    @master_version.setter
    def master_version(self, value):
        """
        Property setter for the remote master version
        """
        self._master_version = value
        self.master_version_value.setText(self._master_version or self._unknown_version)
        self.upgrade_button.setEnabled(self.can_enable_upgrade_button())

    def can_enable_upgrade_button(self):
        """
        Do a couple checks to set the upgrade button state
        """
        return self.master_version_value.text() != self._unknown_version and \
            self.master_version_value.text() != self.current_version_value.text()

    def set_master_version(self):
        """
        Check if the master version is not set, and set it to None to invoke the "unknown version" label
        """
        if not self._master_version:
            self.master_version = None

    def set_urls(self):
        """
        Update the display based on the data input on the screen
        """
        ip_address = self.get_ip_address(self.address_edit.text())
        http_url = 'http://{url}:{text}/'.format(url=ip_address, text=self.port_spin_box.text())
        self.remote_url.setText('<a href="{url}">{url}</a>'.format(url=http_url))
        http_url_temp = http_url + 'stage'
        self.stage_url.setText('<a href="{url}">{url}</a>'.format(url=http_url_temp))
        http_url_temp = http_url + 'chords'
        self.chords_url.setText('<a href="{url}">{url}</a>'.format(url=http_url_temp))
        http_url_temp = http_url + 'main'
        self.live_url.setText('<a href="{url}">{url}</a>'.format(url=http_url_temp))

    def get_ip_address(self, ip_address):
        """
        returns the IP address in dependency of the passed address
        ip_address == 0.0.0.0: return the IP address of the first valid interface
        else: return ip_address
        """
        if ip_address == ZERO_URL:
            # In case we have more than one interface
            for _, interface in get_network_interfaces().items():
                ip_address = interface['ip']
                # We only want the first interface returned
                break
        return ip_address

    def load(self):
        """
        Load the configuration and update the server configuration if necessary
        """
        self.port_spin_box.setText(str(self.settings.value('api/port')))
        self.address_edit.setText(self.settings.value('api/ip address'))
        self.twelve_hour = self.settings.value('api/twelve hour')
        self.twelve_hour_check_box.setChecked(self.twelve_hour)
        self.thumbnails = self.settings.value('api/thumbnails')
        self.thumbnails_check_box.setChecked(self.thumbnails)
        self.user_login_group_box.setChecked(self.settings.value('api/authentication enabled'))
        self.user_id.setText(self.settings.value('api/user id'))
        self.password.setText(self.settings.value('api/password'))
        self.current_version_value.setText(self.settings.value('api/download version'))
        self.set_master_version()
        self.set_urls()

    def save(self):
        """
        Save the configuration and update the server configuration if necessary
        """
        if self.settings.value('api/ip address') != self.address_edit.text():
            self.settings_form.register_post_process('remotes_config_updated')
        self.settings.setValue('api/ip address', self.address_edit.text())
        self.settings.setValue('api/twelve hour', self.twelve_hour)
        self.settings.setValue('api/thumbnails', self.thumbnails)
        self.settings.setValue('api/authentication enabled', self.user_login_group_box.isChecked())
        self.settings.setValue('api/user id', self.user_id.text())
        self.settings.setValue('api/password', self.password.text())

    def on_twelve_hour_check_box_changed(self, check_state):
        """
        Toggle the 12 hour check box.
        """
        self.twelve_hour = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.twelve_hour = True

    def on_thumbnails_check_box_changed(self, check_state):
        """
        Toggle the thumbnail check box.
        """
        self.thumbnails = False
        # we have a set value convert to True/False
        if check_state == QtCore.Qt.Checked:
            self.thumbnails = True

    def on_check_version_button_clicked(self):
        """
        Check for the latest version on the server
        """
        app = Registry().get('application')
        app.set_busy_cursor()
        app.process_events()
        version_info = download_version_info()
        app.process_events()
        self.master_version = version_info['latest']['version']
        app.process_events()
        app.set_normal_cursor()
        app.process_events()
        if self.can_enable_upgrade_button():
            Registry().get('main_window').information_message('New version available!',
                                                              'There\'s a new version of the web remote available.')

    def on_upgrade_button_clicked(self):
        """
        Download/upgrade the web remote
        """
        app = Registry().get('application')
        progress = DownloadProgressDialog(self, app)
        progress.show()
        app.process_events()
        sleep(0.5)
        downloaded_version = download_and_check(progress)
        app.process_events()
        sleep(0.5)
        progress.close()
        app.process_events()
        self.current_version_value.setText(downloaded_version)
        self.settings.setValue('api/download version', downloaded_version)
        self.upgrade_button.setEnabled(self.can_enable_upgrade_button())
