import requests

def remove_bg_api(image_path, output_path, api_key):
    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": open(image_path, "rb")},
        data={"size": "auto"},
        headers={"X-Api-Key": api_key},
    )
    if response.status_code == 200:
        with open(output_path, "wb") as out:
            out.write(response.content)
        print(f"已保存透明背景图片到: {output_path}")
    else:
        print(f"错误: {response.status_code}, {response.text}")

# 需要注册 Remove.bg 获取 API Key
remove_bg_api("input.jpg", "output.png", "your-api-key")