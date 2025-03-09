from textnode import *

def main():
    newTextNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(newTextNode.__repr__())
main()

