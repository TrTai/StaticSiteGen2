from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from formatting import text_to_textnodes
from textnode import TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORD_LIST = "unordered_list"
    ORD_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n\n"):
        newstring = ""
        for i, subline in enumerate(line.split("\n")):
            if i % 2 != 0:
                newstring += "\n"
            newstring += subline.strip()
        blocks.append(newstring.strip())
    return blocks

def block_to_block_type(block):
    if re.match(r"#{1,6} \w", block) != None:
        return BlockType.HEADING
    elif re.match(r"```[\s\S]+```$", block, re.MULTILINE) != None:
        return BlockType.CODE
    elif re.match(r"> \w", block) != None:
        return BlockType.QUOTE
    elif re.match(r"- \S", block) != None:
        return BlockType.UNORD_LIST
    elif re.match(r"\d+\. \S", block) != None:
        return BlockType.ORD_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    htmlNodes = []
    for block in blocks:
        blockType = block_to_block_type(block)
        match (blockType):
            case (BlockType.PARAGRAPH):
                newTextNodes = text_to_textnodes(block)
                newHtmlLeafs = textNodes_to_htmlLeafNodes(newTextNodes)
                newHtmlParent = ParentNode("p", newHtmlLeafs)
                htmlNodes.append(newHtmlParent)
                #print(newHtmlParent.to_html())
            case (BlockType.HEADING):
                headingLevel = re.match(r"#{1,6}", block).span()[1]
                newTextNodes = text_to_textnodes(block.lstrip("#").strip())
                newHtmlLeafs = textNodes_to_htmlLeafNodes(newTextNodes)
                #print(newTextNodes)
                #print(newHtmlLeafs)
                newHtmlParent = ParentNode(f"h{headingLevel}", newHtmlLeafs)
                #print(newHtmlParent.to_html())
                htmlNodes.append(newHtmlParent)
            case (BlockType.CODE):
                codeBlock = block.lstrip("```").rstrip("```").strip()
                newHtmlLeaf = LeafNode("code", codeBlock)
                newParentNode = ParentNode("pre", [newHtmlLeaf])
                print(newParentNode.to_html())
                htmlNodes.append(newHtmlLeaf)
            case (BlockType.QUOTE):
                for line in block.split("\n"):
                    if line[0] == ">":
                        quotedText = line.lstrip(">").strip()
                        

            #case (BlockType.UNORD_LIST):
            #case (BlockType.ORD_LIST):
            case _:
                raise NotImplementedError

def textNodes_to_htmlLeafNodes(textNodes):
    htmlNodes = []
    for node in textNodes:
        newLeaf = text_node_to_html_node(node)
        htmlNodes.append(newLeaf)
    return htmlNodes

