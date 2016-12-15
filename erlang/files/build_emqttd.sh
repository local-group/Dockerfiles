#!/bin/bash

set -x
cd /mnt
git clone --branch ${GIT_TAG} https://github.com/emqtt/emqttd-relx.git
cd emqttd-relx
git describe --abbrev=0 --tags
make
python2 /mnt/release.py
