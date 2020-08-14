#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
import tkinter as tk
import time

# 创建主窗口
window = tk.Tk()
window.title('进度')
window.geometry('450x90')

# 设置下载进度条
label = tk.Label(window, text='执行进度:', ).place(x=20, y=30)
canvas = tk.Canvas(window, width=300, height=22, bg="white")
canvas.place(x=110, y=30)
window.resizable(0, 0)
# window.protocol('WM_DELETE_WINDOW', lambda: closeWindow())

def closeWindow():
    pass
# 显示下载进度
def progress(spead):
    # 填充进度条
    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
    x = 100  # 未知变量，可更改
    n = 300 / x  # 465是矩形填充满的次数
    for i in range(x):
        n = n + 300 / x
        canvas.coords(fill_line, (0, 0, n, 60))
        window.update()
        time.sleep(spead)  # 控制进度条流动的速度

    # 清空进度条
    fill_line = canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="white")
    x = 500  # 未知变量，可更改
    n = 300 / x  # 465是矩形填充满的次数

    for t in range(x):
        n = n + 300 / x
        # 以矩形的长度作为变量值更新
        canvas.coords(fill_line, (0, 0, n, 60))
        window.update()
        time.sleep(0)  # 时间为0，即飞速清空进度条


btn_download = tk.Button(window, text='启动进度条', command=lambda:progress(0.01))
# btn_download.place(x=400, y=105)
btn_download.pack_forget()


def execure():
    btn_download.invoke()
    window.mainloop()


def quit():
    window.destroy()


#    progress()


if __name__ == '__main__':
    execure()
    quit()
    # window.destroy()


