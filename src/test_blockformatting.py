import unittest
from blockformatting import *

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

    def test_md_to_html_node(self):
        md = "``` some code here with some _formatting_ that should **not** be changedd ```"
        htmlNode = markdown_to_html_node(md)

if __name__ == "__main__":
    unittest.main()
