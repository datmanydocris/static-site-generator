class HTMLNode:
    def __init__(self, tag = None, value = None, children: list[HTMLNode] | None = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented in parent class")

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""

        props_list = []
        for key, value in self.props.items():
            props_list.append(f'{key}="{value}"')

        return " " + " ".join(props_list)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tage, value, props=None):
        super().__init__(tage, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"