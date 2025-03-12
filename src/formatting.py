from htmlnode import *
from textnode import TextNode, TextType
import re

#accumulates list of format textNodes and returns list of textNodes with new format
def split_nodes_delimiter(old_nodes, delimiter, textType):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(create_node_type(node, delimiter, textType))
    #print("new nodes: " + str(new_nodes))
    return new_nodes

#limitations: only works for one format type at a time, requires odd output from split
def create_node_type(node, delimiter, textType):
    node_list = []
    #print("incoming node" + str(node))
    if node.textType != TextType.TEXT:
       return [node]
    if node.text.count(delimiter) % 2 != 0:
        raise Exception("No closing delimiter in provided text, invalid MD")
    split_text = node.text.split(delimiter)
    for i, text in enumerate(split_text):
        if i % 2 == 1:
            new_node = TextNode(text, textType)
        else:
            new_node = TextNode(text, TextType.TEXT)
        node_list.append(new_node)
    return node_list

def extract_markdown_images(text):
    imageResults = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return imageResults

def extract_markdown_links(text):
    linkResults = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return linkResults

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes.append(node)
            continue
        imagesResult = extract_markdown_images(node.text)
        if len(imagesResult) == 0:
            new_nodes.append(node)
            continue
        nodeText = node.text
        for i, result in enumerate(imagesResult):
            splitText = nodeText.split(f"![{result[0]}]({result[1]})", 1)
            if splitText[0] != "":
                new_nodes.append(TextNode(splitText[0], TextType.TEXT)) 
            new_nodes.append(TextNode(result[0], TextType.IMAGE, result[1]))
            nodeText = splitText[1]
            #print(nodeText)
            if i == len(imagesResult) - 1 and nodeText != "":
                new_nodes.append(TextNode(nodeText, TextType.TEXT))
                #print(new_nodes)
    return new_nodes
 

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.textType != TextType.TEXT:
            new_nodes.append(node)
            continue
        linkResults = extract_markdown_links(node.text)
        if len(linkResults) == 0:
            new_nodes.append(node)
            continue
        nodeText = node.text
        for i, result in enumerate(linkResults):
            splitText = nodeText.split(f"[{result[0]}]({result[1]})", 1)
            if splitText[0] != "":
                new_nodes.append(TextNode(splitText[0], TextType.TEXT))
            new_nodes.append(TextNode(result[0], TextType.LINK, result[1]))
            nodeText = splitText[1]
            if i == len(linkResults) -1 and nodeText != "":
                new_nodes.append(TextNode(nodeText, TextType.TEXT))
    #for node in new_nodes:

    return new_nodes


def text_to_textnodes(text):
    delimiterDict = { "**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE }
    initialNode = TextNode(text, TextType.TEXT)
    processingNode = [initialNode]
    for key, value in delimiterDict.items():
        processingNode = split_nodes_delimiter(processingNode, key, value)
    processingNode = split_nodes_image(processingNode)
    #print(processingNode)
    processingNode = split_nodes_links(processingNode)
    #print(processingNode)
    return processingNode
