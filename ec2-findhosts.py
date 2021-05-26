#!/usr/local/bin/python3
#
import argparse
import logging
import boto3
import sys


parser = argparse.ArgumentParser(description='Arguments ec2 find hosts script.')


parser.add_argument(
    '--region',
    dest='region',
    required=True,
    help='Region to filter of'
)

parser.add_argument(
    '--phase',
    dest='phase',
    required=True,
    help='Phase to filter of'
)

parser.add_argument(
    '--territory',
    dest='territory',
    default='*',
    help='Territory to filter of'
)


parser.add_argument(
    '--product',
    dest='product',
    default='*',
    help='Product to filter of'
)


# logging class
logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# load arguments
results = parser.parse_args()

region=results.region
phase=results.phase
territory=results.territory
product=results.product
tagName=phase+"-"+territory+"-"+product+"-*"


ec2 = boto3.client('ec2',region)
reservations = ec2.describe_instances(
    Filters=[ 
            {'Name': 'tag:Name',
             'Values': [tagName]}
        ]
    )

for reservation in reservations["Reservations"] :
    for instance in reservation["Instances"]:
        for keyvalue in instance["Tags"]:
            if keyvalue["Key"] == "Name":
                print("%s \t-\t %s" % (instance['PrivateIpAddress'], keyvalue["Value"]))