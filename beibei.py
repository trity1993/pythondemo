from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

products = []
counts = []
prices = []
imgUrls = []
productUrls = []

def getLinks(filePath,articleUrl):
    global products
    global counts
    global prices
    global imgUrls
    global productUrls

    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html)
    getTitle(bsObj, imgUrls, products)
    getPrice(bsObj, prices, counts)
    getPriceUrl(bsObj, productUrls)
    writeIO(filePath,products, productUrls, prices, counts, imgUrls)

# 贝贝网商品完成+依靠商品找出对应的销售量


def getTitle(bsObj, imgUrls, products):
    index = 0
    for content in bsObj.findAll("div", {"class": "title"}):
        if index > 11:
            break
        if "title" in content.attrs:
            product = content.attrs["title"]
            img = bsObj.find("img", {"title": product})
            # print("产品首图："+img.attrs['src'])
            # print("产品："+product)

            imgUrls.append(img.attrs['src'])
            products.append(product)

            # 可选项
            # way=content.find("span",{"class":"my-tag"})
            # if way:
            #     print("活动方式"+way.get_text())

            index = index + 1
# 对应的产品销售数量+单价 优化==需要进行去掉空格和换行


def getPrice(bsObj, prices, counts):
    index = 0
    for priceInt in bsObj.findAll("span", {"class": "price-info "}):
        if index > 11:
            break
        # print("销量:"+priceInt.find("span",{"class":"discount"}).get_text().lstrip('\n').strip(' '))
        # print("单价:"+priceInt.find("span",{"class":"price price-int"}).get_text()+priceInt.find("span",{"class":"price price-decimal"}).get_text().lstrip('\n').strip(' '))

        prices.append(priceInt.find("span", {"class": "price price-int"}).get_text().lstrip('\n').strip(
            ' ') + priceInt.find("span", {"class": "price price-decimal"}).get_text().lstrip('\n').strip(' '))
        counts.append(priceInt.find(
            "span", {"class": "discount"}).get_text().lstrip('\n').strip(' '))

        index = index + 1


def getPriceUrl(bsObj, productUrls):
    index = 0
    for url in bsObj.findAll("a", {"c-emit": "show;click"}):
        if "href" in url.attrs:
            # print("产品链接："+url.attrs["href"])
            productUrls.append(url.attrs["href"])


def writeIO(filePath,products, productUrls, prices, counts, imgUrls):
    with open(filePath, "w+") as f:
        f.write("| 平台  | 产品  | 销量  | 单价 | 产品图 | ")
        f.write("\n")
        f.write(
            "| ------------ | ------------ | ------------ | ------------ | ------------ | ")
        f.write("\n")
        for index in range(0, 10):
            f.write("| 贝贝")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + counts[index])
            f.write(" | " + prices[index])
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")
getLinks("C:Users//trity//Desktop//平台分析-贝贝.txt","http://d.beibei.com/search/item/%E5%AD%95%E5%A6%87%E6%8A%A4%E8%82%A4%E5%93%81----sale_num-1.html")
