import unittest
from textnode import *
from formatting import *

class TestFormatFuncs(unittest.TestCase):

    def test_SingleCodeBlock(self):
        baseNode = TextNode("This is text with a `code block` word", TextType.TEXT)
        newNodes = split_nodes_delimiter([baseNode], "`", TextType.CODE)
        results = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
        self.assertEqual(newNodes, results)



    def test_Bold(self):
        baseNode = TextNode("This is text with a **BOLD** word", TextType.TEXT)
        newNodes = split_nodes_delimiter([baseNode], "**", TextType.BOLD)
        results = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("BOLD", TextType.BOLD),
    TextNode(" word", TextType.TEXT),
    ]
        self.assertEqual(newNodes, results)


    def test_multiBold(self):
        baseNode = TextNode("This is text with a **BOLD** word then another **BOLDED** word", TextType.TEXT)
        newNodes = split_nodes_delimiter([baseNode], "**", TextType.BOLD)
        results = [
 TextNode("This is text with a ", TextType.TEXT),
 TextNode("BOLD", TextType.BOLD),
 TextNode(" word then another ", TextType.TEXT),
 TextNode("BOLDED", TextType.BOLD),
 TextNode(" word", TextType.TEXT),
]
        self.assertEqual(newNodes, results)


    def test_noClose(self):
        baseNode = TextNode("This is text with a **BOLD word", TextType.TEXT)
        #newNodes = split_nodes_delimiter([baseNode], "**", TextType.BOLD)
        with self.assertRaises(Exception):
            split_nodes_delimiter([baseNode], "**", TextType.BOLD)

    #def test_imageMDExtraction(self):
    #    text = "![alt text](https://www.google.com)"
    #    altText, url = extract_markdown_images(text)
    #    self.assertEqual(altText, ["alt text"])
    #    self.assertEqual(url, ["https://www.google.com"])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)



    def test_extract_2markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/zjjcJKY.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another image", "https://i.imgur.com/zjjcJKY.png")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    
    def test_extract_2markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev) and [another link](https://google.com)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("another link", "https://google.com")], matches)


    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )


    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_toNode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
]
        self.assertEqual(text_to_textnodes(text), result)

    def test_text_toNodeAgain(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) and some more text."
        result = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    TextNode(" and some more text.", TextType.TEXT),
]
        self.assertEqual(text_to_textnodes(text), result)

