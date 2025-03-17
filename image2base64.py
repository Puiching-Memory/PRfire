import base64
import sys
import mimetypes

def image_to_base64(file_path):
    try:
        # 读取二进制文件
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
        # 获取 MIME 类型（如 image/jpeg、image/png）
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"  # 默认类型
        
        # 组合为完整的 Data URL 格式
        return f"data:{mime_type};base64,{encoded_string}"
    
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python image_to_base64.py <image_path>")
    #     sys.exit(1)
    
    # file_path = sys.argv[1]
    result = image_to_base64(r"media\IMG1808_9118.JPG")
    print(result)

    # with open("base64.txt", "w") as f:
    #     f.write(result)