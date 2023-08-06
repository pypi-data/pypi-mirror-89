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

import logging

from PyQt5 import QtWidgets

from openlp.core.common.i18n import translate
from openlp.plugins.media.forms import StreamSelectorFormBase, VLCOptionsWidget

log = logging.getLogger(__name__)


class NetworkStreamSelectorForm(StreamSelectorFormBase):
    """
    Class to manage the network stream selection
    """
    log.info('{name} NetworkStreamSelectorForm loaded'.format(name=__name__))

    def __init__(self, parent, callback, theme_stream=False):
        """
        Constructor
        """
        super(NetworkStreamSelectorForm, self).__init__(parent, callback, theme_stream)
        self.type = 'networkstream'
        self.setup_ui()

    def setup_ui(self):
        self.net_mrl_label = QtWidgets.QLabel(self)
        self.net_mrl_label.setObjectName('net_mrl_label')
        self.net_mrl_lineedit = QtWidgets.QLineEdit(self)
        self.net_mrl_lineedit.setObjectName('net_mrl_lineedit')
        self.top_layout.addRow(self.net_mrl_label, self.net_mrl_lineedit)
        self.main_layout.addWidget(self.top_widget)

        # Add groupbox for VLC options
        self.more_options_group = VLCOptionsWidget(self)
        # Add groupbox for more options to main layout
        self.main_layout.addWidget(self.more_options_group)
        # Save and close buttons
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.addButton(QtWidgets.QDialogButtonBox.Save)
        self.button_box.addButton(QtWidgets.QDialogButtonBox.Close)
        self.close_button = self.button_box.button(QtWidgets.QDialogButtonBox.Close)
        self.save_button = self.button_box.button(QtWidgets.QDialogButtonBox.Save)
        self.main_layout.addWidget(self.button_box)

        # translate
        self.retranslate_ui()
        # connect
        self.net_mrl_lineedit.editingFinished.connect(self.on_updates)
        self.more_options_group.caching.valueChanged.connect(self.on_updates)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def retranslate_ui(self):
        self.setWindowTitle(translate('MediaPlugin.StreamSelector', 'Insert Input Stream'))
        if not self.theme_stream:
            self.stream_name_label.setText(translate('MediaPlugin.StreamSelector', 'Stream name'))
        self.net_mrl_label.setText(translate('MediaPlugin.StreamSelector', 'Network URL'))

    def on_updates(self):
        self.update_mrl_options(self.net_mrl_lineedit.text(), '')
