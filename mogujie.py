from urllib import request
import json
import datetime

# 实战 
products=[]
productUrls=[]
prices=[]
counts=[]
imgUrls=[]

def getLinks(filePath,articleUrl):
    global products, productUrls, prices, counts, imgUrls
    req=request.Request(articleUrl)
    getContent(products, productUrls, prices, counts, imgUrls,req)
    writeIO(filePath,products, productUrls, prices, counts, imgUrls)

# 完成蘑菇街ajax的json数据抓取
def getContent(products, productUrls, prices, counts, imgUrls, req):
    with request.urlopen(req) as f:
        json_origin=f.read().decode('utf-8')
        json_filter=json_origin.lstrip("/**/jQuery211021242388869344575_1475684894493(").rstrip(");")
        json_success=json.loads(json_filter)
        for x in range(0,10):
            productUrls.append(json_success['result']['wall']['docs'][x]['link'])
            products.append(json_success['result']['wall']['docs'][x]['title'])
            prices.append(json_success['result']['wall']['docs'][x]['price'])
            counts.append(json_success['result']['wall']['docs'][x]['cfav']) # 无法看到销量，收藏代替
            imgUrls.append(json_success['result']['wall']['docs'][x]['img'])

def writeIO(filePath,products, productUrls, prices, counts, imgUrls):
    with open(filePath, "w+") as f:
        f.write("| 平台  | 产品数量  | 收藏  | 单价 | 产品图 | ")
        f.write("\n")
        f.write(
            "| ------------ | ------------ | ------------ | ------------ | ------------ | ")
        f.write("\n")
        for index in range(0, 10):
            f.write("| 蘑菇街")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + str(counts[index])+" | ")
            f.write(str(prices[index]))
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")

getLinks("D:\python\平台分析-蘑菇街-销量.txt","http://list.mogujie.com/search?callback=jQuery211021242388869344575_1475684894493&priceList=%5B50%2C+100%2C+100%2C+150%2C+150%2C+200%5D&_version=1&_mgjuuid=b91a69e3-040c-4412-83d7-a6bde71608c6&sort=sell&cpc_offset=&cKey=pc-search-wall&page=1&q=%25E5%25AD%2595%25E5%25A6%2587%25E6%258A%25A4%25E8%2582%25A4%25E5%2593%2581&userId=&ppath=&maxPrice=&minPrice=&ratio=2%3A3&_=1475684894494")
