FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y wget git build-essential
ADD zip /mnt
RUN dpkg -i /mnt/esl-erlang_18.3-1-ubuntu-precise_amd64.deb || true
RUN apt-get -f install -y
# RUN git clone https://github.com/emqtt/emqttd-relx.git

CMD ["/bin/bash"]
