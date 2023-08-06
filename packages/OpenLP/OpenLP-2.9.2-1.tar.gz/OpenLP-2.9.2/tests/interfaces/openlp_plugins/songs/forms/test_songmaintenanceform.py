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
Package to test the openlp.plugins.songs.forms.songmaintenanceform package.
"""
import pytest
from unittest.mock import MagicMock, call, patch, ANY

from PyQt5 import QtCore, QtWidgets

from openlp.core.common.i18n import UiStrings
from openlp.core.common.registry import Registry
from openlp.plugins.songs.forms.songmaintenanceform import SongMaintenanceForm


@pytest.yield_fixture()
def form_env(settings):
    main_window = QtWidgets.QMainWindow()
    Registry().register('main_window', main_window)
    mocked_manager = MagicMock()
    frm = SongMaintenanceForm(mocked_manager)
    yield frm, mocked_manager
    del frm
    del main_window


def test_constructor(form_env):
    """
    Test that a SongMaintenanceForm is created successfully
    """
    # GIVEN: A SongMaintenanceForm
    form = form_env[0]
    mocked_manager = form_env[1]
    # WHEN: The form is created
    # THEN: It should have some of the right components
    assert form is not None
    assert form.manager is mocked_manager


@patch.object(QtWidgets.QDialog, 'exec')
def test_exect(mocked_exec, form_env):
    """
    Test the song maintenance form being executed
    """
    # GIVEN: A song maintenance form
    form = form_env[0]
    mocked_exec.return_value = True

    # WHEN: The song mainetnance form is executed
    with patch.object(form, 'type_list_widget') as mocked_type_list_widget, \
            patch.object(form, 'reset_authors') as mocked_reset_authors, \
            patch.object(form, 'reset_topics') as mocked_reset_topics, \
            patch.object(form, 'reset_song_books') as mocked_reset_song_books:
        result = form.exec(from_song_edit=True)

    # THEN: The correct methods should have been called
    assert form.from_song_edit is True
    mocked_type_list_widget.setCurrentRow.assert_called_once_with(0)
    mocked_reset_authors.assert_called_once_with()
    mocked_reset_topics.assert_called_once_with()
    mocked_reset_song_books.assert_called_once_with()
    mocked_type_list_widget.setFocus.assert_called_once_with()
    mocked_exec.assert_called_once_with(form)
    assert result is True


def test_get_current_item_id_no_item(form_env):
    """
    Test _get_current_item_id() when there's no item
    """
    # GIVEN: A song maintenance form without a selected item
    form = form_env[0]
    mocked_list_widget = MagicMock()
    mocked_list_widget.currentItem.return_value = None

    # WHEN: _get_current_item_id() is called
    result = form._get_current_item_id(mocked_list_widget)

    # THEN: The result should be -1
    mocked_list_widget.currentItem.assert_called_once_with()
    assert result == -1


def test_get_current_item_id(form_env):
    """
    Test _get_current_item_id() when there's a valid item
    """
    # GIVEN: A song maintenance form with a selected item
    form = form_env[0]
    mocked_item = MagicMock()
    mocked_item.data.return_value = 7
    mocked_list_widget = MagicMock()
    mocked_list_widget.currentItem.return_value = mocked_item

    # WHEN: _get_current_item_id() is called
    result = form._get_current_item_id(mocked_list_widget)

    # THEN: The result should be -1
    mocked_list_widget.currentItem.assert_called_once_with()
    mocked_item.data.assert_called_once_with(QtCore.Qt.UserRole)
    assert result == 7


@patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
def test_delete_item_no_item_id(mocked_critical_error_message_box, form_env):
    """
    Test the _delete_item() method when there is no item selected
    """
    # GIVEN: Some mocked items
    form = form_env[0]
    mocked_item_class = MagicMock()
    mocked_list_widget = MagicMock()
    mocked_reset_func = MagicMock()
    dialog_title = 'Delete Item'
    delete_text = 'Are you sure you want to delete this item?'
    error_text = 'There was a problem deleting this item'

    # WHEN: _delete_item() is called
    with patch.object(form, '_get_current_item_id') as mocked_get_current_item_id:
        mocked_get_current_item_id.return_value = -1
        form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                          error_text)

    # THEN: The right things should have been called
    mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
    mocked_critical_error_message_box.assert_called_once_with(dialog_title, UiStrings().NISs)


@patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
def test_delete_item_invalid_item(mocked_critical_error_message_box, form_env):
    """
    Test the _delete_item() method when the item doesn't exist in the database
    """
    # GIVEN: Some mocked items
    form = form_env[0]
    mocked_manager = form_env[1]
    mocked_manager.get_object.return_value = None
    mocked_item_class = MagicMock()
    mocked_list_widget = MagicMock()
    mocked_reset_func = MagicMock()
    dialog_title = 'Delete Item'
    delete_text = 'Are you sure you want to delete this item?'
    error_text = 'There was a problem deleting this item'

    # WHEN: _delete_item() is called
    with patch.object(form, '_get_current_item_id') as mocked_get_current_item_id:
        mocked_get_current_item_id.return_value = 1
        form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                          error_text)

    # THEN: The right things should have been called
    mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
    mocked_manager.get_object.assert_called_once_with(mocked_item_class, 1)
    mocked_critical_error_message_box.assert_called_once_with(dialog_title, error_text)


@patch('openlp.plugins.songs.forms.songmaintenanceform.critical_error_message_box')
def test_delete_item(mocked_critical_error_message_box, form_env):
    """
    Test the _delete_item() method
    """
    # GIVEN: Some mocked items
    form = form_env[0]
    mocked_manager = form_env[1]
    mocked_item = MagicMock()
    mocked_item.songs = []
    mocked_item.id = 1
    mocked_manager.get_object.return_value = mocked_item
    mocked_critical_error_message_box.return_value = QtWidgets.QMessageBox.Yes
    mocked_item_class = MagicMock()
    mocked_list_widget = MagicMock()
    mocked_reset_func = MagicMock()
    dialog_title = 'Delete Item'
    delete_text = 'Are you sure you want to delete this item?'
    error_text = 'There was a problem deleting this item'

    # WHEN: _delete_item() is called
    with patch.object(form, '_get_current_item_id') as mocked_get_current_item_id:
        mocked_get_current_item_id.return_value = 1
        form._delete_item(mocked_item_class, mocked_list_widget, mocked_reset_func, dialog_title, delete_text,
                          error_text)

    # THEN: The right things should have been called
    mocked_get_current_item_id.assert_called_once_with(mocked_list_widget)
    mocked_manager.get_object.assert_called_once_with(mocked_item_class, 1)
    mocked_critical_error_message_box.assert_called_once_with(dialog_title, delete_text, form, True)
    mocked_manager.delete_object(mocked_item_class, 1)
    mocked_reset_func.assert_called_once_with()


@patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
@patch('openlp.plugins.songs.forms.songmaintenanceform.Author')
def test_reset_authors(MockedAuthor, MockedQListWidgetItem, form_env):
    """
    Test the reset_authors() method
    """
    # GIVEN: A mocked authors_list_widget and a few other mocks
    form = form_env[0]
    mocked_manager = form_env[1]
    mocked_author1 = MagicMock()
    mocked_author1.display_name = 'John Newton'
    mocked_author1.id = 1
    mocked_author2 = MagicMock()
    mocked_author2.display_name = ''
    mocked_author2.first_name = 'John'
    mocked_author2.last_name = 'Wesley'
    mocked_author2.id = 2
    mocked_authors = [mocked_author1, mocked_author2]
    mocked_author_item1 = MagicMock()
    mocked_author_item2 = MagicMock()
    MockedQListWidgetItem.side_effect = [mocked_author_item1, mocked_author_item2]
    MockedAuthor.display_name = None
    mocked_manager.get_all_objects.return_value = mocked_authors

    # WHEN: reset_authors() is called
    with patch.object(form, 'authors_list_widget') as mocked_authors_list_widget:
        form.reset_authors()

    # THEN: The authors list should be reset
    expected_widget_item_calls = [call('John Wesley'), call('John Newton')]
    mocked_authors_list_widget.clear.assert_called_once_with()
    mocked_manager.get_all_objects.assert_called_once_with(MockedAuthor)
    # Do not care which order items are called since the order is different on macos vs others
    MockedQListWidgetItem.assert_has_calls(expected_widget_item_calls, any_order=True)
    mocked_author_item1.setData.assert_called_once_with(QtCore.Qt.UserRole, ANY)
    mocked_author_item2.setData.assert_called_once_with(QtCore.Qt.UserRole, ANY)
    mocked_authors_list_widget.addItem.assert_has_calls([
        call(mocked_author_item1), call(mocked_author_item2)])


@patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
@patch('openlp.plugins.songs.forms.songmaintenanceform.Topic')
def test_reset_topics(MockedTopic, MockedQListWidgetItem, form_env):
    """
    Test the reset_topics() method
    """
    # GIVEN: Some mocked out objects and methods
    form = form_env[0]
    mocked_manager = form_env[1]
    MockedTopic.name = 'Grace'
    mocked_topic = MagicMock()
    mocked_topic.id = 1
    mocked_topic.name = 'Grace'
    mocked_manager.get_all_objects.return_value = [mocked_topic]
    mocked_topic_item = MagicMock()
    MockedQListWidgetItem.return_value = mocked_topic_item

    # WHEN: reset_topics() is called
    with patch.object(form, 'topics_list_widget') as mocked_topic_list_widget:
        form.reset_topics()

    # THEN: The topics list should be reset correctly
    mocked_topic_list_widget.clear.assert_called_once_with()
    mocked_manager.get_all_objects.assert_called_once_with(MockedTopic)
    MockedQListWidgetItem.assert_called_once_with('Grace')
    mocked_topic_item.setData.assert_called_once_with(QtCore.Qt.UserRole, 1)
    mocked_topic_list_widget.addItem.assert_called_once_with(mocked_topic_item)


@patch('openlp.plugins.songs.forms.songmaintenanceform.QtWidgets.QListWidgetItem')
@patch('openlp.plugins.songs.forms.songmaintenanceform.Book')
def test_reset_song_books(MockedBook, MockedQListWidgetItem, form_env):
    """
    Test the reset_song_books() method
    """
    # GIVEN: Some mocked out objects and methods
    form = form_env[0]
    mocked_manager = form_env[1]
    MockedBook.name = 'Hymnal'
    mocked_song_book = MagicMock()
    mocked_song_book.id = 1
    mocked_song_book.name = 'Hymnal'
    mocked_song_book.publisher = 'Hymns and Psalms, Inc.'
    mocked_manager.get_all_objects.return_value = [mocked_song_book]
    mocked_song_book_item = MagicMock()
    MockedQListWidgetItem.return_value = mocked_song_book_item

    # WHEN: reset_song_books() is called
    with patch.object(form, 'song_books_list_widget') as mocked_song_book_list_widget:
        form.reset_song_books()

    # THEN: The song_books list should be reset correctly
    mocked_song_book_list_widget.clear.assert_called_once_with()
    mocked_manager.get_all_objects.assert_called_once_with(MockedBook)
    MockedQListWidgetItem.assert_called_once_with('Hymnal (Hymns and Psalms, Inc.)')
    mocked_song_book_item.setData.assert_called_once_with(QtCore.Qt.UserRole, 1)
    mocked_song_book_list_widget.addItem.assert_called_once_with(mocked_song_book_item)


@patch('openlp.plugins.songs.forms.songmaintenanceform.and_')
@patch('openlp.plugins.songs.forms.songmaintenanceform.Author')
def test_check_author_exists(MockedAuthor, mocked_and, form_env):
    """
    Test the check_author_exists() method
    """
    # GIVEN: A bunch of mocked out stuff
    form = form_env[0]
    mocked_manager = form_env[1]
    MockedAuthor.first_name = 'John'
    MockedAuthor.last_name = 'Newton'
    MockedAuthor.display_name = 'John Newton'
    mocked_new_author = MagicMock()
    mocked_new_author.first_name = 'John'
    mocked_new_author.last_name = 'Newton'
    mocked_new_author.display_name = 'John Newton'
    mocked_and.return_value = True
    mocked_authors = [MagicMock(), MagicMock()]
    mocked_manager.get_all_objects.return_value = mocked_authors

    # WHEN: check_author_exists() is called
    with patch.object(form, '_check_object_exists') as mocked_check_object_exists:
        mocked_check_object_exists.return_value = True
        result = form.check_author_exists(mocked_new_author, edit=True)

    # THEN: The correct result is returned
    mocked_and.assert_called_once_with(True, True, True)
    mocked_manager.get_all_objects.assert_called_once_with(MockedAuthor, True)
    mocked_check_object_exists.assert_called_once_with(mocked_authors, mocked_new_author, True)
    assert result is True


@patch('openlp.plugins.songs.forms.songmaintenanceform.Topic')
def test_check_topic_exists(MockedTopic, form_env):
    """
    Test the check_topic_exists() method
    """
    # GIVEN: Some mocked stuff
    form = form_env[0]
    mocked_manager = form_env[1]
    MockedTopic.name = 'Grace'
    mocked_new_topic = MagicMock()
    mocked_new_topic.name = 'Grace'
    mocked_topics = [MagicMock(), MagicMock()]
    mocked_manager.get_all_objects.return_value = mocked_topics

    # WHEN: check_topic_exists() is run
    with patch.object(form, '_check_object_exists') as mocked_check_object_exists:
        mocked_check_object_exists.return_value = True
        result = form.check_topic_exists(mocked_new_topic, True)

    # THEN: The correct things should have been called
    mocked_manager.get_all_objects.assert_called_once_with(MockedTopic, True)
    mocked_check_object_exists.assert_called_once_with(mocked_topics, mocked_new_topic, True)
    assert result is True


@patch('openlp.plugins.songs.forms.songmaintenanceform.and_')
@patch('openlp.plugins.songs.forms.songmaintenanceform.Book')
def test_check_song_book_exists(MockedBook, mocked_and, form_env):
    """
    Test the check_song_book_exists() method
    """
    # GIVEN: Some mocked stuff
    form = form_env[0]
    mocked_manager = form_env[1]
    MockedBook.name = 'Hymns'
    MockedBook.publisher = 'Christian Songs'
    mocked_new_book = MagicMock()
    mocked_new_book.name = 'Hymns'
    mocked_new_book.publisher = 'Christian Songs'
    mocked_and.return_value = True
    mocked_books = [MagicMock(), MagicMock()]
    mocked_manager.get_all_objects.return_value = mocked_books

    # WHEN: check_book_exists() is run
    with patch.object(form, '_check_object_exists') as mocked_check_object_exists:
        mocked_check_object_exists.return_value = True
        result = form.check_song_book_exists(mocked_new_book, True)

    # THEN: The correct things should have been called
    mocked_and.assert_called_once_with(True, True)
    mocked_manager.get_all_objects.assert_called_once_with(MockedBook, True)
    mocked_check_object_exists.assert_called_once_with(mocked_books, mocked_new_book, True)
    assert result is True


def test_check_object_exists_no_existing_objects(form_env):
    """
    Test the _check_object_exists() method when there are no existing objects
    """
    # GIVEN: A SongMaintenanceForm instance
    # WHEN: _check_object_exists() is called without existing objects
    form = form_env[0]
    result = form._check_object_exists([], None, False)

    # THEN: The result should be True
    assert result is True


def test_check_object_exists_without_edit(form_env):
    """
    Test the _check_object_exists() method when edit is false
    """
    # GIVEN: A SongMaintenanceForm instance
    # WHEN: _check_object_exists() is called with edit set to false
    form = form_env[0]
    result = form._check_object_exists([MagicMock()], None, False)

    # THEN: The result should be False
    assert result is False


def test_check_object_exists_not_found(form_env):
    """
    Test the _check_object_exists() method when the object is not found
    """
    # GIVEN: A SongMaintenanceForm instance and some mocked objects
    form = form_env[0]
    mocked_existing_objects = [MagicMock(id=1)]
    mocked_new_object = MagicMock(id=2)

    # WHEN: _check_object_exists() is called with edit set to false
    result = form._check_object_exists(mocked_existing_objects, mocked_new_object, True)

    # THEN: The result should be False
    assert result is False


def test_check_object_exists(form_env):
    """
    Test the _check_object_exists() method
    """
    # GIVEN: A SongMaintenanceForm instance and some mocked objects
    form = form_env[0]
    mocked_existing_objects = [MagicMock(id=1)]
    mocked_new_object = MagicMock(id=1)

    # WHEN: _check_object_exists() is called with edit set to false
    result = form._check_object_exists(mocked_existing_objects, mocked_new_object, True)

    # THEN: The result should be False
    assert result is True
