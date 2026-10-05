""" site_helpers.py: module with functions to help with creating aspects of the html static site inside the interactive website
"""


# constants/config
TOC_FILE = "doclist.yaml"


# imports
from yaml import load, Loader # yaml files are small, use python loaders
from os import path
import marimo as mo

# helpers
def load_toc(toc_file:str = TOC_FILE)->dict: 
    """read in a YAML file to convert into a list of links.  The "links" do NOT have file extensionson them
    in an attempt to work both in the exported HTML and native marimo editors"""
    if not path.exists(toc_file):
        Warning(f"can't find toc file {toc_file}, return empty  toc, carry on...")
        toc ={}
    with open(toc_file, 'r') as file: 
        toc = load(file, Loader=Loader)

    return toc

def toc_md(nav_links:dict, filetype = "html")->str:
    """convert dictionary of links into simple markdown bulleted list"""
    md_list = """\n"""
    for key, value in nav_links.items():
        md_list = md_list + f"""  - [{key}]({value}.{filetype})\n"""
    md_list = md_list
    return md_list


def toc_html(nav_links,filetype = "html"):
    # Generate the HTML links
    links_html = "<ul style='list-style-type: none; padding-left: 0;'>"
    for key, value in nav_links.items():
        links_html += f'<li style="margin-bottom: 8px;"><a href="{value}.{filetype}" style="text-decoration: none; color: #007bff;">{key}</a></li>'
    links_html += "</ul>"
    return(links_html)

def nav_sidebar(links_html):
    # Wrap everything in a collapsible section and place it in the sidebar
    return mo.sidebar(
        mo.md(f"""
        ## TOC
        <details open>
            <summary style="cursor: pointer; font-weight: bold; margin-bottom: 10px;">
                Navigation
            </summary>
            {links_html}
        </details>
        """)
    )

def add_nav():
    toc_links = load_toc()
    toc_html = (toc_links)
    return(nav_sidebar(toc_html))
