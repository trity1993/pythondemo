import requests
import json
from datetime import datetime, timedelta


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

def request_url(product_id):
    url = "http://apiv2.yangkeduo.com/goods/%s/local_group" % product_id
    r = requests.get(url)
    json_raw = r.json()
    server_time=json_raw['server_time']
    length = len(json_raw["local_group"])
    # print(length)  # 当有多个开团的情况有用。
    for index in range(0, length):
        dict_str = json_raw["local_group"][index]
        dict_map = json.loads(dict_str)
        expire_time=dict_map["expire_time"]
        time=int(expire_time)-server_time
        now=datetime.now() # 得到当前时间
        future_time=now+timedelta(hours=time/3600)
        print("nickName:",dict_map["nickname"])
        print(future_time)

# 主程序调用执行

# 没有填完所有的商品
product_list=["729878-6224262","729888-6224323","729945-6224466","729947-6224468"]
for index in range(0,len(product_list)):
    request_url(product_list[index])

