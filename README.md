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
mkdir -p ~/workspace-docker/nllw/cache/huggingface/
```
```
docker rm -f nllw
```
```
docker run --restart unless-stopped -d \
  --name nllw \
  --runtime nvidia \
  --gpus all \
  -p 8097:8097 \
  -v ~/workspace-docker/nllw/cache/huggingface/:/root/.cache/huggingface/hub\
  nllw:v1
```

## nllw demo (package使用方式参考)
```bash
python demo.py
```

## websocket 使用方式参考
```bash
# 服务端
python stream_websocket.py

# 客户端测试
python test_stream.py
```