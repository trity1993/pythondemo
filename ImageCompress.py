from PIL import Image
import os

# 打开一个jpg图像文件，注意是当前路径:
# im = Image.open('1.jpg')
# im.save("2.jpg",quality=100) # 默认quality=75
print(os.path.getsize('1.jpg')/1024)
