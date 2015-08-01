#!/usr/bin/env python

import argparse
import json
import requests


API_ENDPOINT = 'https://api.digitalocean.com/v2'


def do_request(api_key, method, path, params):
    headers = {'Authorization': "Bearer %s" % api_key, 'Content-Type': 'application/json'}

    url = '%s/%s' % (API_ENDPOINT, path)

    if method.lower() == 'get':
        return requests.get(url, params=params, headers=headers, timeout=60).json()
    elif method.lower() == 'post':
        return requests.post(url, data=json.dumps(params), headers=headers, timeout=60).json()
    elif method.lower() == 'put':
        return requests.put(url, params=params, headers=headers, timeout=60).json()

def get_external_ip():
    ip_request = requests.get('https://api.ipify.org?format=json')
    return ip_request.json()['ip']

def do_dydns(api_key, domain_name, record_name):
    ip = get_external_ip()

    print 'Found external ip of %s' % (ip, )

    records = [
        r for r
        in do_request(api_key, 'get', '/domains/%s/records/' % (domain_name, ), {})['domain_records']
        if r['name'] == record_name
    ]

    if records:
        print 'Record %s exists, updating' % (record_name, )
        params = {
            'name': record_name,
            'type': 'A',
            'data': ip
        }
        print do_request(api_key, 'put', '/domains/%s/records/%s' % (domain_name, records[0]['id']), params)
    else:
        print 'Record %s not found, creating' % (record_name, )
        params = {
            'name': record_name,
            'type': 'A',
            'data': ip
        }
        print do_request(api_key, 'post', '/domains/%s/records' % (domain_name, ), params)


parser = argparse.ArgumentParser(description='DigitalOcean Dynamic DNS')
parser.add_argument('-a', '--api_key', required=True, help='DigitalOcean v2 api key')
parser.add_argument('-d', '--domain-name', required=True, help='Domain name managed by DigitalOcean (eg: example.com)')
parser.add_argument('-r', '--record-name', required=True, help='Short form DNS name, either subdomain or @ for the domain itself (eg: @ or home)')
args = parser.parse_args()

do_dydns(args.api_key, args.domain_name, args.record_name)
