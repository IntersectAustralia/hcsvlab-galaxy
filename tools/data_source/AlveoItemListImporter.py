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

def write_table(item_lists, filename):
    with open(filename, 'w') as outfile:
        for list_set in item_lists.itervalues():
            for item_list in list_set:
                print item_list
                outfile.write("%s (%d)\t%s\n" % (item_list['name'], item_list['num_items'], item_list['item_list_url']))

if __name__ == '__main__':
    args = parser()
    item_lists = get_item_lists(args.api_key)
    if item_lists:
        write_table(item_lists, args.output)
