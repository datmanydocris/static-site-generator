from enum import Enum
from htmlnode import ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        if block != "":
            filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith("#"):
        hashes = 0
        for char in block:
            if char == "#":
                hashes += 1
            else:
                break
        if 1 <= hashes <= 6 and len(block) > hashes and block[hashes] == " ":
            return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    for i, line in enumerate(lines):
        expected = f"{i + 1}. "
        if not line.startswith(expected):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_html_node(block))
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    raise ValueError("invalid block type")


def paragraph_to_html_node(block):
    paragraph = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(paragraph))


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[3:-3]
    if text.startswith("\n"):
        text = text[1:]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block):
    lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        lines.append(line.lstrip(">").strip())
    content = " ".join(lines)
    return ParentNode("blockquote", text_to_children(content))


def unordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[2:]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = []
    for line in block.split("\n"):
        text = line[line.index(". ") + 2 :]
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)