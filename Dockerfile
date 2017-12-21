FROM gcr.io/tensorflow/tensorflow

COPY . /

WORKDIR ../

RUN apt-get update && apt-get install -y git ffmpeg python-dev curl python3-pip cmake \
    pkg-config \
    python-opencv \
    libopencv-dev \
    libav-tools  \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libjasper-dev \
    python-numpy \
    cython3 \
    python-pycurl \
    python-opencv && \
    cp manifest.json /var/manifest.json && \
    pip3 install --upgrade pip && \
	pip3 install virtualenv && \
	pip3 install -r requirements.txt && \
	make check && \
	git clone https://github.com/thtrieu/darkflow.git && \
	cd ./darkflow && \
	python3 setup.py build_ext --inplace && \
	pip3 install .

COPY ./deploy/yolo.weights ./darkflow/yolo.weights

ENTRYPOINT ["make", "run"]


