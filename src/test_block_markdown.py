import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


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