FROM resin/raspberry-pi-python:latest
# Enable systemd
ENV INITSYSTEM on
ADD . /xbox
WORKDIR /xbox
RUN pip install -r requirements.txt
