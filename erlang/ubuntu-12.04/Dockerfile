FROM ubuntu:12.04

ADD sources.list /etc/apt/
RUN apt-get update
RUN apt-get install -y wget git zip python-pip build-essential
ADD zip /mnt
RUN dpkg -i /mnt/esl-erlang_18.3-1-ubuntu-precise_amd64.deb || true
RUN apt-get -f install -y
RUN pip install qiniu -i http://pypi.douban.com/simple/

ADD build_emqttd.sh /
ADD release.py /

# cleanup
RUN rm /mnt/*.deb
RUN apt-get clean\
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

VOLUME /emqttd_relx/deps

CMD ["/bin/bash", "/build_emqttd.sh"]
