import requests
import json
import re
from datetime import datetime, timedelta

'''
抓取拼多多中开团的部分
'''

# 输出测试


def request_url_print(product_id):
    url = "http://apiv2.yangkeduo.com/goods/%s/local_group" % product_id
    r = requests.get(url)
    json_raw = r.json()
    # 服务器实践，没有保证与服务器时间对接的准确性
    print("server_time:" + str(json_raw['server_time']))
    length = len(json_raw["local_group"])
    print(length)  # 当有多个开团的情况有用。
    for index in range(0, length):
        dict_str = json_raw["local_group"][index]

        dict_map = json.loads(dict_str)
        print(dict_map["group_order_id"])
        for (k, v) in dict_map.items():
            print(k, v)

# 加载对应的商品列表详情


def request_product(product_id, goods_item_price=0):
    url = "http://apiv2.yangkeduo.com/v2/goods/%s" % product_id
    r = requests.get(url)
    json_raw = r.json()

    group_product_item = json_raw["group"]
    for x in range(0, len(group_product_item)):
        if group_product_item[x]["customer_num"] == 2:
            goods_item_price = group_product_item[x]["price"]

    return json_raw["goods_name"], goods_item_price / 100  # 返回商品名称和价格


def request_url(product_id, goods_item_price_sum=0):
    if len(product_id) == 0:  # 判断分割好的情况
        return goods_item_price_sum, None
    product_list = []  # 存储多个开团的情况
    url = "http://apiv2.yangkeduo.com/goods/%s/local_group" % product_id
    r = requests.get(url)
    json_raw = r.json()
    server_time = json_raw['server_time']  # 得到服务器时间
    length = len(json_raw["local_group"])

    for index in range(0, length):
        dict_str = json_raw["local_group"][index]
        dict_str_filter = re.sub(
            r'\\U\d{3}[a-f0-9]{5}|\\ue\w{3}', '', dict_str)  # 过滤昵称使用特殊符号无法显示的情况。
        dict_map = json.loads(dict_str_filter)
        # 计算对应的时间
        expire_time = dict_map["expire_time"]
        time = int(expire_time) - server_time
        now = datetime.now()  # 得到当前时间
        future_time = now + timedelta(hours=time / 3600)
        product_url = "http://mobile.yangkeduo.com/goods.html?goods_id=%s" % product_id
        product_name, product_price = request_product(product_id)

        goods_item_price_sum = goods_item_price_sum + product_price  # 逐个求和

        product_info = product_url + "\r\n" + product_name + "\r\n" + dict_map["nickname"] + "\r\n" + str(
            product_price) + "\r\n" + future_time.strftime('%Y-%m-%d %H:%M:%S') + "\r\n"

        product_list.append(dict(product_info=product_info,
                                 time_stamp=time))
    return goods_item_price_sum, product_list

# 读取商品列表


def read_product_id(file_path):
    with open(file_path) as file_object:
        return file_object.readlines()


def write_product_spell_group(info_list):
    with open("./product_pinduoduo_spell_group.txt", "w+", encoding='utf-8') as f:
        for index in range(0, len(info_list)):
            f.write(info_list[index]["product_info"] + "\n")


def product_sort_sum(product_group, product_sum_qinn,product_sum_lan):
    if len(product_group):
        L = sorted(product_group, key=lambda s: s["time_stamp"])

        L.append(dict(product_info="亲恩总金额：" + str(product_sum_qinn)))
        L.append(dict(product_info="兰可欣总金额：" + str(product_sum_lan)))

        write_product_spell_group(L)
    else:
        print(product_group.append("暂时无任何的开团情况"))


# 主程序调用执行

product_list = read_product_id("./product_pinduoduo_id.txt")
product_group_qinn = []
product_group_lan = []
product_str = ""
product_sum_qinn =0
product_sum_lan = 0
flag = True
for index in range(0, len(product_list)):
    goods_item_price_sum, tmp = request_url(product_list[index].strip())
    if tmp:
        for index_tmp in range(0, len(tmp)):
            if flag:
                if tmp[index_tmp]:
                    product_group_qinn.append(tmp[index_tmp])
                    product_sum_qinn = goods_item_price_sum + product_sum_qinn
            else:
                if tmp[index_tmp]:
                    product_group_lan.append(tmp[index_tmp])
                    product_sum_lan = goods_item_price_sum + product_sum_lan
    elif tmp is None:
        flag = False

product_group_qinn.extend(product_group_lan) # 使用extend合并list
product_sort_sum(product_group_qinn, product_sum_qinn,product_sum_lan)

# if len(product_group):
#     L = sorted(product_group, key=lambda s: s["time_stamp"])
#     # print(L)
#     L.append(dict(product_info=str(product_sum)))
#     write_product_spell_group(L)
# else:
#     print(product_group.append("暂时无任何的开团情况"))
