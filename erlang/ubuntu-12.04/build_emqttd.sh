#!/bin/bash

if [ -d "emqttd-relx" ]; then
    cd emqttd-relx
    if [ -d ".git" ]; then
        git pull
    else
        git clone --depth 2 https://github.com/emqtt/emqttd-relx.git .
    fi
else
    git clone --depth 2 https://github.com/emqtt/emqttd-relx.git
    cd emqttd-relx
fi
make clean
rm -rf _rel
make
make rel
python2 /mnt/release.py
