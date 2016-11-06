FROM centos:7

RUN yum update -y
RUN yum install -y wget git zip
RUN yum groupinstall -y "Development Tools"
RUN wget https://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm -P /tmp
RUN rpm -Uvh /tmp/erlang-solutions-1.0-1.noarch.rpm
RUN wget https://packages.erlang-solutions.com/erlang/esl-erlang/FLAVOUR_1_general/esl-erlang_18.3-1~centos~7_amd64.rpm -O /tmp/erlang.rpm
RUN yum localinstall -y /tmp/erlang.rpm
RUN wget https://bootstrap.pypa.io/get-pip.py -O /tmp/get-pip.py
RUN python /tmp/get-pip.py
RUN pip install qiniu

ADD ./files/build_emqttd.sh /mnt
ADD ./files/release.py /mnt

# cleanup
RUN yum clean packages \
 && rm -rf /tmp/* /var/tmp/*

VOLUME /mnt/emqttd-relx

CMD ["/bin/bash", "/mnt/build_emqttd.sh"]
