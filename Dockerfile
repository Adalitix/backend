FROM python:3.6.5

# Force stdin, stdout and stderr to be totally unbuffered.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y sudo python3-gdal postgresql

RUN useradd -m -s /bin/bash devel \
    && usermod -aG sudo devel \
    && echo 'devel ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER devel
RUN mkdir /home/devel/adalitix
WORKDIR /home/devel/adalitix

# Install dependencies before importing the project
ARG ENVIRONMENT=prod

# install gsconfig from source
RUN git clone http://github.com/dwins/gsconfig.py.git/
RUN cd gsconfig.py && sudo python setup.py install

COPY requirements.txt /home/devel/adalitix/config/requirements.txt
COPY requirements-${ENVIRONMENT}.txt /home/devel/adalitix/config/requirements-${ENVIRONMENT}.txt
RUN sudo pip install -r config/requirements-${ENVIRONMENT}.txt

# Layers for the django app
# add whole project dir to image
ADD . /home/devel/adalitix/backend/
RUN sudo chown -R devel:devel /home/devel/adalitix

WORKDIR /home/devel/adalitix/backend
