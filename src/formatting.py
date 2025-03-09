from textnode import *
from htmlnode import *

def split_nodes_delimiter(old_nodes, delimiter, textType):
    new_nodes = []
    for node in old_nodes:
        new_nodes.extend(create_node_type(node, delimiter, textType))
    return new_nodes

def create_node_type(node, delimiter, textType):
    node_list = []
    if node.textType != TextType.TEXT:
       return node
    if node.text.count(delimiter) % 2 != 0:
        raise Exception("No closing delimiter in provided text, invalid MD")
    split_text = node.text.split(delimiter)
    for text in split_text:
        new_node = TextNode(text, textType)
        node_list.append(new_node)
    return node_list
        

    
    delimiter = "**"
    delimiter = "_"
    delimiter = "`"
