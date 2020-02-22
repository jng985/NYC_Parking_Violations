import os
import sys
import json

from src.bigdata1.api import get_results

if __name__ == "__main__":
    kwargs  = {}
    for arg in sys.argv[1:]:
        key, value = arg.split('=')
        kwargs[key] = value 
    
    print(kwargs)
    page_size = kwargs['--page_size']
    response = get_results(page_size)
    print(response)