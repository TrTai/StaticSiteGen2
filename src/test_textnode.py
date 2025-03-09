import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq_Bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr_Bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        nodeString = f"TextNode(This is a text node, bold, None)"
        self.assertEqual(node.__repr__(), nodeString)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com/images")
        node2 = TextNode("This is a text node", TextType.IMAGE, "https://www.google.com/otherimages")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode("This is a Image node", TextType.IMAGE, "https://www.google.com/images")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["src"], "https://www.google.com/images")
        self.assertEqual(html_node.props["alt"], "This is a Image node")

if __name__ == "__main__":
    unittest.main()
