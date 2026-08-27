import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_bold(self):
        node = TextNode(
            "This is text with a **bolded phrase** in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_delimiters(self):
        node = TextNode("This has **two** bold **words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("two", TextType.BOLD),
                TextNode(" bold ", TextType.TEXT),
                TextNode("words", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_non_text_node_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([node], new_nodes)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("plain ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and `code`", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("plain ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ],
            new_nodes,
        )

    def test_starts_with_delimiter(self):
        node = TextNode("**bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_unmatched_delimiter(self):
        node = TextNode("This is **unclosed bold", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [TextNode("Just plain text", TextType.TEXT)],
            new_nodes,
        )

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_markdown_links_ignores_images(self):
        text = "A ![pic](https://img.com/a.png) and a [link](https://boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("link", "https://boot.dev")],
            matches,
        )

    def test_extract_none(self):
        self.assertListEqual(extract_markdown_images("no images here"), [])
        self.assertListEqual(extract_markdown_links("no links here"), [])


if __name__ == "__main__":
    unittest.main()