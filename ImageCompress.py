from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image
import os

file_old='./img/1.jpg'
file_new='./img/2.jpg'

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        # 输入框创建
        self.numInput = Entry(self)
        self.numInput.pack()

        # 提示框创建
        self.alertButton = Button(self, text='压缩图片', command=self.calculate)
        self.alertButton.pack()

    def compress_img(self,num):
        im = Image.open(file_old)
        n=100
        while n>0:
            im.save(file_new,quality=int(n)) # 默认quality=75
            news=os.path.getsize(file_new)/1024 
            print("质量=%d,大小=%f"%(n,news))
            if news<num:
                break
            n=n-1    
        
        olds=os.path.getsize(file_old)/1024
        return olds,news

    def calculate(self):
        num=self.numInput.get().strip() or '100' # 不输入的情况下为100
        # 进行 image的生成并计算
        messagebox.showinfo('Message','原来大小：%.2f,压缩输大小为：%.2f' % self.compress_img(int(num)))

app = Application()
# 设置窗口标题:
app.master.title('图片压缩小程序')
# 主消息循环:
app.mainloop()