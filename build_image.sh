#!/bin/bash
CUDA_ARCHS="$(
  MODEL="$(tr -d '\0' </proc/device-tree/model 2>/dev/null || true)"
  case "$MODEL" in
    *Nano*|*TX1*)                 echo 53 ;;
    *TX2*)                       echo 62 ;;
    *Xavier*NX*|*AGX*Xavier*)    echo 72 ;;
    *Orin*|*THOR*|*Thor*)        echo 87 ;;
    *)
      echo "ERROR: Unknown Jetson model: $MODEL" >&2
      exit 1
      ;;
  esac
)" && \
docker build \
  --build-arg PROXY=http://192.168.1.xxx:xxx \
  --build-arg CUDA_ARCHS="$CUDA_ARCHS" \
  -t nllw:torch2.8 \
  -f Dockerfile_2.8 \
  .
