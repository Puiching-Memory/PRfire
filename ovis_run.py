from gradio_client import Client, handle_file

client = Client("http://0.0.0.0:5595/")
result = client.predict(
		type="Image", # Literal['Image', 'Video', 'TextOnly']

        # Dict(path: str | None (Path to a local file),
        # url: str | None (Publicly available url or base64 encoded image),
        # size: int | None (Size of image in bytes), orig_name: str | None (Original filename),
        # mime_type: str | None (mime type of image),
        # is_stream: bool (Can always be set to False), meta: Dict())        
		image=handle_file(r"media\IMG1808_9118.JPG"),

        # Dict(video: filepath, subtitles: filepath | None)
		# video={"video":handle_file('https://github.com/gradio-app/gradio/raw/main/demo/video_component/files/world.mp4')},
        video=None,

        # str
		text="我的上一句话是？",
		api_name="/predict"
)
print(result)