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

getLinks("http://d.beibei.com/search/item/%E5%AD%95%E5%A6%87%E6%8A%A4%E8%82%A4%E5%93%81----sale_num-1.html")