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
    /bin/sh -c "pip install timm && lmdeploy serve api_server OpenGVLab/InternVL2_5-4B-MPO --tool-call-parser internlm"
```

# API

启动后查看：

http://0.0.0.0:23333/

# 层次结构

InternVL-2.5

lmdeploy

OpenAI http

tools
