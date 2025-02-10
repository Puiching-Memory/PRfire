from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from typing import Optional
import asyncio
from contextlib import asynccontextmanager
import base64
import sys
import uuid
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from pickledb import PickleDB
from concurrent.futures import ThreadPoolExecutor
import os
from sse_starlette.sse import EventSourceResponse

# from PIL import Image
# import numpy as np
# import time
# import io
# from pathlib import Path
# import shutil
# from fastapi.responses import JSONResponse

sys.path.append("./")

# from internvl_node import chat_with_internvl
from langchainEngine import run_interVL_chain

QUEUE_MAX_SIZE = 10
task_queue = asyncio.Queue(QUEUE_MAX_SIZE)
executor = ThreadPoolExecutor(max_workers=os.cpu_count())


def blocking_process(image: bytes, description: str, task_id: str, session_id: str):
    # time.sleep(20)  # 模拟处理时间

    print(f"Processing image with description: {description}")
    print(f"Task ID: {task_id}")
    history: list = db.get(session_id)

    result = run_interVL_chain(f"data:image/jpeg;base64,{image}",description, history)

    # 保存结果到数据库
    db.set(task_id, result)

    # 更新历史记录
    history.append({"HumanMessage": description, "image_url": image, "AIMessage": result})
    db.set(session_id, history)

    print(f"task {task_id} completed")


async def process(image: bytes, description: str, task_id: str, session_id: str):
    """
    这里可以放置你的图像处理逻辑。
    比如保存文件、分析图像、生成报告等。
    """
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        executor, blocking_process, image, description, task_id, session_id
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    async def worker():
        while True:
            image, description, task_id, session_id = await task_queue.get()
            await process(image, description, task_id, session_id)
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
async def upload(
    file: Optional[UploadFile] = File(None),
    description: str = Form(...),
    session_id: str = Form(...),
):
    """
    接受上传的图片（可选）和聊天文本，并将其放入队列中等待处理。
    ---

    Returns:
        dict: 包含以下键值对的字典
            - message (str): 上传成功的提示信息。
            - image_size (Optional[int]): 如果提供了图片，则返回图片的存储大小(bit)；否则返回 None。
            - description_length (int): 聊天文本的长度。
            - task_id (str): 任务的唯一ID。
            
    FIXME:Send empty value 会导致错误
    """
    if task_queue.full():
        raise HTTPException(status_code=429, detail="队列已满，请稍后再试")
    
    if db.get(session_id) is None:
        raise HTTPException(status_code=404, detail="会话不存在")

    image = None
    image_size = -1

    if file is not None:
        # 将上传的图片转为PIL图像
        # image = np.array(bytearray(await file.read()), dtype=np.uint8)
        # image = Image.open(io.BytesIO(image))

        # 将上传的图片转为base64编码
        image = base64.b64encode(await file.read()).decode()
        image_size = sys.getsizeof(image)

    # 生成唯一ID
    task_id = uuid.uuid4()

    # 将任务加入队列
    await task_queue.put((image, description, task_id, session_id))

    return {
        "message": "数据上传成功，已加入队列等待处理",
        "image_size": image_size,
        "description_length": len(description),
        "task_id": task_id,
    }


@app.get("/new/")
async def create_new_session():
    """创建一个新会话
    ---

    Returns:
        str: 会话的唯一ID。
    """
    session_id = uuid.uuid4()
    db.set(session_id, [])
    return {"session_id": session_id}


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
    返回一个字典,依据任务ID获取任务的状态。

    Returns:
        dict: 包含以下键值对的字典
            - status (str): 任务的状态。
            - result (str): 任务的结果。
    """
    # 从数据库中获取结果
    result = db.get(task_id)
    if result is not None:
        return {"status": "completed", "result": result}

    # 如果任务既不在队列也不在数据库中
    raise HTTPException(status_code=404, detail="查询失败,任务未完成或不存在")


@app.get("/history/{session_id}/")
async def get_history(session_id: str):
    """获取会话的历史记录
    ---
    返回一个字典,包含会话的历史记录。

    Returns:
        dict: 包含以下键值对的字典
            - history (list): 会话的历史记录。
    """
    history = db.get(session_id)
    if history is not None:
        return {"history": history}
