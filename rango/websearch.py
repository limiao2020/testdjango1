__author__ = 'limiao'

import json
import urllib.parse
import urllib.request
import os.path

def read_txdata_api():
    web_txdata_api = None
    filepath = 'search.key'
    if not os.path.isfile(filepath):
        filepath = '..\search.key'

    try:
        with open(filepath, 'r') as f:
            web_txdata_api = f.readline().strip()
            print(web_txdata_api)

    except:
        raise IOError('search.key file not found! ')
    return web_txdata_api

def run_query(search_terms, size=10):
    web_txdata_api = read_txdata_api()

    if not web_txdata_api:
        raise KeyError('web_txdata_api not found!')

    root_url = 'http://api.tianapi.com/generalnews/index'

    query_str = urllib.parse.quote(search_terms)
    search_url = '{root_url}?key={web_txdata_api}&word={query_str}&num=10'.format(root_url = root_url,web_txdata_api = web_txdata_api,query_str = query_str)

    result = []
    try:
        response = urllib.request.urlopen(search_url).read().decode('utf-8')
        json_response = json.loads(response)
        if json_response['code'] == 200:
           result = json_response['newslist']

    except:
        print("Error when querying the Webhose API")

    return result

# 从这开始执行
if __name__ == '__main__':
    print("Starting script...")
    search_str = input('input：')
    result_strs = run_query(search_str)
    print(result_strs)
    for item in result_strs:
        for key,value in item.items():
            print(key+":"+ str(value))
        print('')