from datetime import datetime
from elasticsearch import Elasticsearch

def create_and_update_index(index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
        es.indices.put_mapping(index=index_name, doc_type=doc_type)
    except:
        pass
    return es

def format_record(record):
    for key, value in record.items():
        if 'amount' in key:
            record[key] = float(value)
        elif 'date' in key:
            record[key] = datetime.strptime(record[key], '%m/%d/%Y').date()

def push_record(record, es, index, doc_type):
    format_record(record)
    id = record['summons_number']
    res = es.index(index=index, doc_type=doc_type, body=record, id=id)
    print(res['result'], 'Summons_# %s' % id)

   