#!/usr/bin/env python
# coding: utf-8

import os
import json
# import argparse
import commands
from qiniu import Auth, put_file


# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-r', '--name', required=False, help='Remote file name(default is local filename)')
#     args = parser.parse_args()
#     print u'Args: {}'.format(args)
#     return args


def upload(local_path, remote_name):
    access_key = os.getenv('QINIU_AK')
    secret_key = os.getenv('QINIU_SK')
    bucket_name = os.getenv('QINIU_BUCKET')
    domain = os.getenv('QINIU_DOMAIN')
    if not access_key or not secret_key or not bucket_name or not domain:
        print u'[Error]: Qiniu config unset: QINIU_AK={}, QINIU_SK={}, QINIU_BUCKET={}, QINIU_DOMAIN={}'.format(
            access_key, secret_key, bucket_name, domain)
        exit(-1)

    client = Auth(access_key, secret_key)
    token = client.upload_token(bucket_name, remote_name, 3600)
    ret, info = put_file(token, remote_name, local_path)
    return ret, info


def get_os_version():
    os_id, os_version = None, None
    with open('/etc/os-release') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            key, value = line.split('=', 1)
            if key == 'ID':
                os_id = json.loads(value) if value.startswith('"') else value
            elif key == 'VERSION_ID':
                os_version = json.loads(value) if value.startswith('"') else value
    return os_id, os_version


def main():
    version = commands.getoutput('git describe --abbrev=0 --tags')
    os_id, os_version = get_os_version()
    pkg = 'emqttd-{os_id}{os_version}-{version}.zip'.format(
        version=version, os_id=os_id, os_version=os_version)
    print u'Target file name: {}'.format(pkg)
    local_path = '/tmp/{}'.format(pkg)
    os.system('cd _rel && zip -rq {} emqttd'.format(local_path))
    ret, info = upload(local_path, pkg)
    print ret


if __name__ == '__main__':
    main()
