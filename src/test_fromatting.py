import unittest
from formatting import split_nodes_delimiter
from textnode import *
from formatting import *

class TestFormatFuncs(unittest.TestCase):
    def basicTest(self):
        baseNode = TextNode("This is text with a `code block` word", TextType.TEXTS)
        newNodes = split_nodes_delimiter([baseNode], "`", TextType.CODE)
        results = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(newNodes, results)
