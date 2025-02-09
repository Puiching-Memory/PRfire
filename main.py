from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from pathlib import Path
import shutil
from contextlib import asynccontextmanager
import numpy as np
from PIL import Image
import io
import uuid
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from pickledb import PickleDB

QUEUE_MAX_SIZE = 10
task_queue = asyncio.Queue(QUEUE_MAX_SIZE)


async def process(image: Image, description: str, task_id: str):
    """
    这里可以放置你的图像处理逻辑。
    比如保存文件、分析图像、生成报告等。
    """
    print(f"Processing image {image} with description: {description}")
    print(f"Finished processing image {image}")
    db.set(task_id, "Finished")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def worker():
        while True:
            image_array, description, task_id = await task_queue.get()
            await process(image_array, description, task_id)
            task_queue.task_done()

    asyncio.create_task(worker())

    global db
    db = PickleDB("./tasks.db")

    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")
    yield

    # do cleanup here
    # db.save()


app = FastAPI(lifespan=lifespan)


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), description: str = Form(...)):
    """
    接受上传的图片和聊天文本，并将其放入队列中等待处理
    ---

    Returns:
        dict: 包含以下键值对的字典
            - message (str): 上传成功的提示信息。
            - image_size (list): 上传的图片的尺寸。
            - description_length (int): 聊天文本的长度。
            - task_id (str): 任务的唯一ID。
    """
    if task_queue.full():
        raise HTTPException(status_code=429, detail="队列已满，请稍后再试")

    # 将上传的图片转为PIL图像
    image_array = np.array(bytearray(await file.read()), dtype=np.uint8)
    image_array = Image.open(io.BytesIO(image_array))

    # 生成唯一ID
    task_id = uuid.uuid4()

    # 将任务加入队列
    await task_queue.put((image_array, description, task_id))

    return {
        "message": "数据上传成功，已加入队列等待处理",
        "image_size": image_array.size,
        "description_length": len(description),
        "task_id": task_id,
    }


@app.get("/queue/")
@cache(expire=60)
async def get_queue_state():
    """获取队列状态
    ---
    返回一个字典，包含队列的大小、是否为空、是否已满

    Returns:
        dict: 包含以下键值对的字典
            - queue_size (int): 当前队列的大小。
            - queue_max_size (int): 队列的最大容量。
            - queue_empty (bool): 队列是否为空。
            - queue_full (bool): 队列是否已满。
    """
    return {
        "queue_size": task_queue.qsize(),
        "queue_max_size": QUEUE_MAX_SIZE,
        "queue_empty": task_queue.empty(),
        "queue_full": task_queue.full(),
    }


@app.get("/task/{task_id}/")
@cache(expire=60)
async def get_task(task_id: str):
    """依据任务ID获取任务状态
    ---
    返回一个字典，如果在队列中，则返回任务的状态；如果在数据库中，则返回任务的结果。

    Returns:
        dict: 包含以下键值对的字典
            - status (str): 任务的状态。
            - result (str): 任务的结果。
    """
    # 先尝试从数据库中获取结果
    result = db.get(task_id)
    if result is not None:
        return {"status": "completed", "result": result}

    # 如果任务还在队列中
    for index, (image, description, task_id_q) in enumerate(task_queue._queue):
        if task_id_q == task_id:
            return {"status": "processing", "index": index}

    # 如果任务既不在队列也不在数据库中
    raise HTTPException(status_code=404, detail="任务不存在")
