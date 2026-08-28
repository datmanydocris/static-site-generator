import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
# Heading


Paragraph after extra space


- list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Paragraph after extra space",
                "- list",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### H6"), BlockType.HEADING)

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hi')\n```"),
            BlockType.CODE,
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> line one\n> line two"),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2"),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_start(self):
        self.assertEqual(
            block_to_block_type("2. first\n3. second"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph."),
            BlockType.PARAGRAPH,
        )

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        node = markdown_to_html_node("# Hello")
        self.assertEqual(node.to_html(), "<div><h1>Hello</h1></div>")

    def test_quote(self):
        md = """
> This is a quote
> with two lines
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a quote with two lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li></ul></div>",
        )

if __name__ == "__main__":
    unittest.main()