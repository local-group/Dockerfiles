#!/usr/bin/env python2
# coding: utf-8

import sys
import json
import logging
from argparse import Namespace
from collections import OrderedDict

import redis
from qiniu import Auth, BucketManager

import quip
from ci_settings import QINIU_DOMAIN, QINIU_BUCKET, QINIU_AK, QINIU_SK, \
    QUIP_ACCESS_TOKEN, QUIP_DOC_ID, \
    TASK_QUEUE, TARGET_IMAGES
import docker_cli


def get_stdout_logger(name, fd=sys.stdout, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers = []

    ch = logging.StreamHandler(fd)
    ch.setLevel(level)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = get_stdout_logger('ci_processor')
redis_cli = redis.StrictRedis()


def make_cdn_link(filename):
    return 'http://{}/{}'.format(QINIU_DOMAIN, filename)


def git_push(payload):
    pass


def git_tag(payload):
    args = Namespace()
    args.volumes = []
    args.no_rm = False
    args.tag = payload.get('ref')
    args.domain = QINIU_DOMAIN
    args.bucket = QINIU_BUCKET
    args.access_key = QINIU_AK
    args.secret_key = QINIU_SK

    if not args.domain or not args.bucket or \
       not args.access_key or not args.secret_key:
        raise ValueError(
            (u'[ERROR]: Qiniu settings missing: '
             u'domain={}, bucket={}, access_key={}, secret_key={}').format(
                 args.domain, args.bucket, args.access_key, args.secret_key))

    zip_files = OrderedDict()
    for image in TARGET_IMAGES:
        zip_files[image] = None
        os_release = image.split('-')[-1]
        os_id, os_version = os_release.split(':')
        directory = '-'.join([os_id, os_version])
        args.image = image
        try:
            docker_cli.build(Namespace(directory=directory))
            logger.info(u'RUN {}'.format(args))
            docker_cli.run(args)
            logger.info(u'[build DONE]: image={}, tag={}'.format(
                args.image, args.tag))
            zip_files[image] = 'emqttd-{os_id}{os_version}-{version}.zip'.format(
                version=args.tag, os_id=os_id, os_version=os_version)
        except Exception as e:
            logger.error('[build FAIL]: image={}, tag={}, e={}'.format(
                args.image, args.tag, e))

    qiniu_cli = Auth(args.access_key, args.secret_key)
    bucket_mgr = BucketManager(qiniu_cli)
    quip_cli = quip.QuipClient(QUIP_ACCESS_TOKEN)
    files = []
    for image, zip_file in zip_files.iteritems():
        if not zip_file:
            files.append(u'* `FAIL`: image={}'.format(image))
        else:
            ret, _ = bucket_mgr.stat(args.bucket, zip_file)
            if 'hash' in ret:
                files.append(u'* `SUCCESS`: [{}]({})'.format(
                    zip_file, make_cdn_link(zip_file)))
            else:
                files.append(
                    u'* `FAIL`: build or upload failed: image={}, filename={}'.format(
                        image, zip_file))
    doc = (
        u'## Build emqttd-relx@{tag}\n'
        u'{files}'
    ).format(tag=args.tag, files='\n'.join(files))
    quip_cli.edit_document(QUIP_DOC_ID, doc, format='markdown')
    logger.info('[Sync to quip]: doc={}'.format(doc))


def main():
    logger.info('CI processor Started!')
    while True:
        try:
            _, raw_payload = redis_cli.brpop(TASK_QUEUE)
            payload = json.loads(raw_payload)
            request_id = payload['request_id']
            logger.info('[Got task]: {}'.format(request_id))
            logger.debug('[payload]: {}'.format(payload))
            if payload.get('ref_type') == 'tag':
                git_tag(payload)
        except Exception as e:
            logger.error(u'[{}][Process Error]: {}'.format(request_id, e))


if __name__ == '__main__':
    main()
