#!/usr/bin/env python2
# coding: utf-8

import os
import sys
import argparse


def build(args):
    """ Build docker image """
    directory = args.directory
    dist, version = directory.split('-')
    os.system('docker build -t erlang-{}:{} -f {}/Dockerfile .'.format(
        dist, version, directory))


def run(args):
    """ Run a container """
    git_tag = os.getenv('GIT_TAG', args.tag)
    domain = os.getenv('QINIU_DOMAIN', args.domain)
    bucket = os.getenv('QINIU_BUCKET', args.bucket)
    access_key = os.getenv('QINIU_AK', args.access_key)
    secret_key = os.getenv('QINIU_SK', args.secret_key)
    if not domain or not bucket or not access_key or not secret_key:
        print u'[ERROR]: Qiniu settings missing: domain={}, bucket={}, access_key={}, secret_key={}'.format(
            domain, bucket, access_key, secret_key)
        exit(-1)
    volumes = ' '.join([u'-v {}'.format(v) for v in args.volumes]) \
              if args.volumes else ''
    rm = '' if args.no_rm else '--rm'
    image = args.image
    cmd = ('docker run '
           '-e GIT_TAG={git_tag} '
           '-e QINIU_DOMAIN={domain} '
           '-e QINIU_BUCKET={bucket} '
           '-e QINIU_AK={access_key} '
           '-e QINIU_SK={secret_key} '
           '{volumes} {rm} -i -t {image}').format(**locals())
    print '[CMD]: {}'.format(cmd)
    os.system(cmd)


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # Build
    build_parser = subparsers.add_parser('build', help=build.__doc__)
    build_parser.set_defaults(func=build)
    build_parser.add_argument('directory', help='Target directory')
    # Run
    run_parser = subparsers.add_parser('run', help=run.__doc__)
    run_parser.set_defaults(func=run)
    run_parser.add_argument('-i', '--image', required=True, help='Docker image')
    run_parser.add_argument('--no-rm', action='store_true', help='Docker auto remove container when exit')
    run_parser.add_argument('-v', '--volumes', nargs='*', help='Docker volumnes(DIR:DIR)')
    run_parser.add_argument('-t', '--tag', help='Git tag')
    run_parser.add_argument('-d', '--domain', help='Qiniu bucket domain')
    run_parser.add_argument('-b', '--bucket', help='Qiniu bucket name')
    run_parser.add_argument('-a', '--access-key', help='Qiniu access key')
    run_parser.add_argument('-s', '--secret-key', help='Qiniu secret key')

    args = parser.parse_args()
    print u'Args: {}'.format(args)
    return args


def main():
    args = parse_args()
    args.func(args)
    print 'DONE'


if __name__ == '__main__':
    main()

