import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取贝贝网中开团的部分
'''

# 输出测试


def request_url_print(product_id):
    url = "http://sapi.beibei.com/item/detail/%s.html?biz=pintuan&callback=BeibeiItemDetailGet" % product_id
    r = requests.get(url)
    json_raw = json.loads(r.text.lstrip("BeibeiItemDetailGet(").rstrip(")"))
    print(json_raw['title'])

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

        product_info=product_url+ "\r\n"+product_name+ "\r\n"+dict_map["nick"]+"\r\n"+datetime.fromtimestamp(dict_map["gmt_end"]).strftime('%Y-%m-%d %H:%M:%S')

        product_list.append(dict(info=product_info,time=dict_map["gmt_end"]-dict_map["gmt_begin"]))
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
        # 排序
        L=sorted(tmp, key=lambda s: s["time"])
        for index_tmp in range(0, len(L)):
            if L[index_tmp]:
                # print("test=",L[index_tmp]["info"])
                product_group.append(L[index_tmp]["info"])
                product_group.append("\n")

if len(product_group):
    # pass
    print(product_group)
    write_product_spell_group(product_group)
else:
    write_product_spell_group(product_group.append("暂无拼团数据"))    
