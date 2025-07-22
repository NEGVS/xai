import time
import os
api_key = os.getenv("GEMINI_API_KEY")
print(api_key)

api_key2 = os.getenv("GOOGLE_API_KEY")
print(api_key2)
timestamp = str(int(time.time()))
print(timestamp)
path = './static/image/gemini-image' + timestamp + '.png'
print(path)
