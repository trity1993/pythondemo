from urllib import request
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
            f.write("| 袋鼠妈妈")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + str(counts[index])+" | ")
            f.write(str(prices[index]))
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")

getLinks("D:\python\袋鼠妈妈-价格列表.txt","http://api-static.yangkeduo.com/operation/37/groups?opt_type=3&offset=0&size=100")
