from __future__ import print_function
import json
import argparse
import pyalveo
import os
from urlparse import urlparse

def parser():
    parser = argparse.ArgumentParser(description="Downloads documents in an Alveo Item List")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--item_list_url', required=True, action="store", type=str, help="Item List to download")
    parser.add_argument('--doc_types', required=True, action="store", type=str, help="Item types to download")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="Path to output files")
    parser.add_argument('--output_log', required=True, action="store", type=str, help="Path to output log file")
    parser.add_argument('--metadata', required=True, action="store", type=str, help="Import metadata")
    parser.add_argument('--concat', required=True, action="store", type=str, help="Concatenate all text documents into one galaxy document")
    return parser.parse_args()

# TODO: export common function to helper module
def get_item_list(api_key, item_list_url):
    parsed_uri = urlparse(item_list_url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    client = pyalveo.Client(api_key=api_key, api_url=domain)
    return client.get_item_list(item_list_url)

# TODO: export common function to helper module
def filter_item_list_documents_by_type(item_list, doc_types):
    items = item_list.get_all()
    filtered_documents = []
    for item in items:
        documents = item.get_documents()
        filtered_documents.extend([doc for doc in documents if doc.metadata()['dc:type'] in doc_types])
    return filtered_documents

def filter_documents_by_type(documents, doc_types):
    filtered_documents = []
    filtered_documents.extend([doc for doc in documents if doc.metadata()['dc:type'] in doc_types])
    return filtered_documents

# TODO: export common function to helper module
def download_documents(documents, output_path):
    for document in documents:
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        document.download_content(output_path)

def download_metadata(item_list, output_path):
    for item in item_list.get_all():
        name = str(item.url()).split("/")[-1]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        doc_path = os.path.join(output_path, name+' metadata-document'+'.txt')
        metadata_doc = open (doc_path, 'w')
        metadata_doc.write(str(item.metadata()['alveo:metadata']))

def download_concatenated_documents(item_list, output_path):
    concatenated_content = ""
    for item in item_list.get_all():
        if str(item.metadata()['alveo:primary_text_url'])!= "No primary text found":
            concatenated_content = concatenated_content + "\n\n" + str(item.get_primary_text())
    if concatenated_content != "":
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        doc_path = os.path.join(output_path, 'concatenated_texts.txt')
        concatenated_doc = open (doc_path, 'w')
        concatenated_doc.write(concatenated_content)

def write_log(args, item_list, doc_types):
    log = open (args.output_log, 'a')      
    log.write("Alveo Import Tool.\n\n")        
    log.write("User input parameters are as follows: \n")      
    log.write("\t Item List URI: "+args.item_list_url+"\n")       
    log.write("\t API-KEY: "+args.api_key+"\n")     
    log.write("\t Job Name: "+args.output_log+"\n")        
    log.write("\t Import File Types: "+args.doc_types+"\n")     
    log.write("\t Import Metadata: "+args.metadata+"\n")      
    log.write("\t Concatenate Text Files: "+args.concat+"\n\n")
    log.write("This item list contains "+str(len(item_list))+" items.\n\n")
    for item in item_list.get_all():
        log.write("ITEM: " +str(item.url()) + "\n")
        if args.metadata == "true":
            log.write("---- metadata document: "+(str(item.metadata()['alveo:metadata']))[:100]+"...\n")
        for document in item.get_documents():
            if document.metadata()['dc:type'] in doc_types:
                log.write("---- document: "+str(document.url())+"\n")

def main():
    args = parser()
    try:
        item_list = get_item_list(args.api_key, args.item_list_url) 
        doc_types = args.doc_types.split(',')
        documents = filter_item_list_documents_by_type(item_list, doc_types)
        if (args.concat == "true"):
            download_concatenated_documents(item_list, args.output_path)
            # if concatenating the text documents, filter out the text typed documents out of the documents to download
            text_type = "Text"
            non_text_doc_types = list(doc_types)
            if text_type in non_text_doc_types:
                non_text_doc_types.remove(text_type)
            documents = filter_documents_by_type(documents, non_text_doc_types)
        download_documents(documents, args.output_path)
        write_log(args, item_list, doc_types)
        if args.metadata == "true":
            download_metadata(item_list, args.output_path)
    except pyalveo.APIError as e:
        import sys
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()