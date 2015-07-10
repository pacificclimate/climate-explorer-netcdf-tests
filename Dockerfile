FROM pcic/geospatial-python

RUN apt-get update
RUN apt-get -yq install \
  libzmq3 \
  libzmq3-dev \
  python3-zmq \
  libfreetype6-dev

ADD . /app
WORKDIR /app/notebooks
RUN pip3 install -r /app/requirements.txt

EXPOSE 8888

CMD ipython3 notebook --no-browser --port=8888 --ip=* --matplotlib=inline
