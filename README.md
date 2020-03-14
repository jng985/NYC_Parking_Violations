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
  
### Python Scripts

- `main.py`

```py
import argparse

from src.bigdata1.api import get_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=None, type=int)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    get_results(args.page_size, args.num_pages, args.output)
 ```

- `src/bigdata1/api.py`

```py
import os
import json 
import pprint
from sodapy import Socrata

data_id = 'nc67-uf89'
client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))
count = int(client.get(data_id, select='COUNT(*)')[0]['COUNT'])

def get_results(page_size, num_pages, output, push_elastic):
    if not num_pages:
        num_pages = count // page_size + 1
    if output:
        create_records(output)
    if push_elastic:
        es = create_and_update_index('bigdata1')
    for page in range(num_pages):
        offset = page * page_size
        page_records = client_get(client, data_id, page_size, offset)
        for record in page_records:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)
            if push_elastic:
                push_record(record, es, 'bigdata1')

def client_get(client, data_id, page_size, offset, max_attempts=8):
    page_records = []
    n_attempts = 0
    while not page_records and n_attempts < max_attempts:
        n_attempts += 1
        try:
            page_records = client.get(data_id, limit=page_size, offset=offset)
        except:
            sleep(n_attempts)
    return page_records

def create_records(output):
    with open(output, 'w') as out_file:
        pass

def add_record(record, output):
    with open(output, 'a') as out_file: 
        out_file.write(json.dumps(record) + '\n')
```

### Docker

  - `Dockerfile`

  ```
  FROM python:3.7

  WORKDIR /app

  COPY . .

  RUN pip install -r requirements.txt
  ```

  - `docker build`
  
    - `-t bigdata1:2.0`
    
  ```console
  $ docker build -t bigdata1:2.0 .
  ```

  - `docker run`
  
    - `-v $(pwd):/app`
    - `-e APP_KEY={*Insert Token Here*}`
    - `-it bigdata1:2.0 /bin/bash`
  
### Usage

#### Arguments

- `--page_size`: 

  - **Required**
  - How many records to request from the API per call.
  
- `--num_pages`: 

  - *Optional*
  - If not provided, continue requesting data until the entirety of the content has been exhausted. 
  - If provided, continue querying for data `num_pages` times.
  
- `--output`: 

  - *Optional*
  - If not provided, print results to stdout. 
  - If provided, write the data to the file `output`.
  
#### Example Commands

- `$soda_token` = environment variable set in `.bash_profile`

- Interactive terminal inside container

  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 /bin/bash
  ```

- Print 2 pages of 3 records per page (6 records)

  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 python -m main --page_size=3 --num_pages=2 
  ```

