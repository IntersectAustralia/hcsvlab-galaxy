import json
import argparse
import pyalveo

API_URL = 'https://app.alveo.edu.au'


def parser():
    the_parser = argparse.ArgumentParser(description="retrieve a Alveo itemlists")
    the_parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    the_parser.add_argument('--output', required=True, action="store", type=str, help="output file path")
    return the_parser.parse_args()


def get_item_lists(api_key):
    item_lists = None
    try:
        client = pyalveo.Client(api_key=api_key, api_url=API_URL)
        item_lists = client.get_item_lists()
    except pyalveo.APIError as e:
        # log.write("ERROR: "+str(e)+"\n")
        pass
    return item_lists


if __name__ == '__main__':
    args = parser()
    item_lists = get_item_lists(args.api_key)
    if item_lists:
        with open(args.output, 'w') as outfile:
            json.dump(item_lists, outfile)
