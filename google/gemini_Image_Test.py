from PIL import Image
from google import genai
# 多模态输入
# Gemini API 支持多模态输入，可让您将文本与媒体文件组合使用。以下示例演示了如何提供图片：
client = genai.Client(api_key="AIzaSyCY0pgtmhJbisYENnNgWzd0m_u5vKdiB8U")

image = Image.open("/Users/andy_mac/PycharmProjects/xai/static/9.jpg")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[image, "Tell me about this photo"]
)
print(response.text)



# Here's a description of the photo:
#
# **Overall Impression:**
#
# The photo is a close-up studio portrait of a young Asian woman with beautiful, clear skin. The image has a clean, minimalist aesthetic, typical of beauty or fashion photography.
#
# **Details:**
#
# *   **Model:** The woman has dark hair and light skin. Her features are delicate and conventionally attractive.
# *   **Hair:** Her hair is long, straight, dark, and glossy. A few strands fall across her face.
# *   **Makeup:** She wears natural-looking makeup that emphasizes her features, with glossy lips.
# *   **Jewelry:** She has a small, delicate earring.
# *   **Lighting:** The lighting is soft and even, creating a smooth and flawless appearance.
# *   **Background:** The background is a neutral light gray/white color, which helps to keep the focus on the model and avoids distractions.
#
# **Style and Purpose:**
#
# *   The image has a modern and sophisticated feel.
# *   The focus is on the model's beauty and the quality of her skin.
#
# In summary, it's a well-executed beauty portrait with a focus on natural beauty and flawless skin.
#