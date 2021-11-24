FROM python:3.8
COPY ./sourdough /opt/sourdough
COPY ./setup.py /opt/setup.py
WORKDIR /opt
RUN python ./setup.py develop
