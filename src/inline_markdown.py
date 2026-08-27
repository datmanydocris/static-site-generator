import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        # even number of pieces means an odd number of delimiters → unmatched
        if len(sections) % 2 == 0:
            raise ValueError(f"invalid markdown: unclosed delimiter {delimiter}")

        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)