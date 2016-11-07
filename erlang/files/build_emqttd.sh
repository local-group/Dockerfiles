#!/bin/bash

set -x
cd /mnt
git clone --branch ${GIT_TAG} --depth 1 https://github.com/thewawar/emqttd-relx.git
cd emqttd-relx
git describe --abbrev=0 --tags
make
make rel
python2 /mnt/release.py
