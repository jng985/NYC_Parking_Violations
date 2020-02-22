import os
import sys
import json
import pprint
import pandas as pd
import numpy as np
import argparse
from functools import reduce

from src.bigdata1.api import get_results, output_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=4, type=int)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
<<<<<<< HEAD
    # print(args)
=======
>>>>>>> 8ab5e7b881b58f9e45791845a1ab2f6d5ef9a988

    response = get_results(args.page_size, args.num_pages)
    
    if args.output:
        output_results(response, args.output)
    else:
        pprint.pprint(response, indent=4)


    
