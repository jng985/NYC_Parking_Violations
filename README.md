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
    - `-e APP_KEY={Insert Token Here}`
      - `$soda_token` = environment variable set in `.bash_profile`
    - `-it bigdata1:1.0 /bin/bash`
    
    
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 /bin/bash
      ```
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main
      ```
  
### Python Scripts

`main.py`
  ```py
  if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=4, type=int)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    response = get_results(args.page_size, args.num_pages)
    if args.output:
        output_results(response, args.output)
    else:
        pprint.pprint(response, indent=4)
  ```

`src/bigdata1/api.py`
  ```py
  data_id = 'nc67-uf89'
  client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))

  def get_results(page_size, num_pages):
    pages = {}
    for page in range(num_pages):
        offset = page * page_size
        page_response = client.get(data_id, limit=page_size, offset=offset)
        pages[page] = page_response
    return pages

  def output_results(results, output):
      with open(output, 'w', encoding='utf-8') as f:
          json.dump(results, f, ensure_ascii=False, indent=4)
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
```json
{   0: [   {   'amount_due': '0',
               'county': 'BK',
               'fine_amount': '50',
               'interest_amount': '0',
               'issue_date': '08/19/2019',
               'issuing_agency': 'DEPARTMENT OF TRANSPORTATION',
               'license_type': 'PAS',
               'payment_amount': '75',
               'penalty_amount': '25',
               'plate': 'GYA1764',
               'precinct': '000',
               'reduction_amount': '0',
               'state': 'NY',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWk1rMTZXWGhQUkZWNVRXYzlQUT09&locationName=_____________________'},
               'summons_number': '4663618522',
               'violation': 'PHTO SCHOOL ZN SPEED VIOLATION',
               'violation_time': '06:59P'},
           {   'amount_due': '0',
               'county': 'QN',
               'fine_amount': '50',
               'interest_amount': '0',
               'issue_date': '08/29/2019',
               'issuing_agency': 'DEPARTMENT OF TRANSPORTATION',
               'license_type': 'PAS',
               'payment_amount': '50',
               'penalty_amount': '25',
               'plate': 'HFJ6860',
               'precinct': '000',
               'reduction_amount': '25',
               'state': 'NY',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWk1rNUVVVFZPVkUxNlRVRTlQUT09&locationName=_____________________'},
               'summons_number': '4664495330',
               'violation': 'PHTO SCHOOL ZN SPEED VIOLATION',
               'violation_time': '07:28P'},
           {   'amount_due': '0',
               'county': 'NY',
               'fine_amount': '115',
               'interest_amount': '5.33',
               'issue_date': '04/17/2019',
               'issuing_agency': 'TRAFFIC',
               'judgment_entry_date': '08/01/2019',
               'license_type': 'PAS',
               'payment_amount': '180.2',
               'penalty_amount': '60',
               'plate': 'K54KBY',
               'precinct': '033',
               'reduction_amount': '0.13',
               'state': 'NJ',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VDBSWk5FNUVVVEJPYW1zeFRWRTlQUT09&locationName=_____________________'},
               'summons_number': '8684446951',
               'violation': 'NO STANDING-DAY/TIME LIMITS',
               'violation_status': 'HEARING HELD-GUILTY',
               'violation_time': '10:45A'}],
    1: [   {   'amount_due': '0',
               'county': 'BK',
               'fine_amount': '50',
               'interest_amount': '0',
               'issue_date': '08/15/2019',
               'issuing_agency': 'DEPARTMENT OF TRANSPORTATION',
               'license_type': 'PAS',
               'payment_amount': '50',
               'penalty_amount': '25',
               'plate': 'HCC4188',
               'precinct': '000',
               'reduction_amount': '25',
               'state': 'NY',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWk1rMXFZek5PZWtVMVRuYzlQUT09&locationName=_____________________'},
               'summons_number': '4662777197',
               'violation': 'PHTO SCHOOL ZN SPEED VIOLATION',
               'violation_time': '01:08P'},
           {   'amount_due': '0',
               'county': 'BK',
               'fine_amount': '50',
               'interest_amount': '0',
               'issue_date': '08/15/2019',
               'issuing_agency': 'DEPARTMENT OF TRANSPORTATION',
               'license_type': 'PAS',
               'payment_amount': '50',
               'penalty_amount': '25',
               'plate': 'GRZ9770',
               'precinct': '000',
               'reduction_amount': '25',
               'state': 'NY',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VGtSWk1rMXFZek5PZWtVeVRWRTlQUT09&locationName=_____________________'},
               'summons_number': '4662777161',
               'violation': 'PHTO SCHOOL ZN SPEED VIOLATION',
               'violation_time': '12:49P'},
           {   'amount_due': '115',
               'county': 'NY',
               'fine_amount': '55',
               'interest_amount': '0',
               'issue_date': '10/25/2099',
               'issuing_agency': 'POLICE DEPARTMENT',
               'license_type': 'PAS',
               'payment_amount': '0',
               'penalty_amount': '60',
               'plate': '132THD',
               'precinct': '017',
               'reduction_amount': '0',
               'state': 'DP',
               'summons_image': {   'description': 'View Summons',
                                    'url': 'http://nycserv.nyc.gov/NYCServWeb/ShowImage?searchID=VFhwTk5VMTZSVEJPVkZWNFRrRTlQUT09&locationName=_____________________'},
               'summons_number': '3393145514',
               'violation': 'NO STANDING-EXC. TRUCK LOADING',
               'violation_time': '10:19A'}]}
```

  

## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

