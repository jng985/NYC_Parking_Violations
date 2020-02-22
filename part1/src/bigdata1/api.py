import os
import sys
import requests
import collections

from sodapy import Socrata

data_id = 'nc67-uf89'

def get_results(page_size, num_pages=4, output=None):
    client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))
    pages = {}
    for page in range(num_pages):
        offset = page * page_size
        page_response = client.get(data_id, limit=page_size, offset=offset)
        pages[page] = page_response

    return pages

def output_results(pages):
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


