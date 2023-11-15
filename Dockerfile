FROM python:3.7-slim

# set environment vars
ENV PYTHONPATH="app:${PYTHONPATH}"
ENV SUPERVISOR_APP_STOPWAITSECS=20

# install dependencies
RUN apt-get update && apt-get install -y \
apt-utils \
nginx \
git \
python3-pip \
&& rm -rf /var/lib/apt/lists/*

RUN echo "America/New_York" > /etc/timezone; dpkg-reconfigure -f noninteractive tzdata

# update working directories
ADD ./app /app
ADD ./config /config

# install dependencies
RUN pip install --upgrade pip
RUN pip3 install -r /config/requirements.txt

# setup config
COPY ./config/nginx.conf /etc/nginx/nginx.conf
COPY ./config/server.conf /etc/nginx/conf.d/server.conf
COPY ./config/supervisor.conf /etc/supervisord.conf

EXPOSE 80
CMD ["supervisord", "--nodaemon", "--configuration", "/etc/supervisord.conf"]
# CMD ["python", "/app/app.py"]


