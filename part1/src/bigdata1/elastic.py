from datetime import datetime
from elasticsearch import Elasticsearch

def get_record_datetime(issue_date, violation_time):
    record_dt = issue_date + violation_time + 'M'
    dt = datetime.strptime(record_dt, '%m/%d/%Y%I:%M%p')
    return dt

def get_record_datetime(record):
    issue_date = record['issue_date']
    violation_time = record['violation_time']
    dt_string = issue_date + violation_time + 'M'
    dt = datetime.strptime(dt_string, '%m/%d/%Y%I:%M%p')
    return dt

es = Elasticsearch()

def push_record(record, id):
    # record = {"plate": "88040MH", "state": "NY", "license_type": "COM", "summons_number": "4008752961", "issue_date": "05/23/2018", "violation_time": "03:32P", "violation": "BUS LANE VIOLATION", "fine_amount": "115", "penalty_amount": "0", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "115", "amount_due": "0", "precinct": "000", "county": "QN", "issuing_agency": "DEPARTMENT OF TRANSPORTATION", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSQmQwOUVZekZOYW1zeVRWRTlQUT09&locationName=_____________________", "description": "View Summons"}}
    record['timestamp'] = get_record_datetime(record)
    index = 'violations'
    doc_type = 'violation'
    res = es.index(index=index, doc_type=doc_type, body=record, id=id)

    # print(res['result'])

    # res = es.get(index=index, doc_type=doc_type, id=1)
    # print(res['_source'])

