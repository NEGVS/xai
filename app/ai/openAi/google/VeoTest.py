import time
import os
from google import genai
from google.genai import types

# https://ai.google.dev/gemini-api/docs/video#python
# 付费

# 从环境变量获取API key
api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("请设置 GOOGLE_API_KEY 或 GEMINI_API_KEY 环境变量")

client = genai.Client(api_key=api_key)

operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt="A wide-angle photo of a Chinese beauty sleeping soundly in the sunshine",
    # 一只印花猫在阳光下熟睡的广角照片
    config=types.GenerateVideosConfig(
        person_generation="dont_allow",  # "dont_allow" or "allow_adult"--“禁止”或“允许成人”
        aspect_ratio="16:9",  # "16:9" or "9:16"
    ),
)

while not operation.done:
    time.sleep(20)
    operation = client.operations.get(operation)

for n, generated_video in enumerate(operation.response.generated_videos):
    client.files.download(file=generated_video.video)
    generated_video.video.save(f"video{n}.mp4")  # save the video
