#!/usr/bin/env bash
set -euo pipefail

MODEL="$(tr -d '\0' </proc/device-tree/model 2>/dev/null || true)"

case "$MODEL" in
  *Nano*|*TX1*)                 CUDA_ARCHS=5.3 ;;
  *TX2*)                       CUDA_ARCHS=6.2 ;;
  *Xavier*NX*|*AGX*Xavier*)    CUDA_ARCHS=7.2 ;;
  *Orin*|*THOR*|*Thor*)        CUDA_ARCHS=8.7 ;;
  *)
    echo "ERROR: Unknown Jetson model: $MODEL" >&2
    exit 1
    ;;
esac

echo "[build] Detected Jetson model: $MODEL"
echo "[build] Using CUDA_ARCHS=${CUDA_ARCHS}"

docker build \
  --build-arg PROXY=http://192.168.1.xxx:xxx \
  --build-arg CUDA_ARCHS="${CUDA_ARCHS}" \
  -t nllw:torch2.8 \
  -f Dockerfile_2.8 \
  .
