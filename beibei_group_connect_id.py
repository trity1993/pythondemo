import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取贝贝网中所有拼团产品的id
思路是通过找到其中一个拼团，然后通过商品推荐去找下一个拼团，递归后树形最后比对跳出
'''


# 请求拼团列表url链接
def request_url(product_url):
    url = product_url
    r = requests.get(url)
    json_raw = r.json()

    # 获取对应json的数据
    length = len(json_raw["fightgroup_items"])
    for index in range(0, length):
        dict_map = json_raw["fightgroup_items"][index]

        # 匹配时候为亲恩的产品
        if "亲恩" not in dict_map["title"]:
            continue

        print("排名：" + str(index))
        products.append(dict_map["iid"])
        print("对应产品id：" + str(dict_map["iid"]))
        print("产品名：" + dict_map["title"])

        # 请求当前拼团的参团的各项信息，进行类的调用
        #

        # 获取其关联上的对应的id
        request_group_link(dict_map["iid"])
        break

        # 需要一个容器装入，便于以后的重复遍历
    return None

# 获取拼团推荐关联的亲恩的产品
def request_group_link(iid):
    base_url = "http://sapi.beibei.com/gateway/route"
    # 参数准备
    client_info = {'bd': 'qd55', 'package': 'show', 'os': '7.0', 'screen': '1440x2392', 'imei': "867982021973996",
                   "model": "Nexus 6P", "dn": "Nexus 6P", "udid": "928b90f92deaf1fc", "version": "4.8.8", "platform": "Android", "network": "WiFi"}
    json_client_info = json.dumps(client_info)
    # 参数打包
    param_info = {'client_info': json_client_info, 'event_id': '101174002', 'method': 'beibei.recom.list.get', 'iid': iid,
                  'scene_id': 'app_item_detail_bei_ma_recom', 'sign': '1D59284CF1D61C68264234B8376BEEFD', 'timestamp': '1479619935'}

    product_link = requests.get(base_url, params=param_info).json()
    length = len(product_link["recom_items"])
    # print("length=" + str(length))
    for index in range(0, length):
        product_link_temp = product_link["recom_items"][index]
        if product_link_temp["iid"] not in products:
            if "亲恩" not in product_link_temp["title"] :
                continue
            products.append(product_link_temp["iid"])

            print(product_link_temp["title"],product_link_temp["iid"])
            request_group_link(product_link_temp["iid"])
 
def write_product_spell_group(products):
    with open("./product_beibei_id.txt", "w+", encoding='utf-8') as f:
        for index in range(0, len(products)):
            f.write(str(products[index]) + "\n")


# 主程序调用执行
products = []

request_url(
    "http://sapi.beibei.com/item/fightgroup/2-40-today_group-beauty-440000.html")

if len(products):
    # print(products)
    write_product_spell_group(products)
