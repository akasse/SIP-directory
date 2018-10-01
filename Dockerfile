FROM python:3.7
LABEL maintainer "Thomas Boutry <thomas.boutry@x3rus.com>"

RUN mkdir -p /usr/local/app/data

ENV SRV_IP 0.0.0.0
ENV SRV_PORT 1234
ENV DATA /usr/local/app/data/regs


COPY ./data/regs /usr/local/app/data
COPY ./server/server.py /usr/local/app/

WORKDIR /usr/local/app/

CMD python /usr/local/app/server.py --data $DATA --ip $SRV_IP --port $SRV_PORT -v

EXPOSE 1234
