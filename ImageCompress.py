from PIL import Image

# 打开一个jpg图像文件，注意是当前路径:
im = Image.open('test.jpg')
# im=im.convert('P')
im.save("test1.jpg",quality=90)