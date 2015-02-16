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


def main():
    args = parser()
    try:
        client = pyalveo.Client(api_key=args.api_key, api_url=API_URL)
        outfile = open(args.output_path, 'w')
        outfile.write(args.api_key)
        outfile.close()
    except pyalveo.APIError as e:
        print("ERROR: " + str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()