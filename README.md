# PRfire项目--大模型农业分析

# 环境

windows11

https://github.com/deepspeedai/DeepSpeed/issues/6865 限制python版本到3.11

使用conda进行环境管理

```
conda create -n prfire python=3.11
conda activate prfire
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install -r .\requirements.txt -v
```

# 使用方法

1. 启动服务后端

```
uvicorn main:app --reload
```

2. 启动推理后端

```
lmdeploy serve api_server model\InternVL2_5-4B-MPO --server-port 23333 --server-name 127.0.0.1
```

*4B大概需要16GB显存 See：[https://lmdeploy.readthedocs.io/en/latest/get_started/get_started.html](https://lmdeploy.readthedocs.io/en/latest/get_started/get_started.html)

# API

交互式API文档，启动后查看

http://127.0.0.1:8000/docs

# 功能概述

思维链

队列系统

推理缓存

数据库

UUID标识符（任务id/历史id）

# NOTE

db存储历史记录，langchhainEngine载入历史记录时需要将其转换为langchain专用格式，node使用时需要再转换一次格式为OpenAI格式

# TODO

* [ ] 流式传输
* [X] 多轮对话
* [ ] 本地农业数据检索
* [ ] 工具类调用
