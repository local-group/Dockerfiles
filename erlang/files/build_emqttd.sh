#!/bin/bash

cd /mnt
git clone --branch ${GIT_TAG} --depth 1 https://github.com/emqtt/emqttd-relx.git
cd emqttd-relx
make
make rel
python2 /mnt/release.py
