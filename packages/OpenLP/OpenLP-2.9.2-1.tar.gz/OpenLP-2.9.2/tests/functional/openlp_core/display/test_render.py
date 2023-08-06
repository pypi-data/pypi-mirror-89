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
Test the :mod:`~openlp.core.display.render` package.
"""
from unittest.mock import patch

from openlp.core.display.render import compare_chord_lyric_width, find_formatting_tags, remove_tags, render_chords, \
    render_chords_for_printing, render_tags
from openlp.core.lib.formattingtags import FormattingTags


@patch('openlp.core.display.render.FormattingTags.get_html_tags')
def test_remove_tags(mocked_get_tags):
    """
    Test remove_tags() method.
    """
    # GIVEN: Mocked get_html_tags() method.
    mocked_get_tags.return_value = [{
        'desc': 'Black',
        'start tag': '{b}',
        'start html': '<span style="-webkit-text-fill-color:black">',
        'end tag': '{/b}', 'end html': '</span>', 'protected': True,
        'temporary': False
    }]
    string_to_pass = 'ASDF<br>foo{br}bar&nbsp;{b}black{/b}'
    expected_string = 'ASDF\nfoo\nbar black'

    # WHEN: Clean the string.
    result_string = remove_tags(string_to_pass)

    # THEN: The strings should be identical.
    assert result_string == expected_string, 'The strings should be identical'


@patch('openlp.core.display.render.FormattingTags.get_html_tags')
def test_render_tags(mocked_get_tags, settings):
    """
    Test the render_tags() method.
    """
    # GIVEN: Mocked get_html_tags() method.
    settings.setValue('songs/chord notation', 'english')
    mocked_get_tags.return_value = [
        {
            'desc': 'Black',
            'start tag': '{b}',
            'start html': '<span style="-webkit-text-fill-color:black">',
            'end tag': '{/b}', 'end html': '</span>', 'protected': True,
            'temporary': False
        },
        {
            'desc': 'Yellow',
            'start tag': '{y}',
            'start html': '<span style="-webkit-text-fill-color:yellow">',
            'end tag': '{/y}', 'end html': '</span>', 'protected': True,
            'temporary': False
        },
        {
            'desc': 'Green',
            'start tag': '{g}',
            'start html': '<span style="-webkit-text-fill-color:green">',
            'end tag': '{/g}', 'end html': '</span>', 'protected': True,
            'temporary': False
        }
    ]
    string_to_pass = '{b}black{/b}{y}yellow{/y}'
    expected_string = '<span style="-webkit-text-fill-color:black">black</span>' + \
        '<span style="-webkit-text-fill-color:yellow">yellow</span>'

    # WHEN: Replace the tags.
    result_string = render_tags(string_to_pass)

    # THEN: The strings should be identical.
    assert result_string == expected_string, 'The strings should be identical.'


def test_render_chords(settings):
    """
    Test that the rendering of chords works as expected.
    """
    # GIVEN: A lyrics-line with chords
    settings.setValue('songs/chord notation', 'english')
    text_with_chords = 'H[C]alleluya.[F] [G/B]'

    # WHEN: Expanding the chords
    text_with_rendered_chords = render_chords(text_with_chords)

    # THEN: We should get html that looks like below
    expected_html = '<span class="chordline firstchordline">H<span class="chord"><span><strong>C</strong></span>' \
                    '</span>alleluya.<span class="chord"><span><strong>F</strong></span></span><span class="ws">' \
                    '&nbsp;&nbsp;</span> <span class="chord"><span><strong>G/B</strong></span></span></span>'
    assert text_with_rendered_chords == expected_html, 'The rendered chords should look as expected'


def test_render_chords_with_special_chars(settings):
    """
    Test that the rendering of chords works as expected when special chars are involved.
    """
    # GIVEN: A lyrics-line with chords
    settings.setValue('songs/chord notation', 'english')
    text_with_chords = "I[D]'M NOT MOVED BY WHAT I SEE HALLE[F]LUJA[C]H"

    # WHEN: Expanding the chords
    text_with_rendered_chords = render_tags(text_with_chords, can_render_chords=True)

    # THEN: We should get html that looks like below
    expected_html = '<span class="chordline firstchordline">I<span class="chord"><span><strong>D</strong></span>' \
                    '</span>&#x27;M NOT MOVED BY WHAT I SEE HALLE<span class="chord"><span><strong>F</strong>' \
                    '</span></span>LUJA<span class="chord"><span><strong>C</strong></span></span>H</span>'
    assert text_with_rendered_chords == expected_html, 'The rendered chords should look as expected'


def test_compare_chord_lyric_short_chord():
    """
    Test that the chord/lyric comparing works.
    """
    # GIVEN: A chord and some lyric
    chord = 'C'
    lyrics = 'alleluya'

    # WHEN: Comparing the chord and lyrics
    ret = compare_chord_lyric_width(chord, lyrics)

    # THEN: The returned value should 0 because the lyric is longer than the chord
    assert ret == 0, 'The returned value should 0 because the lyric is longer than the chord'


def test_compare_chord_lyric_long_chord():
    """
    Test that the chord/lyric comparing works.
    """
    # GIVEN: A chord and some lyric
    chord = 'Gsus'
    lyrics = 'me'

    # WHEN: Comparing the chord and lyrics
    ret = compare_chord_lyric_width(chord, lyrics)

    # THEN: The returned value should 4 because the chord is longer than the lyric
    assert ret == 4, 'The returned value should 4 because the chord is longer than the lyric'


def test_render_chords_for_printing(settings):
    """
    Test that the rendering of chords for printing works as expected.
    """
    # GIVEN: A lyrics-line with chords
    settings.setValue('songs/chord notation', 'english')
    text_with_chords = '{st}[D]Amazing {r}gr[D7]ace{/r}  how [G]sweet the [D]sound  [F]{/st}'
    FormattingTags.load_tags()

    # WHEN: Expanding the chords
    text_with_rendered_chords = render_chords_for_printing(text_with_chords, '{br}')

    # THEN: We should get html that looks like below
    expected_html = '<table class="line" width="100%" cellpadding="0" cellspacing="0" border="0"><tr><td><table ' \
                    'class="segment" cellpadding="0" cellspacing="0" border="0" align="left"><tr class="chordrow">'\
                    '<td class="chord">&nbsp;</td><td class="chord">D</td></tr><tr><td class="lyrics">{st}{/st}' \
                    '</td><td class="lyrics">{st}Amazing&nbsp;{/st}</td></tr></table><table class="segment" ' \
                    'cellpadding="0" cellspacing="0" border="0" align="left"><tr class="chordrow">' \
                    '<td class="chord">&nbsp;</td><td class="chord">D7</td></tr><tr><td class="lyrics">{st}{r}gr' \
                    '{/r}{/st}</td><td class="lyrics">{r}{st}ace{/r}&nbsp;{/st}</td></tr></table><table ' \
                    'class="segment" cellpadding="0" cellspacing="0" border="0" align="left"><tr class="chordrow">'\
                    '<td class="chord">&nbsp;</td></tr><tr><td class="lyrics">{st}&nbsp;{/st}</td></tr></table>' \
                    '<table class="segment" cellpadding="0" cellspacing="0" border="0" align="left"><tr ' \
                    'class="chordrow"><td class="chord">&nbsp;</td></tr><tr><td class="lyrics">{st}how&nbsp;{/st}' \
                    '</td></tr></table><table class="segment" cellpadding="0" cellspacing="0" border="0" ' \
                    'align="left"><tr class="chordrow"><td class="chord">G</td></tr><tr><td class="lyrics">{st}' \
                    'sweet&nbsp;{/st}</td></tr></table><table class="segment" cellpadding="0" cellspacing="0" ' \
                    'border="0" align="left"><tr class="chordrow"><td class="chord">&nbsp;</td></tr><tr><td ' \
                    'class="lyrics">{st}the&nbsp;{/st}</td></tr></table><table class="segment" cellpadding="0" ' \
                    'cellspacing="0" border="0" align="left"><tr class="chordrow"><td class="chord">D</td></tr>' \
                    '<tr><td class="lyrics">{st}sound&nbsp;{/st}</td></tr></table><table class="segment" ' \
                    'cellpadding="0" cellspacing="0" border="0" align="left"><tr class="chordrow"><td ' \
                    'class="chord">&nbsp;</td></tr><tr><td class="lyrics">{st}&nbsp;{/st}</td></tr></table>' \
                    '<table class="segment" cellpadding="0" cellspacing="0" border="0" align="left"><tr ' \
                    'class="chordrow"><td class="chord">F</td></tr><tr><td class="lyrics">{st}{/st}&nbsp;</td>' \
                    '</tr></table></td></tr></table>'
    assert text_with_rendered_chords == expected_html, 'The rendered chords should look as expected!'


def test_find_formatting_tags(settings):
    """
    Test that find_formatting_tags works as expected
    """
    # GIVEN: Lyrics with formatting tags and a empty list of formatting tags
    lyrics = '{st}Amazing {r}grace{/r} how sweet the sound'
    tags = []
    FormattingTags.load_tags()

    # WHEN: Detecting active formatting tags
    active_tags = find_formatting_tags(lyrics, tags)

    # THEN: The list of active tags should contain only 'st'
    assert active_tags == ['st'], 'The list of active tags should contain only "st"'
