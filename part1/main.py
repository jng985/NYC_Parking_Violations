import argparse

from src.bigdata1.api import get_results
from src.bigdata1.elastic import push_record

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_size", type=int)
    parser.add_argument("--num_pages", default=None, type=int)
    parser.add_argument("--output", default=None)
    parser.add_argument("--push_elastic", default=False, type=bool)
    args = parser.parse_args()
    
    get_results(args.page_size, args.num_pages, args.output, args.push_elastic)
    



    
