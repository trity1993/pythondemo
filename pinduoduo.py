import requests
import json
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
def request_product(product_id):
    url = "http://apiv2.yangkeduo.com/v2/goods/%s" % product_id
    r = requests.get(url)
    json_raw = r.json()
    # print(json_raw["goods_name"])
    return json_raw["goods_name"]

def request_url(product_id):
    if len(product_id)==0:
        return None
    product_list=[]
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
        product_url="http://mobile.yangkeduo.com/goods.html?goods_id=%s" % product_id
        product_name=request_product(product_id)

        product_list.append(dict(url=product_url,name=product_name,nickName=dict_map["nickname"],finish_time=future_time.strftime('%Y-%m-%d %H:%M:%S')))
        # return dict(url=product_url,name=product_name,nickName=dict_map["nickname"],finish_time=future_time.strftime('%Y-%m-%d %H:%M:%S'))
    return product_list

# 读取商品列表
def read_product_id(file_path):
    with open(file_path) as file_object:
        return file_object.readlines()

def write_product_spell_group(info_list):
    # print(info_list)
    product_info_str=""
    with open("./product_spell_group.txt","w+") as f:
        # f.write(json.dumps(info_list)) # 转换成json
        for index in range(0,len(info_list)):
            f.write(info_list[index]+"\n")


# 主程序调用执行

product_list=read_product_id("./product_id.txt")
product_group=[]
for index in range(0,len(product_list)):
    tmp=request_url(product_list[index].strip())
    if tmp:
        for index_tmp in range(0,len(tmp)):
            if tmp[index_tmp]:
                for(k,v) in tmp[index_tmp].items():
                    tmp_data=str(k)+":"+str(v.strip('\ue035').strip('\U0001f48b').strip('\U0001f495').strip('\U0001f459'))
                    product_group.append(tmp_data)
                product_group.append("\n")
    
if len(product_group):
    print(product_group)
    write_product_spell_group(product_group)
