# PRfire项目--大模型农业分析

# 环境

windows11

https://github.com/deepspeedai/DeepSpeed/issues/6865

限制python版本到3.11

```
conda create -n prfire python=3.11
conda activate prfire
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
pip install -r .\requirements.txt -v
```

# 使用方法

```
uvicorn main:app --reload
```

# API

交互式API文档，启动后查看

http://127.0.0.1:8000/docs

# 代码结构

思维链

队列系统

推理缓存

数据库

UUID访问
