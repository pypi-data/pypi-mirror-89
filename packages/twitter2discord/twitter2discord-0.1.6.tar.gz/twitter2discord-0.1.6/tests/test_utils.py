import unittest

from googletrans import Translator
from twitter2discord.utils import *


class Twitter2DiscordUtilsTests(unittest.TestCase):

    def test_fix_max_length(self):
        result = fix_max_length('')
        self.assertEqual(len(result), 1)
        result = fix_max_length('abcd', 2)
        self.assertEqual(len(result), 2)

    def test_ggtrans(self):
        translator = Translator()
        text = 'こんにちは'
        translation = translator.translate(text)
        self.assertEqual(translation.text, 'Hello')
