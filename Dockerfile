FROM python:3.8
COPY ./sourdough /opt/sourdough
COPY ./setup.py /opt/setup.py
WORKDIR /opt
RUN python ./setup.py develop
RUN python ./init_db.py
WORKDIR ./server
ENTRYPOINT python -m flask run --host 0.0.0.0