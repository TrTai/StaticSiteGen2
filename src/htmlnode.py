class HtmlNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props != None:
            propString = ""
            for prop in self.props:
                propString += f' {prop}=\"{self.props[prop]}\"'
            return propString
        raise TypeError

    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"

class LeafNode(HtmlNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return str(self.value)
        if self.tag == "a":
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HtmlNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent must have Tag")
        if self.children == None:
            raise ValueError("Parent must have Children")
        return f"<{self.tag}>{''.join(list(map(lambda x: x.to_html(), self.children)))}</{self.tag}>"

