# NYC Parking Violations

## Part 1: Python Scripting	

### File Structure

  ```console
  $ tree
  ```

  ```console
  .
  ├── Dockerfile
  ├── main.py
  ├── requirements.txt
  └── src
      └── bigdata1
          └── api.py

  2 directories, 4 files
  ```

### Packages 
- Specified in `requirements.txt`
  - `requests`
  - `pandas`
  - `numpy`
  - `sklearn`
  - `pytest`
  - `pyyaml`
  - `matplotlib`
  - `pygithub`
  - `scipy`
  - `sodapy`
  - `pprint`

### Docker

  - `Dockerfile`

  ```
  FROM python:3.7

  WORKDIR /app

  COPY requirements.txt /app

  RUN pip install -r requirements.txt
  ```

  - `docker build`
  
    - `-t bigdata1:1.0`
    
      ```console
      $ docker build -t bigdata1:1.0 .
      ```

  - `docker run`
  
    - `-v $(pwd):/app`
    - `-e APP_KEY={*Insert Token Here*}`
    - `-it bigdata1:1.0 /bin/bash`
    
    
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 /bin/bash
      ```
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main
      ```
      
    - `$soda_token` = environment variable set in `.bash_profile`
  
### Python Scripts

`main.py`
 ```py
  import argparse

  from src.bigdata1.api import get_results, add_record

  if __name__ == "__main__":
      parser = argparse.ArgumentParser()
      parser.add_argument("--page_size", type=int)
      parser.add_argument("--num_pages", default=None, type=int)
      parser.add_argument("--output", default=None)
      args = parser.parse_args()

      get_results(args.page_size, args.num_pages, args.output)
 ```

`src/bigdata1/api.py`
```py
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
```





  
### Usage

#### Arguments

- `--page_size`: 
  - Required 
  - How many records to request from the API per call.
- `--num_pages`: 
  - Optional
  - If not provided, continue requesting data until the entirety of the content has been exhausted. 
  - If provided, continue querying for data `num_pages` times.
- `--output`: 
  - Optional 
  - If not provided, print results to stdout. 
  - If provided, write the data to the file `output`.


```console
$ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main --page_size=3 --num_pages=2 
```
```console
{   'amount_due': '0',
    'county': 'NY',
    'fine_amount': '115',
    'interest_amount': '0',
    'issue_date': '08/17/2018',
    'issuing_agency': 'TRAFFIC',
    'license_type': 'PAS',
    'payment_amount': '125',
    'penalty_amount': '30',
    'plate': 'JJFT37',
    'precinct': '006',
    'reduction_amount': '20',
    'state': 'FL',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVrOUVUWHBPZW1zMVRWRTlQUT09&locationName=_____________________'},
    'summons_number': '8638337991',
    'violation': 'NO STANDING-DAY/TIME LIMITS',
    'violation_time': '05:43P'}
{   'amount_due': '0',
    'county': 'K',
    'fine_amount': '45',
    'interest_amount': '0',
    'issue_date': '11/27/2018',
    'issuing_agency': 'TRAFFIC',
    'license_type': 'SRF',
    'payment_amount': '45',
    'penalty_amount': '0',
    'plate': 'ASX3866',
    'precinct': '071',
    'reduction_amount': '0',
    'state': 'NY',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVFMTZXWHBOYWxGNFRsRTlQUT09&locationName=_____________________'},
    'summons_number': '8613632415',
    'violation': 'NO PARKING-STREET CLEANING',
    'violation_status': 'HEARING HELD-GUILTY',
    'violation_time': '12:17P'}
{   'amount_due': '0',
    'county': 'K',
    'fine_amount': '45',
    'interest_amount': '0',
    'issue_date': '11/27/2018',
    'issuing_agency': 'TRAFFIC',
    'license_type': 'OMS',
    'payment_amount': '45',
    'penalty_amount': '0',
    'plate': 'HTM7725',
    'precinct': '071',
    'reduction_amount': '0',
    'state': 'NY',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVFMTZXWHBOYWxGNlQxRTlQUT09&locationName=_____________________'},
    'summons_number': '8613632439',
    'violation': 'NO PARKING-STREET CLEANING',
    'violation_time': '12:21P'}
{   'amount_due': '0',
    'county': 'Q',
    'fine_amount': '65',
    'interest_amount': '0',
    'issue_date': '09/30/2017',
    'issuing_agency': 'TRAFFIC',
    'license_type': 'PAS',
    'payment_amount': '65',
    'penalty_amount': '0',
    'plate': 'HER6258',
    'precinct': '104',
    'reduction_amount': '0',
    'state': 'NY',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSVk1rMVVVVEJOUkdkM1RtYzlQUT09&locationName=_____________________'},
    'summons_number': '8561440806',
    'violation': 'FRONT OR BACK PLATE MISSING',
    'violation_time': '11:06A'}
{   'amount_due': '0',
    'county': 'QN',
    'fine_amount': '50',
    'interest_amount': '0',
    'issue_date': '09/07/2017',
    'issuing_agency': 'DEPARTMENT OF TRANSPORTATION',
    'license_type': 'PAS',
    'payment_amount': '50',
    'penalty_amount': '0',
    'plate': 'FGN9037',
    'precinct': '000',
    'reduction_amount': '0',
    'state': 'NY',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWmVrNXFZM2hOUkd0NFRsRTlQUT09&locationName=_____________________'},
    'summons_number': '4636710915',
    'violation': 'PHTO SCHOOL ZN SPEED VIOLATION',
    'violation_time': '11:09A'}
{   'amount_due': '0',
    'county': 'Q',
    'fine_amount': '65',
    'interest_amount': '0',
    'issue_date': '10/24/2016',
    'issuing_agency': 'TRAFFIC',
    'license_type': 'PAS',
    'payment_amount': '65',
    'penalty_amount': '0',
    'plate': 'DWT1970',
    'precinct': '109',
    'reduction_amount': '0',
    'state': 'NY',
    'summons_image': {   'description': 'View Summons',
                         'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VG5wUk5VOVVhM3BOVkZrd1RVRTlQUT09&locationName=_____________________'},
    'summons_number': '7499931640',
    'violation': 'REG. STICKER-EXPIRED/MISSING',
    'violation_time': '02:42P'}
```



