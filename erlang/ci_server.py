#!/usr/bin/env python2
# coding: utf-8

import sys
import json
import hashlib
import hmac
import logging

import redis
from flask import Flask, request, current_app


app = Flask(__name__)
app.config.from_pyfile('ci_settings.py')


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


logger = get_stdout_logger('ci_server')
redis_cli = redis.StrictRedis()


def verify_sign(hub_secret, sign, payload):
    return True
    sign_our = hmac.new(hub_secret, payload, hashlib.sha1).hexdigest()
    return sign == 'sha1={}'.format(sign_our)


@app.route('/git-webhook', methods=['POST'])
def git_webhook():
    # print request.headers, request.args, request.form, request.data
    request_id = request.headers.get('X-GitHub-Delivery')
    logger.info(u'[Hook]: X-GitHub-Delivery={}'.format(request_id))
    sign = request.headers.get('X-Hub-Signature')
    if not verify_sign(current_app.config['HUB_SECRET'], sign, request.data):
        return 'Invalid Signature', 403
    payload = json.loads(request.data)
    payload['request_id'] = request_id
    events = payload.get('hook', {}).get('events', [])
    logger.info(u'[{}][events]: {}'.format(request_id, events))

    redis_cli.lpush(current_app.config['TASK_QUEUE'], json.dumps(payload))
    return 'Got it!'


def main():
    app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)


main()
