# -*- coding: utf-8 -*-
import glob
import fitz
import os
import traceback
from win32com.client import Dispatch
import compressimg as ci

def getFolderName(path):
    reset = set()
    if os.path.exists(path):
        if os.path.isdir(path):
            dirlist = os.listdir(path)  # type: List[Union[bytes, str]]
            for dir in dirlist:
                dir = path + "\\" + dir
                reset = reset | getFolderName(dir)
        elif os.path.isfile(path):
            reset.add(os.path.dirname(path))
        else:
            reset.add(os.path.dirname(path))
        return reset
    else:
        print("dir [%s] is not exist" % path)


def getOutputDirName(path,source_folder):
    dirname = ''
    if "\\" in path:
        slist = path.split("\\")
    else:
        slist = path.split("/")
    if source_folder.endswith('\\'):
        dirname = slist[slist.__len__() - 2] + ".pdf"
    else:
        dirname = slist[slist.__len__() - 1] + ".pdf"
    return source_folder + dirname if source_folder.endswith("\\") else source_folder + "\\" + dirname


def pic2pdf(source_folder,usezip):  # "D:\\火影漫画全集\\1~40 卷\\第03卷"
    source_folderbak=source_folder
    if usezip == 1 and not os.path.exists(source_folder+'/out'):
        os.mkdir(source_folder+'/out',0o777)
    doc = fitz.open()
    try:
        # print(source_folder)
        name = getOutputDirName(source_folder,source_folder)
        if os.path.exists(name):
            return
        source_folder = source_folder + "*" if source_folder.endswith("\\") else source_folder + "/*"
        # print('source_folder_list ', list(glob.glob(source_folder)))
        for img in sorted(glob.glob(source_folder)):  # 读取图片，确保按文件名排序
            if img.endswith('out'):
                continue
            imgzip=img
            if usezip==1:
                res=ci.compress_image(img)
                imgzip=res[0]
                if imgzip.endswith('png'):
                    imgzip=ci.PNG_JPG(imgzip)
                    res = ci.compress_image2(imgzip)
                    imgzip = res[0]
                # print('usezip ', imgzip,'len ',res[1])
            imgdoc = fitz.open(imgzip)  # 打开图片
            pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
            imgpdf = fitz.open("pdf", pdfbytes)
            doc.insertPDF(imgpdf)  # 将当前页插入文档
        print("out put name is %s" % name)
        doc.save(name)  # 保存pdf文件
        os.remove(source_folderbak+'/out')
    except:
        print("目录：[ %s ] 转换pdf异常" % source_folder)
        traceback.print_exc()
    finally:
        doc.close()


def doc2pdf(doc_name, pdf_name):
    print(doc_name)
    print(pdf_name)
    try:
        try:
            # word = Dispatch("Word.Application")
            word = Dispatch("Kwps.Application")  #wps 支持msoffice
        except:
            print('use wps')
            word = Dispatch("Wps.Application")
        if os.path.exists(pdf_name):
            os.remove(pdf_name)
        worddoc = word.Documents.Open(doc_name, ReadOnly=1)
        worddoc.SaveAs(pdf_name, FileFormat=17)
        worddoc.Close()
        return pdf_name
    except:
        return 1


if __name__ == '__main__':
    source_folder = 'D:\\火影漫画全集\\1~40 卷'
    result_set = getFolderName(source_folder)

    result_list = list(result_set)
    result_list.sort()
    print(result_list)
    for dir in result_list:
        pic2pdf(dir)
