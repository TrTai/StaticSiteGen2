import unittest
from main import *

class TestFormatFuncs(unittest.TestCase):

    def test_extractTitle(self):
        md = """
            Here is some text 
            and buried within
        there lies a 
        # Header
        and the function
        should find it
        """
        self.assertEqual(extract_title(md), "Header")

    def test_noHead(self):
        md = """
            Here is some text 
            and buried within
        there lies a 
        Header
        and the function
        should never find
        """
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extractTitlefromStart(self):
        md = """
            # Header
            Here is some text 
            and lying at the start
        there lies a 
        and the function
        should find it
        """
        self.assertEqual(extract_title(md), "Header")

