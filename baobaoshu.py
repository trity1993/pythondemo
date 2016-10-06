from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

# 实战 
products=[]
productUrls=[]
prices=[]
counts=[]
imgUrls=[]

def getLinks(filePath,articleUrl):
    global products, productUrls, prices, counts, imgUrls
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html)
    getImages(imgUrls, bsObj)
    getTitle(bsObj,products,productUrls)
    getDetail(bsObj,prices,counts)
    writeIO(filePath,products, productUrls, prices, counts, imgUrls)

# 完成宝宝树商品图片的抓图
def getImages(imgUrls, bsObj):
    for x in range(1,11):
        findFlag='search_list_c%d_pic%d' % (x,x)
        for imgLink in bsObj.find("a",{"data-track":findFlag}).findAll('img'):
            if 'src' in imgLink.attrs:
                newImg=imgLink.attrs['src']
                # print("img: " + newImg)
                imgUrls.append(newImg)

# 宝宝树商品完成
def getTitle(bsObj,products,productUrls):
    for x in range(1,11):
        findFlag='search_list_c%d_name%d' % (x,x)
        for content in bsObj.findAll("a",{"data-track":findFlag}):
            # print("url:"+content.attrs["href"])
            # print("content:"+content.get_text())
            products.append(content.get_text())
            productUrls.append(content.attrs["href"])

def getDetail(bsObj,prices,counts):
    index = 0
    for productDetail in bsObj.findAll("span",{"class":"r2"}):
        if index>11:
            break
        # print("价格："+productDetail.ins.get_text())
        # print("销售数量："+productDetail.em.get_text())
        prices.append(productDetail.ins.get_text()) 
        counts.append(productDetail.em.get_text())

def writeIO(filePath,products, productUrls, prices, counts, imgUrls):
    with open(filePath, "w+") as f:
        f.write("| 平台  | 产品  | 销量  | 单价 | 产品图 | ")
        f.write("\n")
        f.write(
            "| ------------ | ------------ | ------------ | ------------ | ------------ | ")
        f.write("\n")
        for index in range(0, 10):
            f.write("| 美囤")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + counts[index]+" | ")
            f.write(prices[index].lstrip("\xa5"))
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")


getLinks("D:\python\平台分析-美囤-销量.txt","http://search.meitun.com/search/itempage?key=%E5%AD%95%E5%A6%87%E6%8A%A4%E8%82%A4%E5%93%81&fcategid=&pageSize=20&pageNo=1&slprice=0&salesvolume=1&hasInventoryOnly=0&brandid=&specificationid=") # 按销量排列时候，暂时无法找出对应的请求链接
