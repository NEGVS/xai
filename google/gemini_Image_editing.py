from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import time
import os
import sys
from pathlib import Path

import PIL.Image
# Image editing with Gemini
# To perform image editing, add an image as input. The following example demonstrats uploading base64 encoded images. For multiple images and larger payloads, check the image input section.
# 使用Gemini进行图像编辑
# 要执行图像编辑，请添加图像作为输入。以下示例演示了如何上传base64编码的图像。对于多个图像和更大的有效载荷，请检查图像输入部分。

# Limitations
# For best performance, use the following languages: EN, es-MX, ja-JP, zh-CN, hi-IN.
# Image generation does not support audio or video inputs.
# Image generation may not always trigger:
# The model may output text only. Try asking for image outputs explicitly (e.g. "generate an image", "provide images as you go along", "update the image").
# The model may stop generating partway through. Try again or try a different prompt.
# When generating text for an image, Gemini works best if you first generate the text and then ask for an image with the text.
# 局限性
# 为了获得最佳性能，请使用以下语言：EN、es-MX、ja-JP、zh-CN、hi-IN。
# 图像生成不支持音频或视频输入。
# 图像生成可能并不总是触发：
# 模型可能只输出文本。尝试明确地要求图像输出（例如“生成图像”、“边走边提供图像”和“更新图像”）。
# 模型可能会在中途停止生成。请重试或尝试其他提示。
# 在为图像生成文本时，如果你先生成文本，然后要求一个包含文本的图像，Gemini的效果最好。
image = PIL.Image.open('/Users/andy_mac/PycharmProjects/xai/static/IMG_5314.JPG')

client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

text_input = ('Hi, This is a picture of me.'
            'Can you add a llama next to me?',)

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=[text_input, image],
    config=types.GenerateContentConfig(
      response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO(part.inline_data.data))
    # 保存图片
    current_dir = os.getcwd()
    timestamp = int(time.time())
    filename = f"gemini-image_editing_{timestamp}.png"
    path_final = Path(current_dir) / 'image_editing' / filename
    # print(pythonX.ensure_directory(path_final))

    print(path_final)
    image.save(path_final)
    # 显示图片
    image.show()