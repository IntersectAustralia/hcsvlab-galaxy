from __future__ import print_function
import json
import argparse
import pyalveo


API_URL = 'https://app.alveo.edu.au'


def parser():
    parser = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--output', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()


def get_item_lists(api_key):
    client = pyalveo.Client(api_key=api_key, api_url=API_URL)
    return client.get_item_lists()

def write_table(item_lists, filename):
    with open(filename, 'w') as outfile:
        for list_set in item_lists.itervalues():
            for item_list in list_set:
                outfile.write("%s (%d)\t%s\n" % (item_list['name'], item_list['num_items'], item_list['item_list_url']))

def main():
    args = parser()
    try:
        item_lists = get_item_lists(args.api_key)
        if item_lists:
            write_table(item_lists, args.output)
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)
    

if __name__ == '__main__':
    main()
