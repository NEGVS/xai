import time
import os
import sys

import base64
from pathlib import Path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pythonX

file_path = "/app/ai/google/image22/gemini-image_1744789391.png"

print(pythonX.ensure_directory(file_path))

