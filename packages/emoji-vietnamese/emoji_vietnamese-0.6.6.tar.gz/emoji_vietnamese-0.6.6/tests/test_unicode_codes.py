# -*- coding: UTF-8 -*-


"""
Unittests for emoji_vietnamese.unicode_codes
"""


import emoji_vietnamese


def test_emoji_names():

    for use_aliases, group in (
            (False, emoji_vietnamese.unicode_codes.EMOJI_UNICODE),
            (True, emoji_vietnamese.unicode_codes.EMOJI_ALIAS_UNICODE)):
        for name, ucode in group.items():
            assert name.startswith(':') and name.endswith(':') and len(name) >= 3
            emj = emoji_vietnamese.emojize(name, use_aliases=use_aliases)
            assert emj == ucode, "%s != %s" % (emoji_vietnamese.emojize(name), ucode)


def test_compare_normal_and_aliases():
    # There should always be more aliases than normal codes since the aliases contain
    # the normal codes
    assert len(emoji_vietnamese.EMOJI_UNICODE) < len(emoji_vietnamese.EMOJI_ALIAS_UNICODE)