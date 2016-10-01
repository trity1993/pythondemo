from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

# 实战 
pages = set()
images = set()

def getLinks(articleUrl):
    global pages
    global images
    html = urlopen("http://45pan.net/" + articleUrl)
    bsObj = BeautifulSoup(html)
    # getTitle(bsObj)
    getImages(images, bsObj)
    for link in bsObj.findAll("a", href=re.compile(r"^(index_)[0-9]*.html")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # We have encountered a new page
                newPage = link.attrs['href']
                print("url: "+newPage)
                pages.add(newPage)
                getLinks(newPage)


def getImages(images, bsObj):
    for link in bsObj.findAll("img", src=re.compile(r"(http://)*.(gif)")):
        if 'src' in link.attrs:
            if link.attrs['src'] not in images:
                newImg = link.attrs['src']
                print("img: " + newImg)
                pages.add(newImg)

# def getTitle(bsObj):
#     for content in bsObj.findAll("a",{"itemprop":"name"}):
#         print("content:"+content.get_text().encode("utf-8"))


getLinks("")

# 实战

# html = urlopen("http://45pan.net/")
# bsObj = BeautifulSoup(html)
# for link in bsObj.findAll("img"):
#     if 'src' in link.attrs:
#         print(link.attrs['src'])
#
# images = bsObj.findAll("img", {"src": re.compile(r"(http://)*.(gif)")})
# for img in images:
#     print(img["src"])