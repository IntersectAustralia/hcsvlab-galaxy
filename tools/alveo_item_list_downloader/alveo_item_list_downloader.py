from __future__ import print_function
import json
import argparse
import pyalveo
import sys
import os

API_URL = 'https://app.alveo.edu.au' # TODO: export constants to a separate module

def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    parser.add_argument('--doc_types', required=True, action="store", type=str, help="Item types to download")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output file")
    return parser.parse_args()

def get_item_list(api_key, item_list_url):
    client = pyalveo.Client(api_key=api_key, api_url=API_URL)
    return client.get_item_list(item_list_url)

# TODO: export common function to helper module
def filter_documents_by_type(item_list, doc_types):
    """Filters and Item List to the specified document types.

    :type item_list: pyalveo.ItemList
    :param item_list: Item List to filter

    :type doc_types: list of String
    :param doc_types: pyalveo.Document types to filter from the set
        [Audio, Original, Raw, Text, TextGrid, Video, unspecified]
    """
    items = item_list.get_all()
    filtered_documents = []
    for item in items:
        documents = item.get_documents()
        filtered_documents.extend([doc for doc in documents if doc.doc_metadata['dc:type'] in doc_types])
    return filtered_documents

# TODO: export common function to helper module
def download_documents(documents, output_path):
    """
    Downloads a list of documents to the directory specificed by output_path.

    :type documents: list of pyalveo.Document
    :param documents: Documents to download

    :type output_path: String
    :param output_path: directory to download to the documents to
    """
    for document in documents:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        document.download_content(output_path)

def main():
    args = parser()
    try:
        api_key = open(args.api_key, 'r').read()
        item_list = get_item_list(api_key, args.item_list_url) 
        doc_types = args.doc_types.split(',')
        documents = filter_documents_by_type(item_list, doc_types)
        download_documents(documents, args.output_path)
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()