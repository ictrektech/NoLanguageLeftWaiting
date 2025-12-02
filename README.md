<h1 align="center">NoLanguageLeftWaiting</h1>

上游更新在`main`分支，issue修复或新功能会同步到`ictrek-dev`分支

## pip install
```bash
git clone -b ictrek-dev https://github.com/ictrektech/NoLanguageLeftWaiting.git
cd NoLanguageLeftWaiting
pip install -e .
```

## docker build
```bash
docker build \
  --build-arg PROXY=http://192.168.1.n:10808 \
  -t nllw:v1 \
  .
```

## docker run
```bash
docker run --rm -it --gpus all \
  -v $(pwd):/app \
  -v /home/ictrek/.cache/huggingface/hub:/root/.cache/huggingface/hub \
  -w /app \
  nllw:v1 \
  bash
```

## nllw demo (package使用方式参考)
```bash
# 没有 -v 挂载cache 或没有下载模型，用国内代理下载模型
HF_ENDPOINT=https://hf-mirror.com python demo.py

# 有模型cache时可以用离线模式
OFFLINE=1 python demo.py
```

## websocket 使用方式参考
```bash
HF_ENDPOINT=https://hf-mirror.com python stream_websocket.py

# or

OFFLINE=1 python stream_websocket.py
```