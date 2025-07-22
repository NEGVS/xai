import ssl
import httpx
from contextlib import contextmanager


response = httpx.get("https://www.baidu.com")
# print(response.text)
print(response.status_code)
# LibreSSL 2.8.3
