# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import re

# Code here - Import BeautifulSoup library
import sys

import requests
from bs4 import BeautifulSoup, Tag

# Code ends here

# function to get the html source text of the medium article


def get_page():
    global url

    # Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
    url = input("Enter url of a medium article: ")
    # Code ends here

    # handling possible error
    if not re.match(r"https?://medium.com/", url):
        print("Please enter a valid website, or make sure it is a medium article")
        sys.exit(1)

    # Code here - Call get method in requests object, pass url and collect it in res
    res = requests.get(url)
    # Code ends here

    res.raise_for_status()
    soup = BeautifulSoup(res.content, "html.parser")
    return soup


# function to remove all the html tags and replace some with specific strings


def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items())
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub("\<(.*?)\>", "", text)
    return text


def format_content(content: Tag):
    content.select_one("div.speechify-ignore").decompose()
    article = content.select_one("article")
    elements = article.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p"])
    markdown_content = f"url: {url}\n\n"
    for element in elements:
        if element.name.startswith("h"):
            level = int(element.name[1])  # Get the header level
            markdown_content += f"{'#' * level} {element.get_text()}\n\n"
        elif element.name == "p":
            markdown_content += f"{element.get_text()}\n\n"

    return markdown_content


def collect_text(soup):
    text = f"url: {url}\n\n"
    para_text = soup.find_all("p")
    print(f"paragraphs text = \n {para_text}")
    for para in para_text:
        text += f"{para.text}\n\n"
    return text


# function to save file in the current directory


def save_file(text):
    if not os.path.exists("./scraped_articles"):
        os.mkdir("./scraped_articles")
    name = url.split("/")[-1]
    print(name)
    fname = f"scraped_articles/{name}.txt"

    # Code here - write a file using with (2 lines)
    with open(fname, "w") as f:
        f.write(text)
    # Code ends here

    print(f"File saved in directory {fname}")


if __name__ == "__main__":
    page = get_page()
    formatted = format_content(page)
    save_file(formatted)
    # Instructions to Run this python code
    # Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
