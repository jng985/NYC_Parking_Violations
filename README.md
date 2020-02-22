# NYC Parking Violations

## Part 1: Python Scripting	

- `requirements.txt`

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
```

- Docker

  - `Dockerfile`

```
FROM python:3.7

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt
```

  - `docker build`
  
  ```console
  $ docker build -t bigdata1:1.0 .
  ```

  - `docker run`
  
    - `-v $(pwd):/app`
    - `-e APP_KEY={Insert Token Here}`
    - `-it bigdata1:1.0 /bin/bash`
    
  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 /bin/bash
  ```
  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main.py
  ```
  ```console
  $ docker run -v $(pwd):/app -e APP_KEY=$soda_token -it bigdata1:1.0 python -m main.py --page_size=10
  ```
  
  `$soda_token` = environment variable in `.bash_profile`
  
    


## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

