#!/usr/bin/python
# -*- coding: UTF-8 -*-

from tkinter import *
from os import walk
import os
from tkinter import ttk
# from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import codepdf as co
import chainlp as ch
# import threading
from tkinter.messagebox import showinfo
# import bartool
import threading,time
# import tkinter as tk2
# 创建主窗口
class barTool():
    def __init__(self,speed,event):
        super().__init__()
        if not speed:
            self.speed=0.02
        self.speed = speed
        self.window = Toplevel()
        self.window.title('进度')
        self.window.geometry('450x90')
        self.window.resizable(0, 0)
        self.window.protocol('WM_DELETE_WINDOW', self.closeWindow)
        # 将窗口置顶
        self.window.wm_attributes('-topmost', 1)

        # 设置下载进度条
        Label(self.window, text='执行进度:', ).place(x=20, y=30)

        # print('self.window', self.window)
        self.canvas = Canvas(self.window, width=300, height=22, bg="white")
        self.canvas.place(x=110, y=30)
        self.progress(self.speed)
        # self.btn_download = Button(self.window, text='启动进度条', command=lambda:self.progress(speed))
        # self.btn_download.pack_forget()
        event.wait()
        self.quit()
        showinfo(title='消息', message='处理完毕')
        # self.execure()
        # self.window.destroy()




    # 显示下载进度
    def progress(self,speed):
        # 填充进度条
        fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        x = 100  # 未知变量，可更改
        n = 300 / x  # 300是矩形大小
        for i in range(x):
            n = n + 300 / x
            self.canvas.coords(fill_line, (0, 0, n, 60))
            self.window.update()
            time.sleep(speed)  # 控制进度条流动的速度

        # 清空进度条（暂时不需）
        # fill_line = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
        # x = 10  # 未知变量，可更改
        # n = 300 / x  # 465是矩形填充满的次数
        #
        # for t in range(x):
        #     n = n + 300 / x
        #     # 以矩形的长度作为变量值更新
        #     self.canvas.coords(fill_line, (0, 0, n, 60))
        #     self.window.update()
        #     time.sleep(0)  # 时间为0，即飞速清空进度条

    # def execure(self):
    #     print(self.window)
    #     # self.btn_download.invoke()
    #
    #     self.window.mainloop()
    #
    # def run(self):
    #     print('barTool.run()')




    def quit(self):
        self.window.destroy()

    def closeWindow(self):
        showinfo('警告', '正在执行，请勿退出')


# 选择路径回调函数
def selectPath():
    path_ = askopenfilename()
    path.set(path_)


root = Tk()
path = StringVar()
root.title("OCR工具(支持pdf,png,jpg)_v1.2")
root.geometry('400x260+10+10')
root.resizable(0, 0)  # 防止用户调整尺寸


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

def callBack(p, checkbox1, checkbox2):
    # timer.start()
    # Label(root, text=co.doc_current).grid(row=1, column=0)
    if None == p or len(p) <= 0:
        showinfo(title='消息', message='请选择路径！')
        return
    rw = 'w+'
    if checkbox1 == 1:
        rw = 'a+'
    # tk2 = barTool(root,0.02)
    # tk2.execure()
    # 计算图片数量
    if checkbox2 == 2:
        # 执行图片拆分
        # 统计pdf有多少张图  备注OCR模拟每张4.5秒
        count_total=co.pdfPgCount(p)
        speed = (count_total * 0.5) / 100
    elif p[p.rfind('.') + 1:len(p)] != 'pdf':
        count_total=1
        speed = (count_total * 4.5) / 100
    else:
        #统计pdf有多少张图
        count_total=co.pdfPgCount(p)
        speed = (count_total * 4.5) / 100


    poll = []  # 线程池
    # 线程一个参数也要加逗号
    event = threading.Event()  # 线程通信事件 false # event.clear() ：修改 Flag 值为 False
    thead_one = threading.Thread(target=barTool, args=(speed, event))
    poll.append(thead_one)  # 线程池添加线程
    thead_two = threading.Thread(target=conver_img_all, args=(checkbox2,p,rw, event))
    poll.append(thead_two)  # 线程池添加线程
    # 启动刚刚创建的线程
    for n in poll:
        n.start()  # 准备就绪,等待cpu执行


def conver_img_all(checkbox2,p,rw,event):
    if checkbox2 == 2:
        # 执行图片拆分
        co.get_file(p)
        co.conver_img_only()
    elif p[p.rfind('.') + 1:len(p)] != 'pdf':
        co.ocrcat(p)
    else:
        co.get_file(p)
        # print(rw)
        co.conver_img(rw)
    print('处理完毕')
    event.set()

Label(root, text="目标文件路径:").grid(row=1, column=0)
Entry(root, textvariable=path, width=30).grid(row=1, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=1, column=2)

CheckVar1 = IntVar()
# Checkbutton(root, text="生成单个文本", variable=CheckVar1, onvalue=1, offvalue=0).grid(row=2, column=0)
Radiobutton(root, text='生成多个文本', variable=CheckVar1, value=0).grid(row=2, column=0)
Radiobutton(root, text='生成单个文本', variable=CheckVar1, value=1).grid(row=2, column=1, sticky=W)
Radiobutton(root, text='pdf转图片', variable=CheckVar1, value=2).grid(row=2, column=1, sticky=E)
# CheckVar2 = IntVar()
# Checkbutton(root, text="pdf转图片", variable=CheckVar2, onvalue=2, offvalue=0).grid(row=2, column=1)

