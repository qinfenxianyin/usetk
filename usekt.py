#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *
# from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import codepdf as co
# import threading
from tkinter.messagebox import showinfo


# 选择路径回调函数
def selectPath():
    path_ = askopenfilename()
    path.set(path_)


root = Tk()
path = StringVar()
root.title("PDF读取工具_v1.1")

Label(root, text="目标路径:").grid(row=0, column=0)
Entry(root, textvariable=path).grid(row=0, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)


def reply():
    showinfo(title='消息', message='处理完毕')


# def fun_timer():
#     print('Hello Timer!')
#     # Label(root, text=co.doc_current).grid(row=1, column=0)
#     showinfo(title='消息', message=str(co.doc_current))
#     global timer
#     timer = threading.Timer(5.5, fun_timer)
#     timer.start()
#
# timer = threading.Timer(1, fun_timer)

def callBack(p, manytxt):
    # timer.start()
    # Label(root, text=co.doc_current).grid(row=1, column=0)
    rw = 'w+'
    if manytxt == 1:
        rw = 'a+'
    if p[p.rfind('.') + 1:len(p)] != 'pdf':
        co.ocrcat(p)
    else:
        co.get_file(p)
        print(rw)
        co.conver_img(rw)
    print('处理完毕')
    reply()


CheckVar1 = IntVar()
Checkbutton(root, text="生成单个文本", variable=CheckVar1, onvalue=1, offvalue=0).grid(row=1, column=1)

Label(root, text='可读取pdf或图片').grid(row=1, column=0)
Button(root, text="运行", command=lambda: callBack(p=path.get(), manytxt=CheckVar1.get())).grid(row=1, column=2)

# def refresh_data(root):
#     w = Label(root, text=str(co.doc_current)+"/"+str(co.doc_count)).grid(row=1, column=0)
#     root.after(10000, refresh_data(root))
# refresh_data(root)
root.mainloop()
