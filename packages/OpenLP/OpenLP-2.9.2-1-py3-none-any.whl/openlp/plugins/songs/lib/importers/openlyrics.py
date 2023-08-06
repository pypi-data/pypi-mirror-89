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
The :mod:`openlyrics` module provides the functionality for importing
songs which are saved as OpenLyrics files.
"""
import logging

from lxml import etree

from openlp.core.widgets.wizard import WizardStrings
from openlp.plugins.songs.lib.importers.songimport import SongImport
from openlp.plugins.songs.lib.openlyricsxml import OpenLyrics, OpenLyricsError
from openlp.plugins.songs.lib.ui import SongStrings


log = logging.getLogger(__name__)


class OpenLyricsImport(SongImport):
    """
    This provides the Openlyrics import.
    """
    def __init__(self, manager, **kwargs):
        """
        Initialise the Open Lyrics importer.
        """
        log.debug('initialise OpenLyricsImport')
        super(OpenLyricsImport, self).__init__(manager, **kwargs)
        self.open_lyrics = OpenLyrics(self.manager)

    def do_import(self):
        """
        Imports the songs.
        """
        self.import_wizard.progress_bar.setMaximum(len(self.import_source))
        parser = etree.XMLParser(remove_blank_text=True, remove_pis=True)
        for file_path in self.import_source:
            if self.stop_import_flag:
                return
            self.import_wizard.increment_progress_bar(WizardStrings.ImportingType.format(source=file_path.name))
            try:
                # Pass a file object, because lxml does not cope with some
                # special characters in the path (see lp:757673 and lp:744337).
                parsed_file = etree.parse(file_path.open('rb'), parser)

                # Remove whitespaces from <lines> tags and its descendants
                root = parsed_file.getroot()
                for elem in root.iter('{*}lines'):
                    self._strip_whitespace(elem)
                    for subelem in elem.iter('*'):
                        self._strip_whitespace(subelem)

                xml = etree.tostring(root).decode()
                self.open_lyrics.xml_to_song(xml)
            except etree.XMLSyntaxError:
                log.exception('XML syntax error in file {path}'.format(path=file_path))
                self.log_error(file_path, SongStrings.XMLSyntaxError)
            except OpenLyricsError as exception:
                log.exception('OpenLyricsException {error:d} in file {name}: {text}'.format(error=exception.type,
                                                                                            name=file_path,
                                                                                            text=exception.log_message))
                self.log_error(file_path, exception.display_message)

    def _strip_whitespace(self, elem):
        """
        Remove leading and trailing whitespace from the 'text' and 'tail' attributes of an etree._Element object
        """
        if elem.text is not None:
            elem.text = elem.text.strip()
        if elem.tail is not None:
            elem.tail = elem.tail.strip()
