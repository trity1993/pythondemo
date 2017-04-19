import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取贝贝网中所有拼团产品的id
思路是通过找到其中一个拼团，然后通过商品推荐去找下一个拼团，递归后树形最后比对跳出
没请求一次，做一次运算来进行请求签名一次。所以下一页无法简单的加载进来
'''
str_activity_flag="拼团"

# 请求拼团列表url链接
def request_url(product_url):
    url = product_url
    r = requests.get(url)
    json_raw = r.json()

    # 获取对应json的数据
    length = len(json_raw["search_items"])
    print("length:"+str(length))
    print("活动："+str(json_raw["search_items"][0]["business_text"]))

    for index in range(0, length):
        dict_map = json_raw["search_items"][index]

        # 匹配时候为亲恩的产品
        if dict_map["business_text"]==str_activity_flag:
            print("活动ID:"+str(dict_map["iid"]))
            products.append(dict_map["iid"])
            # request_group_link(dict_map["iid"])
    return None

def write_product_spell_group(products):
    with open("./product_beibei_id.txt", "w+", encoding='utf-8') as f:
        for index in range(0, len(products)):
            f.write(str(products[index]) + "\n")


# 主程序调用执行
products = []

request_url(
    "http://api.beibei.com/gateway/route?client_info=%7B%22bd%22%3A%22qd55%22%2C%22package%22%3A%22show%22%2C%22os%22%3A%227.1.1%22%2C%22screen%22%3A%221440x2392%22%2C%22model%22%3A%22Nexus+6P%22%2C%22dn%22%3A%22Nexus+6P%22%2C%22udid%22%3A%2265eb9d7228ca6b47%22%2C%22version%22%3A%224.8.8%22%2C%22platform%22%3A%22Android%22%2C%22network%22%3A%22WiFi%22%7D&method=beibei.item.search&gender_age=0&sign=DFA5F00791AA0E8844DD6363A4D7AC39&filter_sellout=0&sort=hot&source=home&price_min=0&welfares=0&cat_ids=0&brand_ids=0&page=1&keyword=%E4%BA%B2%E6%81%A9&channel_type=all&price_max=0&page_size=40&timestamp=1489078066")

if len(products):
    # print(products)
    write_product_spell_group(products)
