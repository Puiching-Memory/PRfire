# PRfire项目--大模型农业分析

本地LLM：Ovis-4B/Ovis-2B

# 环境

宿主系统：windows11

为私有化部署，使用Docker进行环境管理

```powershell
docker pull pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel
docker run -d  --privileged=true -p 5595:5595 --name PRfire --shm-size 200G --ulimit memlock=-1 --gpus=all -it pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel /bin/bash
docker attach PRfire

apt update
apt upgrade



```

# 使用方法

1. 启动服务后端

```
uvicorn main:app --reload
```

2. 启动推理后端

# API

交互式API文档，启动后查看

http://127.0.0.1:8000/docs

# TODO
