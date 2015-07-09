FROM ipython/scipystack

RUN apt-get update
RUN apt-get -yq install \
  libzmq3 \
  libzmq3-dev \
  python3-zmq \
  libhdf5-dev \
  libnetcdf-dev \
  libgdal-dev \
  libyaml-dev \
  python3-GDAL

RUN pip3 install scikit-image netCDF4

ADD . /app
WORKDIR /app/notebooks
RUN pip3 install -r /app/requirements.txt

EXPOSE 8888

CMD ipython3 notebook --no-browser --port=8888 --ip=* --matplotlib=inline
