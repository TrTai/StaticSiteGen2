from os.path import isdir
from textnode import *
import os
import shutil
import re
from blockformatting import markdown_to_html_node
def main():
    #newTextNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(newTextNode.__repr__())
    clear_public()
    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

def clear_public():
    print(os.listdir())
    if "public" in os.listdir():
        print("Directory 'public' already exists.")
        absolutePathtoPublic = os.path.join(os.getcwd(), "public")
        print(f"Removing directory {absolutePathtoPublic}")
        shutil.rmtree(absolutePathtoPublic)
        print("Public directory removed.")
    os.mkdir("public")


def copy_static_to_public():
        if os.path.isdir("static"):
            print("Static directory exists, copying to public")
            print(os.listdir("static"))
            copy_from_dir("static")

def copy_from_dir(path):
    if os.path.isdir(path):
        print(f"{path} is a directory")
        if path != "static":
            print(f"Creating subdirectory {path.replace("static", "public")}")
            os.mkdir(path.replace("static", "public"))
        for item in os.listdir(path):
            copy_from_dir(os.path.join(path, item))
    else:
        print(f"{path} is not a directory. Copying file to Public")
        shutil.copy(path, path.replace("static", "public"))

def extract_title(markdown):
    header = re.search(r"# (.*)", markdown).group().lstrip("#").strip()
    if header == None:
        raise Exception("No header found")
    return header
        

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    mdFile = open(from_path, "r")
    md = mdFile.read()
    templateFile = open(template_path, "r")
    template = templateFile.read()
    htmlOut = markdown_to_html_node(md).to_html()
    pageTitle = extract_title(md)
    outputFile = template.replace("{{ Title }}", pageTitle).replace("{{ Content }}", htmlOut)
    print(f"writing out file to {dest_path}")
    destinationFile = open(dest_path, "w")
    destinationFile.write(outputFile)
    mdFile.close()
    templateFile.close()
    destinationFile.close()



main()

