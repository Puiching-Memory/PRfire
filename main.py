from fastapi import FastAPI, File, UploadFile
# import onnxruntime as ort
import numpy as np
from pydantic import BaseModel
import PIL.Image as Image
from io import BytesIO
import numpy as np
import os
from ultralytics import YOLO

app = FastAPI(title="YOLO 农业分类模型 API 🚀")

# print(ort.get_available_providers())

# cuda_path = os.path.join(os.environ["CUDA_PATH"], "bin")
# ort.preload_dlls(cuda=True, cudnn=False, directory=cuda_path)

# 加载 ONNX 模型
# ort_session = ort.InferenceSession(
#     r"./model/model.onnx", providers=ort.get_available_providers()
# )

model = YOLO(r"./model/YOLO11s_cls_1/weights/best.pt")
model.eval()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # 读取上传的图像文件
    contents = await file.read()
    img = Image.open(BytesIO(contents))
    #img = img.resize((640,640)).convert("RGB")

    # # 预处理（调用上述的preprocess_image函数）
    # img = np.array(img)
    # img = img.transpose(2, 0, 1)
    # img = img[np.newaxis, ...]
    # print(img.shape)

    results = model(img)
    result = results[0]
    probs = result.probs
    # print(result.names)

    # # 获取模型输入名称
    # input_name = ort_session.get_inputs()[0].name

    # # 运行推理
    # outputs = ort_session.run(None, {input_name: img})
    # outputs = outputs[0][0]
    # print(outputs)

    # top5_indices = np.argsort(outputs)[::-1][:5]
    # top5_scores = outputs[top5_indices]
    # print(ort_session.get_modelmeta())

    print({"result":probs.top5,"conf":probs.top5conf})

    re_name = []
    for i in probs.top5:
        re_name.append(result.names[i])


    return {"result":re_name,"conf":probs.top5conf.cpu().numpy().tolist()}
