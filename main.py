import argparse
import sys

import requests
import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

URL = 'https://qvthkmtukh.execute-api.us-west-2.amazonaws.com/master'
PARAMETERS = {
        "x-api-key": os.environ.get('API_KEY')
    }


def api():
    print('API')


def account_info():
    response = requests.get(URL + '/api/v1/account/info', headers=PARAMETERS)
    print(response.json())


def all_files(att, limit):
    if att == '' and limit == '':
        response = requests.get(URL + '/api/v1/files', headers=PARAMETERS)
        print(response.json())
    elif att != '' and limit != '':
        response = requests.get(URL + '/api/v1/files?limit=' + args.limit + '&attributes=' + args.attributes,
                                headers=PARAMETERS)
        print(response.json())
    elif att == '':
        response = requests.get(URL + '/api/v1/files?limit=' + args.limit, headers=PARAMETERS)
        print(response.json())
    else:
        response = requests.get(URL + '/api/v1/files?attributes=' + args.attributes, headers=PARAMETERS)
        print(response.json())


def file_by_id(_id):
    response = requests.get(URL + '/api/v1/files/' + _id, headers=PARAMETERS)
    print(response.json())


def devices():
    response = requests.get(URL + '/api/v1/devices/', headers=PARAMETERS)
    print(response.json())


def device_by_id(_id):
    response = requests.get(URL + '/api/v1/devices/' + _id, headers=PARAMETERS)
    print(response.json())


def post_attribute(_id, name, _type, value):
    attributes = {"name": name,
                  "type": _type,
                  "value": value,
                  "file_id": _id}
    att = requests.post(URL + '/api/v1/attributes', headers=PARAMETERS, json={"attributes": [attributes]})
    print(att.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['files', 'file-id', 'devices', 'device-id', 'account', 'attribute'])
    parser.add_argument('--id', '-i', default='', help='Device or File id')
    parser.add_argument('--attributes', '-a', default='', help='What attributes you want to view; default is none, '
                                                               'can be all, or att1,att2,...')
    parser.add_argument('--limit', '-l', default='', help='How many values you want returned; Max 100')
    parser.add_argument('--key', '-k', default='', help='API key if it is not in the .env file')
    parser.add_argument('--name', '-n', help='Name of new attribute')
    parser.add_argument('--type', '-t', help='Type of element the new attribute is')
    parser.add_argument('--value', '-v', help='Value of new attribute')
    args = parser.parse_args()

    if args.key != '':
        PARAMETERS.update({"x-api-key": args.key})
    if args.command == 'account':
        account_info()
    elif args.command == 'files':
        all_files(args.attributes, args.limit)
    elif args.command == 'file-id':
        file_by_id(args.id)
    elif args.command == 'devices':
        devices()
    elif args.command == 'device-id':
        device_by_id(args.id)
    elif args.command == 'attribute':
        if args.name is not None and args.type is not None and args.value is not None and args.id is not None:
            post_attribute(args.id, args.name, args.type, args.value)
        else:
            sys.exit('id, name, type, and value can\'t be empty')
