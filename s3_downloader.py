# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import logging

import boto3

import requests
from cerberus import Validator

session = boto3.Session()
s3_resource = session.resource('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def remote_to_s3(method, url, bucket, s3_key, headers=None):
    jinn_data = s3_resource.Bucket(bucket)
    try:
        # We do it like this to use s3:ListBucket instead of s3:GetObject permissions in IAM
        log_s3_object = [o for o in jinn_data.objects.filter(Prefix=s3_key) if o.key == s3_key][0]
        logger.error('File %s exists in S3, size %s, skipping', s3_key, log_s3_object.size)
        return
    except Exception as e:
        pass
    logger.info('Starting %s download to %s:%s', url, bucket, s3_key)
    log_s3_object = jinn_data.Object(key=s3_key)
    res = requests.request(method=method, url=url, headers=headers, stream=True)
    log_s3_object.upload_fileobj(res.raw)
    logger.info('Transfer completed')


S3_DOWNLOADER_SCHEMA = {
    'source': {
        'type': 'dict',
        'schema': {
            'url': {
                'type': 'string',
                'required': True,
            },
            'method': {
                'type': 'string',
                'default': 'GET',
            },
            'headers': {
                'type': 'dict',
                'default': None,
                'nullable': True,
            },
        },
    },
    'destiny': {
        'type': 'dict',
        'schema': {
            'bucket': {
                'type': 'string',
                'required': True,
            },
            'key': {
                'type': 'string',
                'required': True,
            },
        },
    },
}


def lambda_entrypoint(event, context):
    validator = Validator(schema=S3_DOWNLOADER_SCHEMA)
    if not validator.validate(event):
        logger.error("Event uncorrect format %s", validator.errors)
        return
    data = validator.document
    method, url, headers = data['source']['method'], data['source']['url'], data['source']['headers']
    bucket, s3_key = data['destiny']['bucket'], data['destiny']['key']
    remote_to_s3(method=method, url=url, headers=headers, bucket=bucket, s3_key=s3_key)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('botocore').setLevel(logging.WARN)
    logging.getLogger('boto3').setLevel(logging.WARN)
    logging.getLogger('s3transfer').setLevel(logging.WARN)
    logging.getLogger('requests').setLevel(logging.WARN)
    remote_to_s3('GET', 'https://google.com/', bucket='test', s3_key='test.gz')
