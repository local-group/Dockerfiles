FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y wget git zip python-pip build-essential
RUN wget https://packages.erlang-solutions.com/erlang/esl-erlang/FLAVOUR_1_general/esl-erlang_18.3-1~ubuntu~precise_amd64.deb -O /tmp/erlang.deb
RUN dpkg -i /tmp/erlang.deb || true
RUN apt-get -f install -y
RUN pip install qiniu

# cleanup
RUN apt-get clean\
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ADD ./files/build_emqttd.sh /mnt
ADD ./files/release.py /mnt

VOLUME /mnt/emqttd-relx

CMD ["/bin/bash", "/mnt/build_emqttd.sh"]
