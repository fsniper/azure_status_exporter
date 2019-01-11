#!/usr/bin/python

import re
import time
import requests
import argparse
from pprint import pprint

import os
from sys import exit
from prometheus_client import start_http_server, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY

from azure_status import AzureStatus

DEBUG = int(os.environ.get('DEBUG', '0'))

COLLECTION_TIME = Summary('azure_cloud_status_collector_collect_seconds', 'Time spent to collect metrics from Azure Status')
STATUSES = {
    'good': 0,
    'warning': -1,
    'error': 2
}

class AzureStatusCollector(object):

    def collect(self):
        start = time.time()

        # Request data from Azure Status
        status = self._request_data()

        for region_section in status[1]:
            for category in status[1][region_section]:
                for service in status[1][region_section][category]:
                    for region in status[1][region_section][category][service]:
                        metric_name = "azure_status_{}_{}_status".format(category, service).replace(".", "_")
                        metric = GaugeMetricFamily(metric_name, 'Azure Status for {}'.format(metric_name), labels=["region"])

                        metric.add_metric([region], STATUSES[status[1][region_section][category][service][region]])
                        yield metric

        duration = time.time() - start
        COLLECTION_TIME.observe(duration)

    def _request_data(self):
        a = AzureStatus()
        return a.status()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Azure Status exporter args'
    )
    parser.add_argument(
        '-p', '--port',
        metavar='port',
        required=False,
        type=int,
        help='Listen to this port',
        default=int(os.environ.get('VIRTUAL_PORT', '9999'))
    )
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        port = int(args.port)
        REGISTRY.register(AzureStatusCollector())
        start_http_server(port)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Interrupted")
        exit(0)


if __name__ == "__main__":
    main()
