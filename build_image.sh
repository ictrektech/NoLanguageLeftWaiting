docker build \
  --build-arg PROXY=http://192.168.1.xxx:xxx \
  --build-arg CUDA_ARCHS=87 \
  -t nllw:torch2.8 \
  -f Dockerfile_2.8 \
  .
