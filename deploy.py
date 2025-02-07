from lmdeploy import pipeline, TurbomindEngineConfig
from lmdeploy.vl import load_image
import time

time_start = time.time()

model = "C:\workspace\github\PRfire\InternVL2_5-4B-MPO"
image = load_image("C:\workspace\github\PRfire\IMG1808_9118.JPG")
pipe = pipeline(model, backend_config=TurbomindEngineConfig(session_len=8192))
response = pipe(("诊断该植物健康状况，如果生病请确定他的具体病名。", image))
print(response.text)

print("Time taken:", time.time() - time_start)