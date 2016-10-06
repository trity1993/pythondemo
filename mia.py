from urllib.request import urlopen
from bs4 import BeautifulSoup

imgUrls=[]
products=[]
productUrls=[]
prices=[]

def getLinks(filePath,articleUrl):
    global imgUrls,products,productUrls,prices
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html)
    getContent(bsObj,imgUrls,products,productUrls,prices)
    writeIO(filePath,products, productUrls, prices, imgUrls)

# 贝贝网树商品完成+依靠商品找出对应的销售量
def getContent(bsObj,imgUrls,products,productUrls,prices):
    index=0;
    for content in bsObj.findAll("div",{"class":"block"}):
        if index>10:
            break;

        # 产品链接
        # print("url："+content.a.attrs["href"])
        productUrls.append(content.a.attrs["href"])

        # 产品
        # print("title："+content.a.attrs["title"])
        products.append(content.a.attrs["title"])

        # 产品图
        if "data-src" in content.a.img.attrs:
            image=content.a.img.attrs["data-src"]
        else:
            image=content.a.img.attrs["src"]
        # print("img:"+image)
        imgUrls.append(image)

        # 价格
        # print(content.find("span",{"class":"Tahoma f20 pink l blod"}).get_text())
        prices.append(content.find("span",{"class":"Tahoma f20 pink l blod"}).get_text())
        index=index+1

def writeIO(filePath,products, productUrls, prices, imgUrls):
    with open(filePath, "w+") as f:
        f.write("| 平台  | 产品 | 单价 | 产品图 | ")
        f.write("\n")
        f.write(
            "| ------------ | ------------ | ------------ | ------------ | ")
        f.write("\n")
        for index in range(0, 10):
            f.write("| 蜜芽")
            f.write(" | [%s](%s) " % (products[index], productUrls[index]))
            f.write(" | " + prices[index])
            f.write(" | ![](%s)" % imgUrls[index])
            f.write("|\n")

getLinks("D:\python\平台分析-蜜芽.txt","http://www.mia.com/search/s?k=%E5%AD%95%E5%A6%87%E6%8A%A4%E8%82%A4%E5%93%81&order=sales")
