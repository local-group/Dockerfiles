FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y wget git build-essential
ADD esl-erlang_18.3-1~ubuntu~precise_amd64.deb /mnt
RUN dpkg -i /mnt/esl-erlang_18.3-1~ubuntu~precise_amd64.deb
RUN apt-get -f install
RUN git clone https://github.com/emqtt/emqttd-relx.git

CMD ["/bin/bash"]
