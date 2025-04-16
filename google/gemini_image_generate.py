from pybase16384.backends.cffi.build import system

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import time
import os
import sys

import base64
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# from pythonX import ensure_directory
# Gemini 2.0 Flash Experimental supports the ability to output text and inline images.
# This lets you use Gemini to conversationally edit images or generate outputs with interwoven text (for example, generating a blog post with text and images in a single turn).
# All generated images include a SynthID watermark, and images in Google AI Studio include a visible watermark as well.
# Gemini 2.0 Flash Experimental支持输出文本和内联图像。这使您可以使用Gemini进行对话式编辑图像或生成交织文本的输出（例如，
# 在一个回合中生成包含文本和图像的博客文章）。所有生成的图像都包含SynthID水印，Google AI Studio中的图像也包含可见水印。


client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

contents = ('Generate a giant iPhone')

response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=contents,
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO((part.inline_data.data)))

        current_dir = os.getcwd()
        timestamp = int(time.time())
        filename = f"gemini-image_{timestamp}.png"
        path_final = Path(current_dir) / 'image' / filename
        # print(pythonX.ensure_directory(path_final))

        print(path_final)
        image.save(path_final)
        image.show()
