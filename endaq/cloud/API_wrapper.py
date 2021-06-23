import argparse
import sys

import requests
import os
from dotenv import load_dotenv, find_dotenv
import csv

load_dotenv(find_dotenv())

URL = 'https://qvthkmtukh.execute-api.us-west-2.amazonaws.com/master'
PARAMETERS = {
        "x-api-key": os.environ.get('API_KEY')
    }


def attributes_file(data):
    att_file = open('../../output/attributes.csv', 'w')
    csv_writer = csv.writer(att_file)
    count = 0
    for x in data:
        for y in x['attributes']:
            if count == 0:
                csv_writer.writerow(['file_id', 'attribute'])
                count += 1
            csv_writer.writerow([x['id'], y])
        x.update({'attributes': []})


def account_info():
    response = requests.get(URL + '/api/v1/account/info', headers=PARAMETERS)
    print(response.json())


def all_files(att, limit):
    data = None
    if att == '' and limit == '':
        response = requests.get(URL + '/api/v1/files', headers=PARAMETERS)
        data = response.json()['data']
    elif att != '' and limit != '':
        response = requests.get(URL + '/api/v1/files?limit=' + args.limit + '&attributes=' + args.attributes,
                                headers=PARAMETERS)
        data = response.json()['data']
        attributes_file(data)
    elif att == '':
        response = requests.get(URL + '/api/v1/files?limit=' + args.limit, headers=PARAMETERS)
        data = response.json()['data']
    else:
        response = requests.get(URL + '/api/v1/files?attributes=' + args.attributes, headers=PARAMETERS)
        data = response.json()['data']
        attributes_file(data)

    data_file = open('../../output/files.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for x in data:
        if count == 0:
            headers = x.keys()
            csv_writer.writerow(headers)
            count += 1
        csv_writer.writerow(x.values())


def file_by_id(_id):
    response = requests.get(URL + '/api/v1/files/' + _id, headers=PARAMETERS)
    data = response.json()

    att_file = open('../../output/attributes.csv', 'w')
    csv_writer = csv.writer(att_file)
    count = 0
    for x in data['attributes']:
        if count == 0:
            csv_writer.writerow(x.keys())
            count += 1
        csv_writer.writerow(x.values())
    data.update({'attributes': []})

    data_file = open('output/file_' + _id + '.csv', 'w')
    csv_writer = csv.writer(data_file)
    headers = data.keys()
    csv_writer.writerow(headers)
    csv_writer.writerow(data.values())


def devices():
    response = requests.get(URL + '/api/v1/devices/', headers=PARAMETERS)
    data = response.json()['data']
    data_file = open('../../output/devices.csv', 'w')
    csv_writer = csv.writer(data_file)
    count = 0
    for x in data:
        if count == 0:
            headers = x.keys()
            csv_writer.writerow(headers)
            count += 1
        csv_writer.writerow(x.values())


def device_by_id(_id):
    response = requests.get(URL + '/api/v1/devices/' + _id, headers=PARAMETERS)
    data = response.json()
    data_file = open('../../output/devices.csv', 'w')
    csv_writer = csv.writer(data_file)
    headers = data.keys()
    csv_writer.writerow(headers)
    csv_writer.writerow(data.values())


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

    if not os.path.exists('../../output/'):
        os.makedirs('../../output/')

    if args.key != '':
        PARAMETERS.update({"x-api-key": args.key})
    elif args.key == '' and os.environ.get('API_KEY') is None:
        sys.exit('Create a .env with API Key or pass it in with --key')
    
    if args.command == 'account':
        account_info()
    elif args.command == 'files':
        all_files(args.attributes, args.limit)
        print('output can be found in output/files.csv and output/attributes.csv')
    elif args.command == 'file-id' and args.id != '':
        file_by_id(args.id)
        print(f'output can be found in output/file_{args.id}.csv and output/attributes.csv')
    elif args.command == 'devices':
        devices()
        print('output can be found in devices.csv')
    elif args.command == 'device-id' and args.id != '':
        device_by_id(args.id)
        print('output can be found in devices.csv')
    elif args.command == 'attribute':
        if args.name is not None and args.type is not None and args.value is not None and args.id is not None:
            post_attribute(args.id, args.name, args.type, args.value)
        else:
            sys.exit('id, name, type, and value can\'t be empty')
    else:
        sys.exit('Use -h for help with commands.')
