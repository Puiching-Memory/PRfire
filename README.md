# PRfire项目--大模型农业分析

本地LLM：Ovis-4B/Ovis-2B

# 环境

宿主系统：windows11

为私有化部署，使用Docker进行环境管理

# 从头安装

```powershell
docker pull pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel
docker run -d  --privileged=true -p 5595:5595 -p 7897:7897 --name PRfire --shm-size 200G --ulimit memlock=-1 --gpus=all -it pytorch/pytorch:2.4.0-cuda12.4-cudnn9-devel /bin/bash
docker attach PRfire

apt update
apt upgrade
apt install git

git clone https://github.com/Puiching-Memory/PRfire.git
cd PRfire
git submodule init
git submodule update

mkdir model
export HF_ENDPOINT=https://hf-mirror.com
pip install huggingface_hub
huggingface-cli download --resume-download AIDC-AI/Ovis2-4B --local-dir ./model/

cd Ovis
pip install -r requirements.txt
pip install -e . -v
pip install flash-attn==2.7.0.post2 --no-build-isolation -v

export GRADIO_SERVER_NAME=0.0.0.0
python ovis/serve/server.py --model_path /workspace/PRfire/model/ --port 5595
```

# 使用方法

1. 载入Docker镜像tar包

   ```
   docker run -d  --privileged=true -p 5595:5595 -p 7897:7897 --name PRfire --shm-size 200G --ulimit memlock=-1 --gpus=all -it PRfire-Ovis:latest /bin/bash
   ```
2. 启动Ovis+gradio

   ```
   cd /workspace/PRfire/Ovis/
   python ovis/serve/server.py --model_path /workspace/PRfire/model/ --port 5595
   ```


# API

本地浏览器访问：http://0.0.0.0:5595

### python

见ovis_run.py

### Javascript

```
npm i -D @gradio/client
```

```
import { Client } from "@gradio/client";

const response_0 = await fetch("https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png");
const exampleImage = await response_0.blob();
			
const response_1 = await fetch("undefined");
const exampleVideo = await response_1.blob();
			
const client = await Client.connect("http://0.0.0.0:5595/");
const result = await client.predict("/predict", { 
		type: "Image", 
				image: exampleImage, 
				video: exampleVideo, 
		text: "Hello!!", 
});

console.log(result.data);
```

| 参数项 | 类型             | 选项 | 注释                         |
| ------ | ---------------- | ---- | ---------------------------- |
| type   | string           | 必填 | “Image”,"Vedio","TextOnly" |
| image  | Blob/File/Buffer | 必填 | 可选项：null                 |
| video  | any              | 必填 | 可选项：null                 |
| text   | string           | 必填 |                              |

# TODO
