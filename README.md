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

`main.py`
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
    
    
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 /bin/bash
      ```
      ```console
      $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 python -m main
      ```
      
    - `$soda_token` = environment variable set in `.bash_profile`
  
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


```console
$ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:2.0 python -m main --page_size=3 --num_pages=2 
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

- Export environment variable `APP_KEY` if necessary
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
    
```console
$ sudo docker run -e APP_KEY=${APP_KEY} -v ${PWD}:/app/out -it jng985/bigdata1:2.0 python -m main --page_size=3 --num_pages=2 --output=./out/results.json
```

- Checking the number of records in `results.json`
  - if `page_size` and `num_pages` are given, `page_size` * `num_pages` should be printed to stdout
    ```console
    $ cat results.json | wc -l
    ```

## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

