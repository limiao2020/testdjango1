__author__ = 'limiao'

import json
import urllib.parse
import urllib.request

def read_txdata_api():
    web_txdata_api = None

    try:
        with open('search.key', 'r') as f:
           web_txdata_api = f.readline().strip()
    except:
        raise IOError('search.key file not found! ')
    return web_txdata_api

def run_query(search_terms, size=10):
    web_txdata_api = read_txdata_api()

    if