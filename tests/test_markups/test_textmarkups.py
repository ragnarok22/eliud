import unittest

from eliud.markups import TextMarkup


class TestMarkup(unittest.TestCase):
    def test_textMarkup_with_simple_text(self):
        markup = TextMarkup(text="Hello there")
        self.assertEqual(markup.text, "Hello there")

    def test_textMarkup_with_kwargs(self):
        markup = TextMarkup(text="Hello {name}", name="John")
        self.assertEqual(markup.text, "Hello John")

    def test_textMarkup_with_wrong_kwargs(self):
        with self.assertRaises(KeyError) as error:
            TextMarkup(text="Hello {name}", first_name="John")
        self.assertEqual(str(error.exception), "'Wrong attributes for the given text'")

    def test_textMarkup_str(self):
        markup = TextMarkup(text="Hello world!")
        self.assertEqual(str(markup), markup.text)
        self.assertEqual(str(markup), "Hello world!")

    def test_textMarkup_repr(self):
        markup = TextMarkup(text="Hello world!")
        self.assertEqual(repr(markup), "Markup(text=Hello world!)")
