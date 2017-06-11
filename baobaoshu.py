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
num_len=21

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
    for x in range(1,num_len):
        findFlag='search_list_c%d_pic%d' % (x,x)
        for imgLink in bsObj.find("a",{"data-track":findFlag}).findAll('img'):
            if 'src' in imgLink.attrs:
                newImg=imgLink.attrs['src']
                # print("img: " + newImg)
                imgUrls.append(newImg)

# 宝宝树商品完成
def getTitle(bsObj,products,productUrls):
    for x in range(1,num_len):
        findFlag='search_list_c%d_name%d' % (x,x)
        for content in bsObj.findAll("a",{"data-track":findFlag}):
            # print("url:"+content.attrs["href"])
            # print("content:"+content.get_text())
            products.append(content.get_text())
            productUrls.append(content.attrs["href"])

def getDetail(bsObj,prices,counts):
    index = 0
    for productDetail in bsObj.findAll("span",{"class":"r2"}):
        if index>num_len:
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
        for index in range(0, num_len-1):
            f.write("| 美囤")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + counts[index]+" | ")
            f.write(prices[index].lstrip("\xa5"))
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")
key_qinen="http://search.meitun.com/searchpage?key=%E4%BA%B2%E6%81%A9"
key_dsmm="http://search.meitun.com/searchpage?key=%E8%A2%8B%E9%BC%A0%E5%A6%88%E5%A6%88"
key_zc="http://search.meitun.com/searchpage?key=%E5%AD%90%E5%88%9D%E5%A6%88%E5%A6%88"
key_wy="http://search.meitun.com/searchpage?key=%E4%BA%94%E7%BE%8A%E5%A6%88%E5%92%AA"
key_ymy="http://search.meitun.com/searchpage?key=%E4%BC%98%E7%BE%8E%E5%AD%95"

getLinks("D:\python\平台分析-美囤-销量.txt",key_ymy)
