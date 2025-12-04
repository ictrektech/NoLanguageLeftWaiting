FROM swr.cn-southwest-2.myhuaweicloud.com/ictrek/pytorch_py312:jet_latest

WORKDIR /opt/ictrek/app/nllw

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

ARG PIP_ARGS="--index-url https://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com --timeout 120 --retries 5 --upgrade-strategy only-if-needed"
ARG PROXY=""

RUN export HTTPS_PROXY="${PROXY}" && \
    git clone --recursive https://github.com/OpenNMT/CTranslate2.git /tmp/CTranslate2 && \
    unset HTTPS_PROXY

RUN cd /tmp/CTranslate2 && \
    mkdir build && cd build && \
    cmake .. -DWITH_CUDA=ON -DWITH_MKL=OFF -DWITH_CUDNN=ON -DOPENMP_RUNTIME=COMP -DCMAKE_BUILD_TYPE=Release && \
    make -j 4 && make install

RUN cd /tmp/CTranslate2/python && \
    pip3 install -r install_requirements.txt ${PIP_ARGS} && \
    python3 setup.py bdist_wheel && \
    python3 -m pip install --force-reinstall dist/*.whl ${PIP_ARGS}

RUN pip3 install transformers websockets ${PIP_ARGS}

# RUN mkdir -p /root/.cache/huggingface/
# COPY ./hub /root/.cache/huggingface/hub

RUN mkdir -p /opt/ictrek/app/nllw/
COPY ./nllw /opt/ictrek/app/nllw/nllw
COPY ./stream_websocket.py /opt/ictrek/app/nllw/stream_websocket.py
COPY ./test_stream.py /opt/ictrek/app/nllw/test_stream.py

# OFFLINE=1 python stream_websocket.py
ENV OFFLINE=1
CMD ["python", "./stream_websocket.py"]