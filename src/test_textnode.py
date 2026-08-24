import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a google link", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a google link", TextType.LINK, "https://www.google.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        # Both have url=None (the default)
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_url_none_vs_value(self):
        node = TextNode("This is a link", TextType.LINK)          # url = None
        node2 = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()