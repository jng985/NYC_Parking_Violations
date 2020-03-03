from datetime import datetime
from elasticsearch import Elasticsearch

def create_and_update_index(index_name, doc_type):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
        es.indices.put_mapping(index=index_name, doc_type=doc_type)
    except Exception:
        pass

    return es

def format_record(record):
    if 'violation_time' in record:
        violation_time = record['violation_time']
        if violation_time[:2] == '00':
            violation_time = '12' + violation_time[2:]
        record['violation_time'] = datetime.strptime(violation_time + 'M', '%I:%M%p')
    
    issue_date = record['issue_date']
    record['issue_date'] = datetime.strptime(issue_date, '%m/%d/%Y')

    for key, value in record.items():
        if 'amount' in key:
            record[key] = float(value)




def push_record(record, es):
    format_record(record)
    index = 'violations'
    doc_type = 'violation'
    
    res = es.index(index=index, doc_type=doc_type, body=record)
    print(res['result'])

   