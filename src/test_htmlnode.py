import unittest
from htmlnode import *

class TestHtmlNode(unittest.TestCase):
    def testNotImplemented(self):
        node = HtmlNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def testPropsString(self):
        testProps = {
    "href": "https://www.google.com",
    "target": "_blank",
}        
        node = HtmlNode(props = testProps)
        expectedString = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expectedString)

    def testRepr(self):
        node = HtmlNode("h1", "Testing Replication")
        expectedString = f"tag = h1, value = Testing Replication, children = None, props = None"
        self.assertEqual(node.__repr__(), expectedString)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        nodeProps = {
            "href" : "https://www.google.com"
        }
        node = LeafNode("a", "Hello, world!", nodeProps)
        self.assertEqual(node.to_html(), '<a href=\"https://www.google.com\">Hello, world!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
