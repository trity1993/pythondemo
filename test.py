from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename


def selectPath():
    path_ = askdirectory()
    path.set(path_)

def load_file():
    fname = askopenfilename(filetype=(("txt files", "*.txt"),("HTML files", "*.html;*.htm")))
    path.set(fname)

root = Tk()
path = StringVar()

Label(root,text = "目标路径:").grid(row = 0, column = 0)
Entry(root, textvariable = path).grid(row = 0, column = 1)
Button(root, text = "路径选择", command = load_file).grid(row = 0, column = 2)

root.mainloop()