- Save 2 pages of 3 records per page (6 records) to `results.json`

  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 python -m main --page_size=3 --num_pages=2 --output=results.json
  ```

### Deploy to Dockerhub

- Build docker image if necessary
  ```console
  $ docker build -t bigdata1:2.0 .
  ```

- Get the `UUID` of the desired image
  ```console
  $ docker images | grep bigdata1
  ```

- Tag the image with dockerhub username **with** the version number
  ```console
  $ docker tag {*Insert UUID*} jng985/bigdata1:2.0
  ```

- Push docker image **without** the version number
  ```console
  $ docker push jng985/bigdata1
  ```

### EC2

#### ssh into EC2

- Change directory to the folder containing `.pem` file

- Change `.pem` file permissions to **read-only**
  ```console
  $ chmod 0400 {*Insert .pem File*}
  ```

- ssh into the EC2 instance
  ```console
  $ ssh -i {*Insert .pem File*} ubuntu@{*Insert Public IP*}
  ```

#### Docker setup 

Note: When using docker **within** the EC2 instance, the `sudo` command **must** be run. It is possible to make it so that it isn't required, but this is the case "out of the box".

- Update and install `docker.io`
  ```console
  $ sudo apt-get update
  $ sudo apt install docker.io
  ```

- Log in and pull docker image
  ```console
  $ sudo docker login --username=jng985
  $ sudo docker pull jng985/bigdata1:2.0
  ```

- Export environment variable `APP_KEY`
  ```console
  $ export APP_KEY={*Insert App Token*}
  ```

#### Run docker modules

- `sudo docker run`

  - `-e APP_KEY=${APP_KEY}`
  
  - `-v ${PWD}:/app/out`
  
    - This loads the current working directory into the `out` directory within the docker container
    
  - `-it jng985/bigdata1:2.0`
  
  - `python -m main` 
  
    - `--page_size={*Insert Page Size*}` 
    
    - `--num_pages={*Insert Num Pages*}`
    
    - `--output=./out/{*Insert Output Filename*}`
  
  - if `page_size` and `num_pages` are given, `page_size` * `num_pages` should be printed to stdout
    
#### EC2 Examples
 
 ---
 
  - `page_size=2`
  - `num_pages=2`
 
  ```console
  $ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=2 --num_pages=2
  ```
  
  ```output
  {   'amount_due': '197.96',
      'county': 'BX',
      'fine_amount': '60',
      'interest_amount': '77.96',
      'issue_date': '09/14/2012',
      'issuing_agency': 'POLICE DEPARTMENT',
      'judgment_entry_date': '01/03/2013',
      'license_type': 'PAS',
      'payment_amount': '0',
      'penalty_amount': '60',
      'plate': 'FHW8370',
      'precinct': '040',
      'reduction_amount': '0',
      'state': 'NY',
      'summons_image': {   'description': 'View Summons',
                           'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSTk1FNUVZekpOVkdkNFRWRTlQUT09&locationName=_____________________'},
      'summons_number': '1344761811',
      'violation': 'NO PARKING-EXC. AUTH. VEHICLE',
      'violation_time': '02:50P'}
  {   'amount_due': '125',
      'county': 'NY',
      'fine_amount': '115',
      'interest_amount': '0',
      'issue_date': '01/15/2020',
      'issuing_agency': 'POLICE DEPARTMENT',
      'license_type': 'SRF',
      'payment_amount': '0',
      'penalty_amount': '10',
      'plate': 'GR8ITUDE',
      'precinct': '000',
      'reduction_amount': '0',
      'state': 'NY',
      'summons_image': {   'description': 'View Summons',
                           'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1kNlRYYzlQUT09&locationName=_____________________'},
      'summons_number': '1464913833',
      'violation': 'NO STANDING-BUS LANE',
      'violation_time': '06:17P'}
  {   'amount_due': '75',
      'county': 'NY',
      'fine_amount': '65',
      'interest_amount': '0',
      'issue_date': '01/15/2020',
      'issuing_agency': 'POLICE DEPARTMENT',
      'license_type': 'PAS',
      'payment_amount': '0',
      'penalty_amount': '10',
      'plate': '45E0534',
      'precinct': '000',
      'reduction_amount': '0',
      'state': 'PA',
      'summons_image': {   'description': 'View Summons',
                           'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1jeFRuYzlQUT09&locationName=_____________________'},
      'summons_number': '1464913857',
      'violation': 'FRONT OR BACK PLATE MISSING',
      'violation_time': '06:30P'}
  {   'amount_due': '125',
      'county': 'NY',
      'fine_amount': '115',
      'interest_amount': '0',
      'issue_date': '01/15/2020',
      'issuing_agency': 'POLICE DEPARTMENT',
      'license_type': 'PAS',
      'payment_amount': '0',
      'penalty_amount': '10',
      'plate': '45E0534',
      'precinct': '000',
      'reduction_amount': '0',
      'state': 'PA',
      'summons_image': {   'description': 'View Summons',
                           'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1jeVQxRTlQUT09&locationName=_____________________'},
      'summons_number': '1464913869',
      'violation': 'NO STANDING-BUS LANE',
      'violation_time': '06:30P'}
  ```
  
  
  ```console
  $ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=2 --num_pages=2 --output=./out/results.json 
  ```
  
  **To see what the output file `results.json` looks like:**
  
  ```console
  $ cat results.json
  ```
  
  ```output
  {"plate": "FHW8370", "state": "NY", "license_type": "PAS", "summons_number": "1344761811", "issue_date": "09/14/2012", "violation_time": "02:50P", "violation": "NO PARKING-EXC. AUTH. VEHICLE", "judgment_entry_date": "01/03/2013", "fine_amount": "60", "penalty_amount": "60", "interest_amount": "77.96", "reduction_amount": "0", "payment_amount": "0", "amount_due": "197.96", "precinct": "040", "county": "BX", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSTk1FNUVZekpOVkdkNFRWRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GR8ITUDE", "state": "NY", "license_type": "SRF", "summons_number": "1464913833", "issue_date": "01/15/2020", "violation_time": "06:17P", "violation": "NO STANDING-BUS LANE", "fine_amount": "115", "penalty_amount": "10", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "0", "amount_due": "125", "precinct": "000", "county": "NY", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1kNlRYYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "45E0534", "state": "PA", "license_type": "PAS", "summons_number": "1464913857", "issue_date": "01/15/2020", "violation_time": "06:30P", "violation": "FRONT OR BACK PLATE MISSING", "fine_amount": "65", "penalty_amount": "10", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "0", "amount_due": "75", "precinct": "000", "county": "NY", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1jeFRuYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "45E0534", "state": "PA", "license_type": "PAS", "summons_number": "1464913869", "issue_date": "01/15/2020", "violation_time": "06:30P", "violation": "NO STANDING-BUS LANE", "fine_amount": "115", "penalty_amount": "10", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "0", "amount_due": "125", "precinct": "000", "county": "NY", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1jeVQxRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  ```
  
  ---
  
  - `page_size=10`
  - `num_pages=100`
  - `output=./out/results.json`
  
  ```console
  $ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=10 --num_pages=100 --output=./out/results.json 
  ```
  
  **To print the number of records:**
  
  ```console
  $ cat results.json | wc -l
  ```
  
  ```output
  1000
  ```
  
  ---
  
  - `page_size=8`
  - `num_pages=1`
  - `output=./out/results.json`
  
  ```console
  $ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=8 --num_pages=1 --output=./out/results.json 
  $ cat results.json | wc -l 
  $ cat results.json
  ```
  
  ```output
  8
  {"plate": "CJLS22", "state": "FL", "license_type": "PAS", "summons_number": "1419826750", "issue_date": "01/19/2017", "violation_time": "11:38A", "violation": "NO PARKING-STREET CLEANING", "judgment_entry_date": "05/11/2017", "fine_amount": "45", "penalty_amount": "60", "interest_amount": "25.97", "reduction_amount": "0", "payment_amount": "0", "amount_due": "130.97", "precinct": "026", "county": "NY", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUmVFOVVaM2xPYW1NeFRVRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "CVW7557", "state": "NY", "license_type": "PAS", "summons_number": "8006734926", "issue_date": "11/11/2014", "violation_time": "12:40P", "violation": "EXPIRED MUNI METER", "judgment_entry_date": "02/26/2015", "fine_amount": "35", "penalty_amount": "60", "interest_amount": "41.51", "reduction_amount": "0", "payment_amount": "0", "amount_due": "136.51", "precinct": "104", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPUkd0NVRtYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GFL1292", "state": "NY", "license_type": "PAS", "summons_number": "8006735098", "issue_date": "11/11/2014", "violation_time": "02:55P", "violation": "EXPIRED MUNI METER", "judgment_entry_date": "02/26/2015", "fine_amount": "35", "penalty_amount": "60", "interest_amount": "41.49", "reduction_amount": "0", "payment_amount": "0", "amount_due": "136.49", "precinct": "104", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPVkVFMVQwRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "EHT6039", "state": "NY", "license_type": "PAS", "summons_number": "8006736212", "issue_date": "11/18/2014", "violation_time": "01:24P", "violation": "NO STANDING-TAXI STAND", "judgment_entry_date": "03/05/2015", "fine_amount": "115", "penalty_amount": "60", "interest_amount": "77.49", "reduction_amount": "0", "payment_amount": "0", "amount_due": "252.49", "precinct": "114", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPYWtsNFRXYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "BEL1496", "state": "NC", "license_type": "PAS", "summons_number": "8006736522", "issue_date": "11/21/2014", "violation_time": "10:25A", "violation": "FAIL TO DSPLY MUNI METER RECPT", "judgment_entry_date": "03/12/2015", "fine_amount": "35", "penalty_amount": "60", "interest_amount": "41.17", "reduction_amount": "0", "payment_amount": "0", "amount_due": "136.17", "precinct": "112", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPYWxWNVRXYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GTP6411", "state": "NY", "license_type": "PAS", "summons_number": "8006737216", "issue_date": "11/25/2014", "violation_time": "10:07A", "violation": "NO PARKING-STREET CLEANING", "judgment_entry_date": "03/12/2015", "fine_amount": "45", "penalty_amount": "60", "interest_amount": "46.31", "reduction_amount": "0", "payment_amount": "0", "amount_due": "151.31", "precinct": "110", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPZWtsNFRtYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GNR6165", "state": "NY", "license_type": "OMS", "summons_number": "8006737575", "issue_date": "11/28/2014", "violation_time": "11:42A", "violation": "NO PARKING-STREET CLEANING", "judgment_entry_date": "03/19/2015", "fine_amount": "45", "penalty_amount": "60", "interest_amount": "46.13", "reduction_amount": "0", "payment_amount": "0", "amount_due": "151.13", "precinct": "114", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPZWxVelRsRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GBN2149", "state": "OH", "license_type": "PAS", "summons_number": "8006737782", "issue_date": "11/29/2014", "violation_time": "07:38A", "violation": "FAIL TO DSPLY MUNI METER RECPT", "judgment_entry_date": "03/19/2015", "fine_amount": "35", "penalty_amount": "60", "interest_amount": "41.01", "reduction_amount": "0", "payment_amount": "0", "amount_due": "136.01", "precinct": "109", "county": "Q", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSQmQwNXFZM3BPZW1NMFRXYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  ```
  
  ---
  
  - `page_size=1`
  - `num_pages=8`
  - `output=./out/results.json`
  
  ```console
  $ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=1 --num_pages=8 --output=./out/results.json 
  $ cat results.json | wc -l 
  $ cat results.json
  ```
  
  ```output
  8
  {"plate": "HYZ1824", "state": "NY", "license_type": "PAS", "summons_number": "8663055225", "issue_date": "07/07/2018", "violation_time": "09:07A", "violation": "FAIL TO DSPLY MUNI METER RECPT", "fine_amount": "35", "penalty_amount": "10", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "45", "amount_due": "0", "precinct": "068", "county": "K", "issuing_agency": "TRAFFIC", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWk1rMTZRVEZPVkVsNVRsRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "T754690C", "state": "NY", "license_type": "OMT", "summons_number": "8602839765", "issue_date": "02/08/2018", "violation_time": "11:08A", "violation": "NO PARKING-STREET CLEANING", "fine_amount": "45", "penalty_amount": "0", "interest_amount": "0", "reduction_amount": "45", "payment_amount": "0", "amount_due": "0", "precinct": "109", "county": "Q", "issuing_agency": "TRAFFIC", "violation_status": "HEARING HELD-NOT GUILTY", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWmQwMXFaM3BQVkdNeVRsRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "45E0534", "state": "PA", "license_type": "PAS", "summons_number": "1464913857", "issue_date": "01/15/2020", "violation_time": "06:30P", "violation": "FRONT OR BACK PLATE MISSING", "fine_amount": "65", "penalty_amount": "10", "interest_amount": "0", "reduction_amount": "0", "payment_amount": "0", "amount_due": "75", "precinct": "000", "county": "NY", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUk1rNUVhM2hOZW1jeFRuYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GWW2528", "state": "PA", "license_type": "PAS", "summons_number": "7404230949", "issue_date": "01/15/2010", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VG5wUmQwNUVTWHBOUkdzd1QxRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "V79LBJ", "state": "NJ", "license_type": "PAS", "summons_number": "5106018456", "issue_date": "04/08/2019", "violation_time": "01:32P", "violation": "FAILURE TO STOP AT RED LIGHT", "judgment_entry_date": "07/11/2019", "fine_amount": "50", "penalty_amount": "25", "interest_amount": "4.07", "reduction_amount": "0", "payment_amount": "0", "amount_due": "79.07", "precinct": "000", "county": "BX", "issuing_agency": "DEPARTMENT OF TRANSPORTATION", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGxSRmQwNXFRWGhQUkZFeFRtYzlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "HUG6116", "state": "NY", "license_type": "PAS", "summons_number": "1433962950", "issue_date": "08/11/2018", "violation_time": "04:44A", "violation": "DOUBLE PARKING", "judgment_entry_date": "11/29/2018", "fine_amount": "115", "penalty_amount": "60", "interest_amount": "3.61", "reduction_amount": "0.22", "payment_amount": "178.39", "amount_due": "0", "precinct": "081", "county": "K", "issuing_agency": "POLICE DEPARTMENT", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFZSUmVrMTZhekpOYW1zeFRVRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "Y21HKL", "state": "NJ", "license_type": "PAS", "summons_number": "4641946670", "issue_date": "01/16/2018", "violation_time": "02:02P", "violation": "PHTO SCHOOL ZN SPEED VIOLATION", "judgment_entry_date": "04/12/2018", "fine_amount": "50", "penalty_amount": "25", "interest_amount": "0.01", "reduction_amount": "0", "payment_amount": "75.01", "amount_due": "0", "precinct": "000", "county": "BX", "issuing_agency": "DEPARTMENT OF TRANSPORTATION", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWk1FMVVhekJPYWxrelRVRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  {"plate": "GWR4023", "state": "NY", "license_type": "PAS", "summons_number": "8706513694", "issue_date": "01/23/2019", "violation_time": "09:24A", "violation": "REG. STICKER-EXPIRED/MISSING", "judgment_entry_date": "06/13/2019", "fine_amount": "65", "penalty_amount": "60", "interest_amount": "7.75", "reduction_amount": "0", "payment_amount": "0", "amount_due": "132.75", "precinct": "122", "county": "R", "issuing_agency": "TRAFFIC", "violation_status": "HEARING HELD-GUILTY", "summons_image": {"url": "http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSamQwNXFWWGhOZWxrMVRrRTlQUT09&locationName=_____________________", "description": "View Summons"}}
  ```


## Part 2: Loading into ElasticSearch	

### File Structure

- 2 new files created:
  - `docker-compose.yml`
  - `src/bigdata1/elastic.py`

```console
$ tree
```

```console
.
├── Dockerfile
├── docker-compose.yml
├── main.py
├── requirements.txt
└── src
    └── bigdata1
        ├── api.py
        └── elastic.py
```

- `requirements.txt`

  - Add `elasticsearch` to `requirements.txt`

```
requests
pandas
numpy
sklearn
pytest
pyyaml
matplotlib
pygithub
scipy
sodapy
pprint
elasticsearch
```

### `docker-compose.yml`

```
version: '3'
services:
  pyth:
    network_mode: host
    container_name: pyth
    build:
      context: .
    volumes:
      - .:/app:rw 
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.3.2
    environment: 
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    expose: 
      - "9200"
    ports:
      - "9200:9200"
    
  kibana:
    image: docker.elastic.co/kibana/kibana:6.3.2
    ports:
      - "5601:5601"
```

### Scripts

- `main.py`
  - The only change to `main.py` is adding the `push_elastic` command line argument.

```py
import argparse

from src.bigdata1.api import get_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=None, type=int)
    parser.add_argument("--output", default=None)
    parser.add_argument("--push_elastic", default=False, type=bool)
    args = parser.parse_args()
    
    get_results(args.page_size, args.num_pages, args.output, args.push_elastic)
```

- `src/bigdata1/elastic.py`
  - Script to handle formatting and pushing results to `elasticsearch/kibana`
  - Record Formatting:
    - Changes fields containing `date` to a `date` object
    - Changes fields containing `amount` to a `float` object
  - Results are pushed to Elastic Search with the `summons_number` set as the `id`  
  
```py
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
                m, d, y = map(int, record[key].split('/'))
                if m == 2 and d == 29 and y % 4:
                    m, d = 3, 1
                    record[key] = datetime.date(y, m, d)

def push_record(record, es, index):
    format_record(record)
    res = es.index(index=index, body=record, id=record['summons_number'])
```

- `src/bigdata1/api.py`

  - Add `push_elastic` argument to `get_results`

```py
import os
import json 
import pprint
from time import sleep
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
        es = create_and_update_index('bigdata1')
    for page in range(num_pages):
        offset = page * page_size
        try:
            page_records = client.get(data_id, limit=page_size, offset=offset)
        except:
            sleep(10)
            page_records = client.get(data_id, limit=page_size, offset=offset)
        for record in page_records:
            if output:
                add_record(record, output)
            else:
                pprint.pprint(record, indent=4)
            if push_elastic:
                push_record(record, es, 'bigdata1')


def create_records(output):
    with open(output, 'w') as out_file:
        pass

def add_record(record, output):
    with open(output, 'a') as out_file: 
        out_file.write(json.dumps(record) + '\n')
```

### Elastic Search

  - Build ElasticSearch & Kibana service

  ```console
  $ docker-compose build pyth
  ```

  - Launch ElasticSearch & Kibana service

  ```console
  $ docker-compose up -d
  ```

  - Kill the ElasticSearch & Kibana service

  ```console
  $ docker-compose down
  ```

#### Pushing to ElasticSearch

  - Run the ElasticSearch & Kibana service

  ```console
  $ docker-compose up -d
  ```

  - Run the `main.py` script **with** `--push_elastic=True`
    - The following will push 100,000 records to ElasticSearch
    
  ```console
  $ docker-compose run -e APP_KEY=$soda_token -v ${PWD}:/app/out pyth python -m main --page_size=100 --num_pages=1000 --output=./out/results.json --push_elastic=True
  ```
 
#### Querying ElasticSearch
  
- `curl` requests
  
  - After pushing records to ElasticSearch, we can query ElasticSearch as well using `curl`
  
  - The following command outputs the response of the curl request that returns 5 records from the state of New York to a file `output.txt`. This file is located in the `part2` folder in this repository.
  
  ```console
  $ curl -o output.txt http://localhost:9200/bigdata1/_search?q=state:NY&size=5 
  ```

  - Alternatively, to view the response in the browser, visit the url shown below
    - http://localhost:9200/bigdata1/_search?q=state:NY&size=5
 
  

## Part 3: Visualizing and Analysis on Kibana	

- Visit http://localhost:5601 to launch Kibana

- Create Index Pattern

![](/part3/imgs/kibana1.png)

- Records from the past 5 years in Kibana

![](/part3/imgs/kibana3.png)

### Visualizations


#### Vertical Barchart

- Number of Violations Issue by Issuing Agency

![](/part3/imgs/V1.png)

#### Line Graph

- Monthly Average of Fine Amount, Interest Amount, and Reduction Amount

![](/part3/imgs/V2.png)

#### Pie Chart

- Top 8 Most Frequent Violations

![](/part3/imgs/V3.png)

#### Word Cloud

- Which License Types are given the highest fine amounts on average?

![](/part3/imgs/V4.png)


#### The Dashboard

All 4 visualizations above can be combined into a single dashboard in Kibana. 

![](/part3/imgs/D1.png)

The dashboard updates when the time range is changed. Below it has been changed to show data from the past 4 years.

![](/part3/imgs/D2.png)


## Part 4: Deploying to EC2 Instance	

