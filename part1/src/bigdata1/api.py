import os
import json 
import pprint
from sodapy import Socrata

data_id = 'nc67-uf89'
client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))
count = int(client.get(data_id, select='COUNT(*)')[0]['COUNT'])

def get_results(page_size, num_pages, output):
    if not num_pages:
        num_pages = count // page_size + 1

    if output:
        create_records(output)

    for page in range(num_pages):
        offset = page * page_size
        page_records = client.get(data_id, limit=page_size, offset=offset)

        for record in page_records:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)

def create_records(output):
    with open(output, 'w') as json_file:
        init = {'results': []}
        json.dump(init, json_file, indent=4)


def add_record(record, output):

    with open(output) as json_file: 
        data = json.load(json_file) 
        records = data['results'] 
        records.append(record) 
    
    with open(output, 'w') as json_file:
        json.dump(data, json_file, indent=4)




