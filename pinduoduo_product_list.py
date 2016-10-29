import requests
import json
import datetime

'''
通过分析竞争对手类似产品的售价，更好的调整自己的价格
'''

# 实战 
products=[]
productUrls=[]
prices=[]
counts=[]
imgUrls=[]

def getLinks(filePath,shop_url):
    global products, productUrls, prices, counts, imgUrls
    req=requests.get(shop_url).json()
    getContent(products, productUrls, prices, counts, imgUrls,req)
    writeIO(filePath,products, productUrls, prices, counts, imgUrls)

def getContent(products, productUrls, prices, counts, imgUrls, req):
    product_list=req["goods_list"]
    length=len(product_list)
    for index in range(0,length):
        productUrls.append("http://mobile.yangkeduo.com/goods.html?goods_id=%d" % product_list[index]["goods_id"] )
        products.append(product_list[index]["goods_name"])
        imgUrls.append(product_list[index]["thumb_url"])
        counts.append(product_list[index]["cnt"])
        prices.append("常规价: %.2f,开团价格: %.2f "% (product_list[index]["normal_price"]/100,product_list[index]["group"]["price"]/100))

def writeIO(filePath,products, productUrls, prices, counts, imgUrls):
    with open(filePath, "w+") as f:
        f.write("| 产品  | 销售数量  | 价格 | 产品图 | ")
        f.write("\n")
        f.write(
            "| ------------ | ------------ | ------------ | ------------ | ")
        f.write("\n")
        for index in range(0, len(products)):
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + str(counts[index])+" | ")
            f.write(str(prices[index]))
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")
    # 清空设置操作
    products.clear()
    productUrls.clear()
    prices.clear()
    counts.clear()
    imgUrls.clear()

id_dict=dict(袋鼠妈妈=14844,子初=6135,五羊=7477)
for (k,v) in id_dict.items():
    getLinks("D:\python\%s-价格列表.txt" % k,"http://api-static.yangkeduo.com/v2/mall/%d/goods?page=1&size=50&sort_type=GMV" % v)
