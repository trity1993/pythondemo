from urllib import request
import json

req = request.Request('http://sapi.beibei.com/fightgroup/visitor_recom/15265364-1.html?callback=BeibeiFightgroupRecommendGet')
# req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k, v in f.getheaders():
        print('%s: %s' % (k, v))
    print('Data:', f.read().decode('utf-8'))
    json_str=f.read().decode('utf-8')
    json_strip=json_str.lstrip("BeibeiFightgroupRecommendGet(").rstrip(")")
    json_success=json.loads(json_strip)
    print(json_success)
    # print(json_success['result']['wall']['docs'])
    # for x in range(0,10):
    #     print(json_success['result']['wall']['docs'][x]['link'])