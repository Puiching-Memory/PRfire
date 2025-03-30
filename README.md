# PRfire项目--大模型农业分析

本地LLM：IntenVL

# 环境

宿主系统：windows11

为私有化部署，使用Docker进行环境管理

# 拉取镜像

```powershell
docker pull openmmlab/lmdeploy:v0.7.1-cu12
```

# 使用方法

需要hugging face 访问凭证

```
docker run --runtime nvidia --gpus all `
    -v $HOME/.cache/huggingface:/root/.cache/huggingface `
    --env "HUGGING_FACE_HUB_TOKEN=<secret>" `
    -p 23333:23333 `
    --name PRfire `
    --ipc=host `
    openmmlab/lmdeploy:v0.7.1-cu12 `
    /bin/sh -c "pip install timm && pip install flash-attn --no-build-isolation && lmdeploy serve api_server OpenGVLab/InternVL2_5-4B-MPO"
```

# API

启动后查看：

http://0.0.0.0:23333/

# YOLO服务器

### 导出onnx

```
conda create -n prfire python=3.11
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install ultralytics onnx onnxslim
pip install onnxruntime-gpu
python yolo_cls\yolo_onnx.py
```

### 启动YOLO服务器

```
docker run -it --gpus all `
    -p 8000:8000 `
    --name PRfire_yolo `
    pytorch/pytorch:2.1.2-cuda12.1-cudnn8-devel `
    /bin/sh
```

pip install -r .\requirements.txt

apt update && apt install libgl1-mesa-glx libglib2.0-0 -y

uvicorn main:app --host 0.0.0.0 --port 8000

[http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs)

### 直接使用

```
docker run -it --gpus all `
    -p 8000:8000 `
    --name PRfire_yolo `
    prfire_yolo:latest `
    /bin/sh -c "cd PRfire && uvicorn main:app --host 0.0.0.0 --port 8000"
```
