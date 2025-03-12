import unittest
from blockformatting import *
import textwrap

class TestFormatFuncs(unittest.TestCase):

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
    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("# This is a heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### This is another heading"), BlockType.HEADING)

    def test_more_block_to_block_type(self):
        self.assertEqual(block_to_block_type("############ This is not a heading"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```python\nprint('hello world')\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- This is a list"), BlockType.UNORD_LIST)

    def test_even_more_block_to_block_type(self):
        self.assertEqual(block_to_block_type("1. This is a list"), BlockType.ORD_LIST)
        self.assertEqual(block_to_block_type("1.3 This is a decimal"), BlockType.PARAGRAPH)

    #def test_paragraphs(self):
    #    md = """
    #This is **bolded** paragraph
    #text in a p
    #tag here

    #This is another paragraph with _italic_ text and `code` here

    #"""

    #    node = markdown_to_html_node(md)
    #    html = node.to_html()
    #    self.assertEqual(
    #        html,
    #        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    #    )

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

if __name__ == "__main__":
    unittest.main()
