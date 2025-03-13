from textnode import *
import os
import shutil
import re
from blockformatting import markdown_to_html_node
from pathlib import Path
from sys import argv

def main():
    global basepath
    basepath = argv
    if basepath == "":
        basepath = "/"
    #newTextNode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    #print(newTextNode.__repr__())
    #clear_public()
    clear_docs()
    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "docs")
    #generate_page("content/index.md", "template.html", "public/index.html")

def clear_public():
    print(os.listdir())
    if "public" in os.listdir():
        print("Directory 'public' already exists.")
        absolutePathtoPublic = os.path.join(os.getcwd(), "public")
        print(f"Removing directory {absolutePathtoPublic}")
        shutil.rmtree(absolutePathtoPublic)
        print("Public directory removed.")
    os.mkdir("public")

def clear_docs():
    print(os.listdir())
    if "docs" in os.listdir():
        print("Directory 'docs' already exists.")
        absolutePathtoPublic = os.path.join(os.getcwd(), "docs")
        print(f"Removing directory {absolutePathtoPublic}")
        shutil.rmtree(absolutePathtoPublic)
        print("docs directory removed.")
    os.mkdir("docs")



def copy_static_to_public():
        if os.path.isdir("static"):
            print("Static directory exists, copying to public")
            print(os.listdir("static"))
            copy_from_dir("static")

def copy_from_dir(path):
    if os.path.isdir(path):
        print(f"{path} is a directory")
        if path != "static":
            print(f"Creating subdirectory {path.replace("static", "docs")}")
            os.mkdir(path.replace("static", "docs"))
        for item in os.listdir(path):
            copy_from_dir(os.path.join(path, item))
    else:
        print(f"{path} is not a directory. Copying file to Public")
        shutil.copy(path, path.replace("static", "docs"))

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
    outputFile = template.replace("{{ Title }}", extract_title(md)).replace("{{ Content }}", markdown_to_html_node(md).to_html()).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
    print(f"writing out file to {dest_path}")
    if os.path.dirname(dest_path) != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    destinationFile = open(dest_path, "w")
    destinationFile.write(outputFile)
    mdFile.close()
    templateFile.close()
    destinationFile.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
            if os.path.isfile(os.path.join(dir_path_content, item)):
                generate_page(os.path.join(dir_path_content, item), template_path,  Path(os.path.join(dest_dir_path, item)).with_suffix(".html"))
            else:
                generate_pages_recursive(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, item))
main()

