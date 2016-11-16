import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取拼多多中开团的部分
'''

# 输出测试


def request_url_print(product_id):
    url = "http://sapi.beibei.com/item/detail/%s.html?biz=pintuan&callback=BeibeiItemDetailGet" % product_id
    r = requests.get(url)
    json_raw = json.loads(r.text.lstrip("BeibeiItemDetailGet(").rstrip(")"))
    print(json_raw['title'])
    # 服务器实践，没有保证与服务器时间对接的准确性
    # print("server_time:" + str(json_raw['server_time']))
    # length = len(json_raw["local_group"])
    # print(length)  # 当有多个开团的情况有用。
    # for index in range(0, length):
    #     dict_str = json_raw["local_group"][index]

    #     dict_map = json.loads(dict_str)
    #     print(dict_map["group_order_id"])
    #     for (k, v) in dict_map.items():
    #         print(k, v)

# 加载对应的商品列表详情


def request_product(product_id):
    url = "http://sapi.beibei.com/item/detail/%s.html?biz=pintuan&callback=BeibeiItemDetailGet" % product_id
    r = requests.get(url)
    json_raw = json.loads(r.text.lstrip("BeibeiItemDetailGet(").rstrip(")"))
    return json_raw['title']


def request_url(product_id):
    if len(product_id) == 0:
        return None
    product_list = []
    url = "http://sapi.beibei.com/fightgroup/visitor_recom/%s-1.html?callback=BeibeiFightgroupRecommendGet" % product_id
    r = requests.get(url)
    json_raw = json.loads(r.text.lstrip("BeibeiFightgroupRecommendGet(").rstrip(")"))
    
    length = len(json_raw["recom_fightgroups"])
    for index in range(0, length):
        # 过滤昵称使用特殊符号无法显示的情况。
        # dict_str = json_raw["recom_fightgroups"][index]
        # dict_str_filter = re.sub(r'\\U\d{3}[a-f0-9]{5}|\\ue\w{3}', '', dict_str)
        dict_map = json_raw["recom_fightgroups"][index]

        product_url = "http://m.beibei.com/mpt/group/detail.html?iid=%s" % product_id
        product_name = request_product(product_id)

        product_list.append(dict(url=product_url, name=product_name, nickName=dict_map[
                            "nick"], finish_time=datetime.fromtimestamp(dict_map["gmt_end"]).strftime('%Y-%m-%d %H:%M:%S')))
    return product_list

# 读取商品列表


def read_product_id(file_path):
    with open(file_path) as file_object:
        return file_object.readlines()


def write_product_spell_group(info_list):
    with open("./product_beibei_spell_group.txt", "w+",encoding='utf-8') as f:
        for index in range(0, len(info_list)):
            f.write(info_list[index] + "\n")


# 主程序调用执行

product_list = read_product_id("./product_beibei_id.txt")

product_group = []
for index in range(0, len(product_list)):
    tmp = request_url(product_list[index].strip())
    if tmp:
        for index_tmp in range(0, len(tmp)):
            if tmp[index_tmp]:
                for(k, v) in tmp[index_tmp].items():
                    product_group.append(v)
                product_group.append("\n")

if len(product_group):
    print(product_group)
    write_product_spell_group(product_group)
