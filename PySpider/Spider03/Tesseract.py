from pytesseract import *
from PIL import Image

# 打开图片
image = Image.open("")

text = image_to_string(image)

print(text)