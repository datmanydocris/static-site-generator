import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_from_doc(self):
        md = """
# Tolkien Fan Club

Here's a paragraph
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_extract_title_none(self):
        with self.assertRaises(Exception):
            extract_title("## not an h1\njust text")