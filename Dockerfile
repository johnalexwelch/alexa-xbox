From python:3.6
ADD . /xbox
WORKDIR /xbox
RUN pip install -r requirements.txt
