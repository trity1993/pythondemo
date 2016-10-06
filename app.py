from urllib import request
import json

req = request.Request('http://list.mogujie.com/search?callback=jQuery211021242388869344575_1475684894493&priceList=%5B50%2C+100%2C+100%2C+150%2C+150%2C+200%5D&_version=1&_mgjuuid=b91a69e3-040c-4412-83d7-a6bde71608c6&sort=sell&cpc_offset=&cKey=pc-search-wall&page=1&q=%25E5%25AD%2595%25E5%25A6%2587%25E6%258A%25A4%25E8%2582%25A4%25E5%2593%2581&userId=&ppath=&maxPrice=&minPrice=&ratio=2%3A3&_=1475684894494')
req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    # print('Data:', f.read().decode('utf-8'))
    json_str=f.read().decode('utf-8')
    json_strip=json_str.lstrip("/**/jQuery211021242388869344575_1475684894493(").rstrip(");")
    json_success=json.loads(json_strip)
    # print(json_success['result']['wall']['docs'])
    for x in range(0,10):
        print(json_success['result']['wall']['docs'][x]['link'])