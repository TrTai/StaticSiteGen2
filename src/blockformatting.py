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
    for block in markdown.split("\n\n"):
        newstring = ""
        for line in block.split("\n"):
            newstring += "\n"
            newstring += line.strip()
        blocks.append(newstring.strip())
    blocks[-1] = blocks[-1].rstrip("\n")
    #print(blocks)
    return blocks

def block_to_block_type(block):
    if re.match(r"#{1,6} \w", block) != None:
        return BlockType.HEADING
    elif re.match(r"```[\s\S]+```$", block, re.MULTILINE) != None:
        return BlockType.CODE
    elif re.match(r"> \S", block) != None:
        #print("quote: " + block)
        return BlockType.QUOTE
    elif re.match(r"- \S", block) != None:
        return BlockType.UNORD_LIST
    elif re.match(r"\d+\. \S", block) != None:
        return BlockType.ORD_LIST
    else:
        #print("paragraph: " + block)
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    #print(blocks)
    htmlNodes = []

    for block in blocks:
        if block == "":
            continue
        blockType = block_to_block_type(block)
        #print(blockType)

        match (blockType):

            case (BlockType.PARAGRAPH):
                #print(f"new block: {block}")
                textNodes = []
                #for line in block.split("\n"):
                    #print(f"new line: {line}")
                newTextNodes = text_to_textnodes(block.replace("\n", " "))
                textNodes.extend(newTextNodes)
                #print(f"new text nodes: {textNodes}")
                newHtmlLeafs = textNodes_to_htmlLeafNodes(textNodes)
                #print(f"new leaf nodes: {newHtmlLeafs}")
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
                codeBlock = block.lstrip("```").rstrip("```").strip(" ").lstrip("\n")
                #print(repr(codeBlock))
                newHtmlLeaf = LeafNode("code", codeBlock)
                #print(newHtmlLeaf)
                newParentNode = ParentNode("pre", [newHtmlLeaf])
                #print(newParentNode.to_html())
                htmlNodes.append(newParentNode)

            case (BlockType.QUOTE):
                quotedText = ""
                plainText = ""
                #print(repr(block))
                for line in block.split("\n"):
                    #print(repr(line))
                    if line[0] == ">":
                        quotedText += line.lstrip(">").strip() + "<br>"
                    elif line[0] != ">":
                        plainText += line.strip()
                    if len(plainText) > 0:
                        raise ValueError("Plain text in quote block")
                    else:
                        #print(repr(quotedText))
                        newTextNodes = text_to_textnodes(quotedText)
                        #print(newTextNodes)
                        newHtmlLeafs = textNodes_to_htmlLeafNodes(newTextNodes)
                newHtmlParent = ParentNode("blockquote", newHtmlLeafs)
                #print(newHtmlParent.to_html())
                htmlNodes.append(newHtmlParent)

            case (BlockType.UNORD_LIST):
                itemHtmlNodes = []
                for line in block.split("\n"):
                    if line[0] == "-":
                        itemTextNode = text_to_textnodes(line.lstrip("-").strip())
                        itemHtmlLeafs = textNodes_to_htmlLeafNodes(itemTextNode)
                        itemHtmlNodes.append(ParentNode("li", itemHtmlLeafs))
                ulHtmlParent = ParentNode("ul", itemHtmlNodes)
                htmlNodes.append(ulHtmlParent)

            case (BlockType.ORD_LIST):
                itemHtmlNodes = []
                for line in block.split("\n"):
                    #print(re.match(r"\d+\. ", line).group())
                    newTextNode = text_to_textnodes(line.lstrip(re.match(r"\d+\. ", line).group()))
                    newHtmlLeafs = textNodes_to_htmlLeafNodes(newTextNode)
                    itemHtmlNodes.append(ParentNode("li", newHtmlLeafs))
                olHtmlParent = ParentNode("ol", itemHtmlNodes)
                htmlNodes.append(olHtmlParent)
                #print(olHtmlParent.to_html())
            case _:
                raise NotImplementedError
    return ParentNode("div", htmlNodes)

def textNodes_to_htmlLeafNodes(textNodes):
    htmlNodes = []
    for node in textNodes:
        newLeaf = text_node_to_html_node(node)
        htmlNodes.append(newLeaf)
    return htmlNodes

