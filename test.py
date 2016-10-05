from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

# 实战 
def getLinks(articleUrl):
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html)
    
    print(bsObj)
    # getTitle(bsObj)

    # getPrice(bsObj)getPriceUrl
    # getPriceUrl(bsObj)

# 蘑菇街商品完成+依靠商品找出对应的销售量
def getTitle(bsObj):
    index=0;
    for content in bsObj.findAll("a",{"class":"img J_dynamic_imagebox loading_bg_120"}):
        if index>10:
            break;
        if "href" in content.attrs:
            product=content.attrs["href"]
            print(product)

            # img=bsObj.find("img",{"title":product})
            # print("产品首图："+img.attrs['src'])
            # print("产品："+product)
            # way=content.find("span",{"class":"my-tag"})
            # if way:
            #     print("活动方式"+way.get_text())

            index=index+1
# 对应的产品销售数量+单价 优化==需要进行去掉空格和换行
def getPrice(bsObj): 
    index=0;
    for priceInt in bsObj.findAll("span",{"class":"price-info "}):
        if index>10:
            break;
        print("销量:"+priceInt.find("span",{"class":"discount"}).get_text())
        print("单价:"+priceInt.find("span",{"class":"price price-int"}).get_text()+priceInt.find("span",{"class":"price price-decimal"}).get_text())
        index=index+1

def getPriceUrl(bsObj):
    index=0
    for url in bsObj.findAll("a",{"c-emit":"show;click"}):
        if "href" in url.attrs:
            print("产品链接："+url.attrs["href"])
        pass

getLinks("http://list.mogujie.com/search?callback=jQuery211021242388869344575_1475684894493&priceList=%5B50%2C+100%2C+100%2C+150%2C+150%2C+200%5D&_version=1&_mgjuuid=b91a69e3-040c-4412-83d7-a6bde71608c6&sort=sell&cpc_offset=&cKey=pc-search-wall&page=1&q=%25E5%25AD%2595%25E5%25A6%2587%25E6%258A%25A4%25E8%2582%25A4%25E5%2593%2581&userId=&ppath=&maxPrice=&minPrice=&ratio=2%3A3&_=1475684894494")