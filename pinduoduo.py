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
        print("product_id:",product_id)
        print("nickName:",dict_map["nickname"])
        print(future_time)

def read_product_id(file_path):
    file_object = open(file_path) 
    try: 
      all_the_text = file_object.readlines() 
      # print(all_the_text) 
      return all_the_text
    finally: 
      file_object.close() 

# 主程序调用执行

# 没有填完所有的商品
product_list=read_product_id("D:/python/product_id.txt")
# print(len(product_list))
for index in range(0,len(product_list)):
    # print(product_list[index].rstrip("\n"))
    request_url(product_list[index].rstrip("\n"))

