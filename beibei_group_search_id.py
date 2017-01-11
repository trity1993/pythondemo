import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取贝贝网中所有拼团产品的id
思路是通过找到其中一个拼团，然后通过商品推荐去找下一个拼团，递归后树形最后比对跳出
'''
str_activity_flag="http://b0.hucdn.com/party/2016/11/upload_50f597a934529a38fe89dc53e30dfd59_46x24.png"

# 请求拼团列表url链接
def request_url(product_url):
    url = product_url
    r = requests.get(url)
    json_raw = r.json()

    # 获取对应json的数据
    length = len(json_raw["search_items"])
    print("length:"+str(length))
    # print("活动："+str(json_raw["search_items"][0]["business_icons"][0]["img"]))

    for index in range(0, length):
        dict_map = json_raw["search_items"][index]

        # print("item:"+str(len(dict_map["business_icons"])))

        # 匹配时候为亲恩的产品
        if len(dict_map["business_icons"])>0:
            # print("活动图："+dict_map["business_icons"][0]["img"])
            if dict_map["business_icons"][0]["img"] == str_activity_flag:
                # print("拼团："+str(dict_map["iid"]))
                request_group_link(dict_map["iid"])
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
    "http://api.beibei.com/gateway/route.html?keyword=%E4%BA%B2%E6%81%A9&gender_age=19&client_info=%7B%0A%20%20%22screen%22%20%3A%20%22375x667%22%2C%0A%20%20%22os%22%20%3A%20%2210.2%22%2C%0A%20%20%22platform%22%20%3A%20%22iPhone%22%2C%0A%20%20%22model%22%20%3A%20%22iPhone%22%2C%0A%20%20%22udid%22%20%3A%20%222c6c147046390f2242e71cb00cb96879986b341a%22%2C%0A%20%20%22bd%22%20%3A%20%22App%20Store%22%2C%0A%20%20%22version%22%20%3A%20%225.0.02%22%2C%0A%20%20%22dn%22%20%3A%20%22i6%20plus%22%2C%0A%20%20%22app_name%22%20%3A%20%22beibei%22%0A%7D&channel_type=all&sign=8542E25AF4531029E53679802DE5EA86&brand_ids=0&timestamp=1484065451&filter_sellout=0&session=3c9b8eed27122100586f3f22423c5&welfares=&source=home&cat_ids=0&page=1&page_size=40&sort=hot&method=beibei.item.search")

if len(products):
    # print(products)
    write_product_spell_group(products)
