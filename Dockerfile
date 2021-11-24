FROM python:3.8
COPY ./sourdough /opt/sourdough
COPY ./setup.py /tmp/setup.py
RUN python /tmp/setup.py install
RUN rm /tmp/setup.py


