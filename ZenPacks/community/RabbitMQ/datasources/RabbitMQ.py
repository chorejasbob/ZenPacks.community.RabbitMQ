#!/usr/bin/env python

import json
import requests
from requests.auth import HTTPBasicAuth
import argparse

# Disable HTTPS verification failure warnings.
import urllib3
urllib3.disable_warnings()

parser = argparse.ArgumentParser('Pull rabbitmq queues values.')
parser.add_argument(
    "-u",
    "--username",
    help="RabbitMQ Username",
    required=True
    )
parser.add_argument(
    "-p",
    "--password",
    help="RabbitMQ Password",
    required=True
    )
parser.add_argument(
    "--url",
    help="RabbitMQ Web Administration URL",
    required=True
    )

args = parser.parse_args()

# setting up credentials:
user = args.username
url = args.url
password = args.password
credentials = 'user, password'
data = {}
results = {}
results['values'] = {}
session = requests.Session()
session.auth = credentials


def get_queues():
    try:
        response = session.get(
            url,
            auth=HTTPBasicAuth(user, password),
            verify=False
            )
    except requests.exceptions.RequestException as e:
        results['events'] = [
            {
                "severity": 5,
                "summary": "RabbitMQ collection",
                "message": str(e),
                "eventClass": "/Status",
                "eventKey": "rabbitQueues",
                "component": "rabbitQueues"
            }
        ]
        print json.dumps(results)
        return results
    if response.status_code == 200:
        json_data = response.json()
        for vhost in json_data:
            data[vhost['name'].replace('.', '_')] = vhost['messages']
        results['values']['rabbitQueues'] = data
        results['events'] = [
            {
                "severity": 0,
                "summary": "RabbitMQ collection",
                "message": "Collection successful: " + str(response.status_code),
                "eventClass": "/Status",
                "eventKey": "rabbitQueues",
                "component": "rabbitQueues"
            }
        ]
        print json.dumps(results)
        return results
    else:
        results['events'] = [
            {
                "severity": 5,
                "summary": "RabbitMQ collection",
                "message": (response.status_code, response.text),
                "eventClass": "/Status",
                "eventKey": "rabbitQueues",
                "component": "rabbitQueues"
            }
        ]
        print json.dumps(results)
        return results

get_queues()
