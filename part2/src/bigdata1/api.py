import os
import json 
import pprint
from sodapy import Socrata
from src.bigdata1.elastic import create_and_update_index, push_record

data_id = 'nc67-uf89'
client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))
count = int(client.get(data_id, select='COUNT(*)')[0]['COUNT'])

def get_results(page_size, num_pages, output, push_elastic):
    if not num_pages:
        num_pages = count // page_size + 1
    if output:
        create_records(output)
    if push_elastic:
        es = create_and_update_index('bigdata1', 'violations')
    for page in range(num_pages):
        offset = page * page_size
        page_records = client.get(data_id, limit=page_size, offset=offset)
        for record in page_records:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)
            if push_elastic:
                push_record(record, es, 'bigdata1', 'violations')

def create_records(output):
    with open(output, 'w') as out_file:
        pass

def add_record(record, output):
    with open(output, 'a') as out_file: 
        out_file.write(json.dumps(record) + '\n')