```console
$ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main --page_size=3 --num_pages=2 --output=results.json
```

`results.json`

```
{
    "results": [
        {
            "plate": "JJFT37",
            "state": "FL",
            "license_type": "PAS",
            "summons_number": "8638337991",
            "issue_date": "08/17/2018",
            "violation_time": "05:43P",
            "violation": "NO STANDING-DAY/TIME LIMITS",
            "fine_amount": "115",
            "penalty_amount": "30",
            "interest_amount": "0",
            "reduction_amount": "20",
            "payment_amount": "125",
            "amount_due": "0",
            "precinct": "006",
            "county": "NY",
            "issuing_agency": "TRAFFIC",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVrOUVUWHBPZW1zMVRWRTlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        },
        {
            "plate": "ASX3866",
            "state": "NY",
            "license_type": "SRF",
            "summons_number": "8613632415",
            "issue_date": "11/27/2018",
            "violation_time": "12:17P",
            "violation": "NO PARKING-STREET CLEANING",
            "fine_amount": "45",
            "penalty_amount": "0",
            "interest_amount": "0",
            "reduction_amount": "0",
            "payment_amount": "45",
            "amount_due": "0",
            "precinct": "071",
            "county": "K",
            "issuing_agency": "TRAFFIC",
            "violation_status": "HEARING HELD-GUILTY",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVFMTZXWHBOYWxGNFRsRTlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        },
        {
            "plate": "HTM7725",
            "state": "NY",
            "license_type": "OMS",
            "summons_number": "8613632439",
            "issue_date": "11/27/2018",
            "violation_time": "12:21P",
            "violation": "NO PARKING-STREET CLEANING",
            "fine_amount": "45",
            "penalty_amount": "0",
            "interest_amount": "0",
            "reduction_amount": "0",
            "payment_amount": "45",
            "amount_due": "0",
            "precinct": "071",
            "county": "K",
            "issuing_agency": "TRAFFIC",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmVFMTZXWHBOYWxGNlQxRTlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        },
        {
            "plate": "EGM4552",
            "state": "NY",
            "license_type": "PAS",
            "summons_number": "8012893095",
            "issue_date": "04/25/2015",
            "violation_time": "04:08P",
            "violation": "INSP. STICKER-EXPIRED/MISSING",
            "judgment_entry_date": "08/13/2015",
            "fine_amount": "65",
            "penalty_amount": "60",
            "interest_amount": "39.09",
            "reduction_amount": "0",
            "payment_amount": "164.09",
            "amount_due": "0",
            "precinct": "105",
            "county": "Q",
            "issuing_agency": "TRAFFIC",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmVFMXFaelZOZWtFMVRsRTlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        },
        {
            "plate": "22461JY",
            "state": "NY",
            "license_type": "COM",
            "summons_number": "1461301208",
            "issue_date": "08/20/2019",
            "violation_time": "11:04A",
            "violation": "SAFETY ZONE",
            "fine_amount": "115",
            "penalty_amount": "10",
            "interest_amount": "0",
            "reduction_amount": "10",
            "payment_amount": "115",
            "amount_due": "0",
            "precinct": "000",
            "county": "NY",
            "issuing_agency": "POLICE DEPARTMENT",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rMVVUWGROVkVsM1QwRTlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        },
        {
            "plate": "036TSD",
            "state": "DP",
            "license_type": "PAS",
            "summons_number": "3284119012",
            "issue_date": "09/17/2098",
            "violation_time": "04:37P",
            "violation": "NO STANDING-EXC. TRUCK LOADING",
            "fine_amount": "55",
            "penalty_amount": "60",
            "interest_amount": "0",
            "reduction_amount": "0",
            "payment_amount": "0",
            "amount_due": "115",
            "precinct": "019",
            "county": "NY",
            "issuing_agency": "PARKING CONTROL UNIT",
            "summons_image": {
                "url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFhwSk5FNUVSWGhQVkVGNFRXYzlQUT09&locationName=_____________________",
                "description": "View Summons"
            }
        }
    ]
}
```

## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

