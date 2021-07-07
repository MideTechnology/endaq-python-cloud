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


def attributes_file(data, _output):
    """
    Writes the attributes to a file for user to see
    :param data: All the attributes for the files
    :param _output: File path
    """
    att_file = open(_output + 'attributes.csv', 'w', newline='')
    csv_writer = csv.writer(att_file)
    csv_writer.writerow(['file_id', 'attribute'])
    for x in data:
        for y in x['attributes']:
            csv_writer.writerow([x['id'], y])


def account_info():
    """
    Makes the account API call and prints info to terminal
    """
    print(URL + '/api/v1/account/info')
    response = requests.get(URL + '/api/v1/account/info', headers=PARAMETERS)
    print(response.json())


def all_files(att, limit, _output):
    """
    Makes the file API call and writes output to files
    :param att: list of attributes to be shown
    :param limit: how many files to be listed
    :param _output: location of output files
    """
    if att == '' and limit == '':
        print(URL + '/api/v1/files')
        response = requests.get(URL + '/api/v1/files', headers=PARAMETERS)
        data = response.json()['data']
    elif att != '' and limit != '':
        print(URL + '/api/v1/files?limit=' + limit + '&attributes=' + att)
        response = requests.get(URL + '/api/v1/files?limit=' + limit + '&attributes=' + att,
                                headers=PARAMETERS)
        data = response.json()['data']
        attributes_file(data, _output)
    elif att == '':
        print(URL + '/api/v1/files?limit=' + limit)
        response = requests.get(URL + '/api/v1/files?limit=' + limit, headers=PARAMETERS)
        data = response.json()['data']
    else:
        print(URL + '/api/v1/files?attributes=' + att)
        response = requests.get(URL + '/api/v1/files?attributes=' + att, headers=PARAMETERS)
        data = response.json()['data']
        attributes_file(data, _output)

    data_file = open(_output + 'files.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    headers = list(data[0].keys())
    headers.remove('attributes')
    csv_writer.writerow(headers)
    for x in data:
        del x['attributes']
        csv_writer.writerow(x.values())


def file_by_id(id_, _output):
    """
    Makes file API call for a specific file and writes information to files
    :param id_: File ID
    :param _output: Output directory
    """
    print(URL + '/api/v1/files/' + id_)
    response = requests.get(URL + '/api/v1/files/' + id_, headers=PARAMETERS)
    data = response.json()

    att_file = open(_output + 'attributes.csv', 'w', newline='')
    csv_writer = csv.writer(att_file)
    headers = list(data['attributes'][0].keys())
    csv_writer.writerow(headers)
    for x in data['attributes']:
        csv_writer.writerow(x.values())

    del data['attributes']
    data_file = open(_output + 'file_' + id_ + '.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    headers = data.keys()
    csv_writer.writerow(headers)
    csv_writer.writerow(data.values())


def devices(_output):
    """
    Lists output of Device API call to file
    :param _output: output file location
    """
    print(URL + '/api/v1/devices/')
    response = requests.get(URL + '/api/v1/devices/', headers=PARAMETERS)
    data = response.json()['data']
    data_file = open(_output + 'devices.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    headers = list(data[0].keys())
    csv_writer.writerow(headers)
    for x in data:
        csv_writer.writerow(x.values())


def device_by_id(id_, _output):
    """
    Writes information for specific device
    :param id_: ID of specific device
    :param _output: output location for information
    """
    print(URL + '/api/v1/devices/' + id_)
    response = requests.get(URL + '/api/v1/devices/' + id_, headers=PARAMETERS)
    data = response.json()
    data_file = open(_output + 'devices.csv', 'w', newline='')
    csv_writer = csv.writer(data_file)
    headers = data.keys()
    csv_writer.writerow(headers)
    csv_writer.writerow(data.values())


def post_attribute(id_, name, type_, value):
    """
    Makes Attribute API call and prints response to terminal
    :param id_: file ID
    :param name: attribute name
    :param type_: attribute type
    :param value: attribute value
    """
    print(URL + '/api/v1/attributes')
    attributes = {"name": name,
                  "type": type_,
                  "value": value,
                  "file_id": id_}
    att = requests.post(URL + '/api/v1/attributes', headers=PARAMETERS, json={"attributes": [attributes]})
    print(att.json())


def main():
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

    parser.add_argument('--url', '-u', default='', help=argparse.SUPPRESS)
    parser.add_argument('--output', '-o', default='')
    args = parser.parse_args()

    print('API Starting')

    # Specifies output directory if one is passed in
    output = './output/'
    if args.output != '':
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        output = args.output
    elif not os.path.exists('./output/'):
        os.makedirs('./output/')

    # changes API url if one is passed in. (ONLY FOR DEVS)
    if args.url != '':
        URL = args.url

    # changes API key if one is passed in
    if args.key != '':
        PARAMETERS.update({"x-api-key": args.key})
    elif args.key == '' and os.environ.get('API_KEY') is None:
        sys.exit('Create a .env with API Key or pass it in with --key')

    if args.command == 'account':
        account_info()
    elif args.command == 'files':
        all_files(args.attributes, args.limit, output)
        print('output can be found in output/files.csv and output/attributes.csv')
    elif args.command == 'file-id' and args.id != '':
        file_by_id(args.id, output)
        print(f'output can be found in output/file_{args.id}.csv and output/attributes.csv')
    elif args.command == 'devices':
        devices(output)
        print('output can be found in devices.csv')
    elif args.command == 'device-id' and args.id != '':
        device_by_id(args.id, output)
        print('output can be found in devices.csv')
    elif args.command == 'attribute':
        if args.name is not None and args.type is not None and args.value is not None and args.id is not None:
            post_attribute(args.id, args.name, args.type, args.value)
        else:
            sys.exit('id, name, type, and value can\'t be empty')
    else:
        sys.exit('Use -h for help with commands.')


if __name__ == '__main__':
    main()
