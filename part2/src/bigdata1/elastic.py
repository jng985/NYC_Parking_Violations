from datetime import datetime, date
from elasticsearch import Elasticsearch

def create_and_update_index(index_name):
    es = Elasticsearch()
    try:
        es.indices.create(index=index_name)
    except:
        pass
    return es

def format_record(record):
    for key, value in record.items():
        if 'amount' in key:
            record[key] = float(value)
        elif 'date' in key:
            try:
                record[key] = datetime.strptime(record[key], '%m/%d/%Y').date()
            except:
                try:
                    m, d, y = map(int, record[key].split('/'))
                    if m == 2 and d == 29 and y % 4:
                        m, d = 3, 1
                        record[key] = datetime.date(y, m, d)
                except:
                    pass

def push_record(record, es, index):
    format_record(record)
    res = es.index(index=index, body=record, id=record['summons_number'])
    
    

   