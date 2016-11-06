FROM centos:6

RUN yum update -y
RUN yum install -y wget git zip python-pip build-essential
RUN wget https://packages.erlang-solutions.com/erlang/esl-erlang/FLAVOUR_1_general/esl-erlang_18.3-1~centos~6_amd64.rpm -O /tmp/erlang.rpm
RUN yum --nogpgcheck localinstall /tmp/erlang.rpm || true
RUN pip install qiniu

ADD ./files/build_emqttd.sh /mnt
ADD ./files/release.py /mnt

# cleanup
RUN yum clean packages \
 && rm -rf /tmp/* /var/tmp/*

VOLUME /mnt/emqttd-relx

CMD ["/bin/bash", "/mnt/build_emqttd.sh"]
