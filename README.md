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
  
  `$soda_token` = environment variable set in `.bash_profile`
  
### Python Scripts

`main.py`
  ```py
  if __name__ == "__main__":
      kwargs  = {}
      for arg in sys.argv[1:]:
          key, value = arg.split('=')
          kwargs[key] = value 

      print(kwargs)
      page_size = kwargs['--page_size']
      response = get_results(page_size)

      pprint.pprint(response)
  ```

`src/bigdata1/api.py`
  ```py
  data_id = 'nc67-uf89'
  client = Socrata('data.cityofnewyork.us', os.environ.get("APP_KEY"))

  def get_results(page_size, num_pages=4, output=None):
      pages = {}
      for page in range(num_pages):
          offset = page * page_size
          page_response = client.get(data_id, limit=page_size, offset=offset)
          pages[page] = page_response
          print(pd.DataFrame(page_response))
      return pages
      
  def output_results(pages):
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
  ```
  
  

## Part 2: Loading into ElasticSearch	


## Part 3: Visualizing and Analysis on Kibana	


## Part 4: Deploying to EC2 Instance	

