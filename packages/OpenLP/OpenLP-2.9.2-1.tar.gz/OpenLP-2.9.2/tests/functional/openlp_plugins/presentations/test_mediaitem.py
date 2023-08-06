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
This module contains tests for the lib submodule of the Presentations plugin.
"""
from pathlib import Path
from unittest.mock import MagicMock, PropertyMock, call, patch

from openlp.core.common.registry import Registry
from openlp.core.lib import ServiceItemContext
from openlp.core.lib.serviceitem import ItemCapabilities
from openlp.plugins.presentations.lib.mediaitem import PresentationMediaItem


def test_build_file_mask_string(media_item):
    """
    Test the build_file_mask_string() method
    """
    # GIVEN: Different controllers.
    impress_controller = MagicMock()
    impress_controller.enabled.return_value = True
    impress_controller.supports = ['odp']
    impress_controller.also_supports = ['ppt']
    presentation_controller = MagicMock()
    presentation_controller.enabled.return_value = True
    presentation_controller.supports = ['ppt']
    presentation_controller.also_supports = []
    presentation_viewer_controller = MagicMock()
    presentation_viewer_controller.enabled.return_value = False
    pdf_controller = MagicMock()
    pdf_controller.enabled.return_value = True
    pdf_controller.supports = ['pdf']
    pdf_controller.also_supports = ['xps', 'oxps', 'epub', 'cbz', 'fb2']
    # Mock the controllers.
    media_item.controllers = {
        'Impress': impress_controller,
        'Powerpoint': presentation_controller,
        'Powerpoint Viewer': presentation_viewer_controller,
        'Pdf': pdf_controller
    }

    # WHEN: Build the file mask.
    with patch('openlp.plugins.presentations.lib.mediaitem.translate') as mocked_translate:
        mocked_translate.side_effect = lambda module, string_to_translate: string_to_translate
        media_item.build_file_mask_string()

    # THEN: The file mask should be generated correctly with a space before all bar the first.
    assert '*.odp' in media_item.on_new_file_masks, 'The file mask should contain the odp extension'
    assert ' *.ppt' in media_item.on_new_file_masks, 'The file mask should contain the ppt extension'
    assert ' *.pdf' in media_item.on_new_file_masks, 'The file mask should contain the pdf extension'
    assert ' *.xps' in media_item.on_new_file_masks, 'The file mask should contain the xps extension'
    assert ' *.oxps' in media_item.on_new_file_masks, 'The file mask should contain the oxps extension'
    assert ' *.epub' in media_item.on_new_file_masks, 'The file mask should contain the epub extension'
    assert ' *.cbz' in media_item.on_new_file_masks, 'The file mask should contain the cbz extension'
    assert ' *.fb2' in media_item.on_new_file_masks, 'The file mask should contain the fb2 extension'


def test_clean_up_thumbnails(media_item):
    """
    Test that the clean_up_thumbnails method works as expected when files exist.
    """
    # GIVEN: A mocked controller, and mocked os.path.getmtime
    mocked_disabled_controller = MagicMock()
    mocked_disabled_controller.enabled.return_value = False
    mocked_disabled_supports = PropertyMock()
    type(mocked_disabled_controller).supports = mocked_disabled_supports
    mocked_enabled_controller = MagicMock()
    mocked_enabled_controller.enabled.return_value = True
    mocked_doc = MagicMock(**{'get_thumbnail_path.return_value': Path()})
    mocked_enabled_controller.add_document.return_value = mocked_doc
    mocked_enabled_controller.supports = ['tmp']
    media_item.controllers = {
        'Enabled': mocked_enabled_controller,
        'Disabled': mocked_disabled_controller
    }

    thumb_path = MagicMock(st_mtime=100)
    file_path = MagicMock(st_mtime=400)
    with patch.object(Path, 'stat', side_effect=[thumb_path, file_path]), \
            patch.object(Path, 'exists', return_value=True):
        presentation_file = Path('file.tmp')

        # WHEN: calling clean_up_thumbnails
        media_item.clean_up_thumbnails(presentation_file, True)

    # THEN: doc.presentation_deleted should have been called since the thumbnails mtime will be greater than
    #       the presentation_file's mtime.
    mocked_doc.assert_has_calls([call.get_thumbnail_path(1, True), call.presentation_deleted()], True)
    assert mocked_disabled_supports.call_count == 0


def test_clean_up_thumbnails_missing_file(media_item):
    """
    Test that the clean_up_thumbnails method works as expected when file is missing.
    """
    # GIVEN: A mocked controller, and mocked os.path.exists
    mocked_controller = MagicMock()
    mocked_doc = MagicMock()
    mocked_controller.add_document.return_value = mocked_doc
    mocked_controller.supports = ['tmp']
    media_item.controllers = {
        'Mocked': mocked_controller
    }
    presentation_file = Path('file.tmp')
    with patch.object(Path, 'exists', return_value=False):

        # WHEN: calling clean_up_thumbnails
        media_item.clean_up_thumbnails(presentation_file, True)

    # THEN: doc.presentation_deleted should have been called since the presentation file did not exist.
    mocked_doc.assert_has_calls([call.get_thumbnail_path(1, True), call.presentation_deleted()], True)


def test_pdf_generate_slide_data(media_item):
    """
    Test that the generate slide data function makes the correct ajustments to a pdf service item.
    """
    # GIVEN: A mocked pdf service item
    media_item.list_view = MagicMock()
    media_item.display_type_combo_box = MagicMock()
    mocked_service_item = MagicMock()

    # WHEN: generate_slide_data is called
    media_item.generate_slide_data(mocked_service_item, context=ServiceItemContext.Live, file_path=Path('test.pdf'))

    # THEN: Should be categorized as images and overrides the theme
    assert mocked_service_item.name == 'images'
    mocked_service_item.add_capability.assert_any_call(ItemCapabilities.ProvidesOwnTheme)


@patch('openlp.plugins.presentations.lib.mediaitem.MediaManagerItem._setup')
@patch('openlp.plugins.presentations.lib.mediaitem.PresentationMediaItem.setup_item')
def test_search(mock_setup, mock_item, registry):
    """
    Test that the search method finds the correct results
    """
    # GIVEN: A mocked Settings class which returns a list of Path objects,
    #        and an instance of the PresentationMediaItem
    path_1 = Path('some_dir', 'Impress_file_1')
    path_2 = Path('some_other_dir', 'impress_file_2')
    path_3 = Path('another_dir', 'ppt_file')
    mocked_returned_settings = MagicMock()
    mocked_returned_settings.value.return_value = [path_1, path_2, path_3]
    Registry().register('settings', mocked_returned_settings)
    media_item = PresentationMediaItem(None, MagicMock(), None)

    # WHEN: Calling search
    results = media_item.search('IMPRE', False)

    # THEN: The first two results should have been returned
    assert results == [[str(path_1), 'Impress_file_1'], [str(path_2), 'impress_file_2']]