Label(root, text='请选择可读取的pdf或图片', justify=LEFT, compound='left').grid(row=0, column=0, columnspan=3, sticky=W)
Button(root, text="开始识别", fg="blue",
       command=lambda: callBack(p=path.get(), checkbox1=CheckVar1.get(), checkbox2=CheckVar1.get())).grid(row=2,
                                                                                                          column=2)

# 水平分割线
sh = ttk.Separator(root, orient=HORIZONTAL)
sh.grid(row=3, column=0, columnspan=3, sticky="we")
# 垂直分割线
# sv = ttk.Separator(root, orient=VERTICAL)
# sv.grid(row=1, column=2, rowspan=3, sticky="ns")
Label(root, text='请选择图片目录，合并为pdf').grid(row=4, column=0, columnspan=3, sticky=W)

# 选择路径回调函数
path2 = StringVar()


def selectPath2():
    path2_ = askdirectory()
    path2.set(path2_)


# 传值变量 (图片压缩后大小)
textVar = IntVar()
textVar.set(150)
e1 = Entry(root, textvariable=textVar, width=5)
e2 = Label(root, text='图片大小(kb)')


# 点击消失或显示
def printselection(p):
    if p % 2 == 1:
        e1.grid(row=6, column=1, padx=3)
        e2.grid(row=6, column=1, sticky=W)
    else:
        e1.grid_forget()
        e2.grid_forget()


CheckVar3 = IntVar()
Checkbutton(root, text="图片是否压缩", variable=CheckVar3, onvalue=1, offvalue=0,
            command=lambda: printselection(p=CheckVar3.get())).grid(row=6, column=0)

def zipimgtopdf(result_list,usezip,zipkb,event):
    for dir in result_list:
        ch.pic2pdf(dir, usezip, zipkb)
    print('处理完毕')
    event.set()
    # reply()

def callBack2(p, usezip, zipkb):
    if None == p or len(p) <= 0:
        showinfo(title='消息', message='请选择路径！')
        return
    result_set = ch.getFolderName(p)
    result_list = list(result_set)
    result_list.sort()
    #计算图片数量
    count_total=0
    for dir in result_list:
        count_total += sum([len(files) for root, dirs, files in walk(dir)])
    speed=(count_total*0.5)/100
    # print(result_list)
    # 创建一个线程
    # 创建2个线程
    poll = []  # 线程池
    #线程一个参数也要加逗号
    event = threading.Event()  #线程通信事件 false # event.clear() ：修改 Flag 值为 False
    thead_one = threading.Thread(target=barTool, args=(speed,event))
    poll.append(thead_one)  # 线程池添加线程
    thead_two = threading.Thread(target=zipimgtopdf, args=(result_list,usezip,zipkb,event))
    poll.append(thead_two)  # 线程池添加线程
    # 启动刚刚创建的线程
    for n in poll:
        n.start()  # 准备就绪,等待cpu执行






Label(root, text="目标文件夹或目录:").grid(row=5, column=0)
Entry(root, textvariable=path2, width=30).grid(row=5, column=1)
Button(root, text="路径选择", command=selectPath2).grid(row=5, column=2)

Button(root, text="开始转换", fg="blue",
       command=lambda: callBack2(p=path2.get(), usezip=CheckVar3.get(), zipkb=textVar.get())).grid(row=6, column=2)
#######
# 水平分割线
sh = ttk.Separator(root, orient=HORIZONTAL)
sh.grid(row=7, column=0, columnspan=3, sticky="we")
Label(root, text='请选择doc文件或docx文件', justify=LEFT).grid(row=8, column=0, columnspan=3, sticky=W)

# 选择路径回调函数
path3 = StringVar()


def selectPath3():
    path3_ = askopenfilename()
    path3.set(path3_)


def callBack3(p):
    # doc_files = []
    # directory = "C:\\Users\\xkw\\Desktop\\destData"
    # for root, dirs, filenames in walk(directory):
    #     for file in filenames:
    if None == p or len(p) <= 0:
        showinfo(title='消息', message='请选择路径！')
        return
    if p.endswith(".doc") or p.endswith(".docx"):
        count_total = os.path.getsize(p)
        speed = (count_total * 0.5) / 100000000
        poll = []  # 线程池
        # 线程一个参数也要加逗号
        event = threading.Event()  # 线程通信事件 false # event.clear() ：修改 Flag 值为 False
        thead_one = threading.Thread(target=barTool, args=(speed, event))
        poll.append(thead_one)  # 线程池添加线程
        thead_two = threading.Thread(target=localdoc2pdf, args=(p,event))
        poll.append(thead_two)  # 线程池添加线程
        # 启动刚刚创建的线程
        for n in poll:
            n.start()  # 准备就绪,等待cpu执行

    else:
        showinfo(title='消息', message='请选择正确的文件格式！')

def localdoc2pdf(p,event):
    ch.doc2pdf(p, p[0:p.rfind('.')])
    print("处理完毕")
    event.set()

Label(root, text="目标文件路径:").grid(row=9, column=0)
Entry(root, textvariable=path3, width=30).grid(row=9, column=1)
Button(root, text="路径选择", command=selectPath3).grid(row=9, column=2)

Button(root, text="开始转换", fg="blue", command=lambda: callBack3(p=path3.get())).grid(row=10, column=2)

# root.rowconfigure(1,weight=1)

# def refresh_data(root):
#     w = Label(root, text=str(co.doc_current)+"/"+str(co.doc_count)).grid(row=1, column=0)
#     root.after(10000, refresh_data(root))
# refresh_data(root)

# class myWindow:
#     def __init__(self, root, myTitle, flag):
#         self.top = Toplevel(root, width=300, height=200)
#         self.top.title(myTitle)


# tk2 = barTool(root,0.02)
# tk2.start()
# tk2.execure()

#tk2.quit()

root.mainloop()
