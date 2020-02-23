import os
import json 
import pprint
from sodapy import Socrata


data_id = 'nc67-uf89'
client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))

def get_results(page_size, num_pages, output):
    for page in range(num_pages):
        offset = page * page_size
        page_response = client.get(data_id, limit=page_size, offset=offset)

        for record in page_response:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)

    print(len(set()))

def add_record(record, output):

    with open(output, 'r') as json_file: 
        data = json.load(json_file) 
        records = data['results'] 
        records.append(record) 

    with open(output, 'w') as json_file:
        json.dump(results, f, indent=4)


