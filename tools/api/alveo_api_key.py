from __future__ import print_function
import argparse
import pyalveo
import sys

API_URL = 'https://app.alveo.edu.au'

def parser():
    parser = argparse.ArgumentParser(description="Retrieves Alveo Item Lists")
    parser.add_argument('--api_key', required=True, action="store", type=str, help="Alveo API key")
    parser.add_argument('--output_path', required=True, action="store", type=str, help="File to store the API key in")
    return parser.parse_args()

def write_key(api_key, output_path, client_module=pyalveo):
    client = client_module.Client(api_key, API_URL)
    outfile = open(output_path, 'w')
    outfile.write(api_key)
    outfile.close()

def main():
    args = parser()
    try:
        write_key(args.api_key, args.output_path)
    except Exception as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()