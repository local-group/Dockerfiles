#!/usr/bin/env python2
# coding: utf-8

import sys
import json
import logging
from argparse import Namespace

import redis

from ci_settings import TASK_QUEUE, QINIU_BUCKET, QINIU_AK, QINIU_SK, TARGET_IMAGES


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


def git_push(payload):
    pass


def git_tag(payload):
    args = Namespace()
    args.tag = payload.get('ref')
    args.bucket = QINIU_BUCKET
    args.access_key = QINIU_AK
    args.secret_key = QINIU_SK
    for image in TARGET_IMAGES:
        args.image = image
        logger.info(u'RUN {}'.format(args))
        # docker_cli.run(args)


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
