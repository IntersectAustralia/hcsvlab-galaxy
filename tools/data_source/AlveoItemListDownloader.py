import json
import argparse
import pyalveo

API_URL = 'https://app.alveo.edu.au'


def parser():
    the_parser = argparse.ArgumentParser(description="retrieve a Alveo itemlists")
    the_parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    the_parser.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    the_parser.add_argument('--doc_types', required=True, action="store", type=str, help="Item types download")
    the_parser.add_argument('--output_path', required=True, action="store", type=str, help="Output path")
    the_parser.add_argument('--output_id', required=True, action="store", type=str, help="Output ID")
    return the_parser.parse_args()


def get_item_list(api_key, item_list_url):
    client = pyalveo.Client(api_key=api_key, api_url=API_URL)
    return client.get_item_list(item_list_url)

def filter_documents_by_type(item_list, doc_types):
    items = item_list.get_all()
    filtered_documents = []
    for item in items:
        documents = item.get_documents()
        filtered_documents.extend([doc for doc in documents if doc.doc_metadata['dc:type'] in doc_types])
    return filtered_documents

def download_documents(documents, output_path, output_id):
    for document in documents:
        basename, ext = document.get_filename().split('.')
        galaxy_file = "primary_%s_%s_visible_%s" % (output_id, basename, ext)
        document.download_content(output_path, galaxy_file)

def main():
    args = parser()
    try:
        item_list = get_item_list(args.api_key, args.item_list_url) 
        doc_types = args.doc_types.split(',')
        documents = filter_documents_by_type(item_list, doc_types)
        download_documents(documents, args.output_path, args.output_id)
    except pyalveo.APIError as e:
        # log.write("ERROR: "+str(e)+"\n")
        pass

if __name__ == '__main__':
    main()