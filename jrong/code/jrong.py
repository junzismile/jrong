#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import requests
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import scrolledtext
import ast
import tkinter.simpledialog
import func
import glob
from  mythread import *
from file import *
from tkinter.font import Font
from tkinter.ttk import *

MYopid = [9000]
bankinfo = {}
glob.linenum = 0
glob.stopFlag = 0
glob.linecount = 0
#bankinfo = {'APPID':'A0001','SessionID':'20180323171409A0001','RequestId':'-1','RequestTime':'20160112144615','opId':'9000','opType':'1','phoneNumber':'','certType':'0101','IDNumber':'','userName':'','Gender':'','Lon':'','Lat':'','img64': '', 'livingRegion': '', 'livingCity': '', 'homeArea': ''}

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        #self.setjson = ""
        Frame.__init__(self, master)
        self.master.title('备案核验')
        #self.master.geometry('800x600')

        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        self.master.geometry('%dx%d+%d+%d' % (800, 600, (screenwidth - 800) / 2, (screenheight - 600) / 2 - 100))
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()
        self.style = Style()

        '''========================================================='''
        menubar  =  Menu(self)
        set = Menu(menubar, tearoff=0)
        set.add_command(label="修改url", command = self.changeUrl)
        set.add_command(label="修改消息体", command = self.changeMsgbody)
        menubar.add_cascade(label="设置", menu=set)
        self.top.config(menu = menubar)

        '''========================================================='''
        self.returnsVar = StringVar(value='')
        self.returns = scrolledtext.ScrolledText(self.top, width=100, height=50, relief="solid")
        self.returns.place(relx=0.04, rely=0.34, relwidth=0.923, relheight=0.60)

        '''========================================================='''
        self.style.configure('Label1_1.TLabel', anchor='w', font=('宋体', 9))
        self.Label1_1 = Label(self.top, text='能力：', style='Label1_1.TLabel')
        self.Label1_1.place(relx=0.04, rely=0.061, relwidth=0.109, relheight=0.043)

        self.opIdList = MYopid
        self.opId = Combobox(self.top, values=self.opIdList, font=('宋体',9))
        self.opId.place(relx=0.16, rely=0.061, relwidth=0.109, relheight=0.051)
        self.opId.set(self.opIdList[0])
        self.opId.bind("<<ComboboxSelected>>", self.getopid)

        self.sendbutton = Button(self.top, text='发送', command=self.sendBankInfo)
        self.sendbutton.place(relx=0.668, rely=0.061, relwidth=0.109, relheight=0.051)

        self.sendbutton = Button(self.top, text='暂停', command=self.stopsend)
        self.sendbutton.place(relx=0.800, rely=0.061, relwidth=0.109, relheight=0.051)

        '''========================================================='''

        '''=======================数据源=================================='''
        self.style.configure('Label2.TLabel', anchor='w', font=('宋体', 9))
        self.Label2 = Label(self.top, text='源数据路径', style='Label2.TLabel')
        self.Label2.place(relx=0.04, rely=0.163, relwidth=0.109, relheight=0.064)

        if self.dataPathVar == "":
            self.dataPathVar = StringVar(value='请选择')
        else:
            self.dataPathVar = StringVar(value=self.dataPathVar)

        self.dataPath = Entry(self.top, textvariable=self.dataPathVar, font=('宋体', 9))
        self.dataPath.place(relx=0.16, rely=0.163, relwidth=0.500, relheight=0.046)

        self.dataselectpath = Button(self.top, text='文本选择', command=self.selectDataPath)
        self.dataselectpath.place(relx=0.668, rely=0.163, relwidth=0.109, relheight=0.046)
        '''========================================================='''

        '''=========================图片================================'''
        self.style.configure('Label4.TLabel', anchor='w', font=('宋体', 9))
        self.Label4 = Label(self.top, text='图片路径', style='Label4.TLabel')
        self.Label4.place(relx=0.04, rely=0.224, relwidth=0.109, relheight=0.043)

        if self.picpathVar == "":
            self.picpathVar = StringVar(value='请选择')
        else:
            self.picpathVar = StringVar(value=self.picpathVar)

        self.picpath = Entry(self.top, textvariable=self.picpathVar, font=('宋体',9))
        self.picpath.place(relx=0.16, rely=0.224, relwidth=0.500, relheight=0.046)

        self.picselectpath = Button(self.top, text='路径选择', command=self.selectPicPath)
        self.picselectpath.place(relx=0.668, rely=0.224, relwidth=0.109, relheight=0.046)

        self.pictypevalue = IntVar(value=0)
        self.pictypevaluebak = 0
        self.pictype = Checkbutton(self.top, text='base64', variable=self.pictypevalue, onvalue=1, offvalue=0, command=self.typeSelection)
        self.pictype.place(relx=0.800, rely=0.224, relwidth=0.08, relheight=0.046)

        '''========================================================='''
    def stopsend(self):
        print('stop')
        print(glob.stopFlag, glob.FFlag)

        if glob.stopFlag == 1:
            return

        glob.stopFlag = 1


        if (glob.threadnum == 1):
            glob.linenum = glob.linenum + glob.linecount + 1
            print('linenum = %s' % (glob.linenum))
        else:
            if glob.FFlag == 1:
                return

            glob.FFlag = 0
            for i in range(glob.threadnum):
                linenum = glob.get_value("thread_%d_linenum" % i)
                linecount = glob.get_value("thread_%d_linecount" % i)
                glob.set("thread_%d_linenum" % i, (linenum + linecount + 1))

    def changeUrl(self):
        url = self.URL
        url = tkinter.simpledialog.askstring(title = '获取最新url',prompt='请输入您要替换的url：                                   ',initialvalue = url)
        print(url)

        if url != None:
            self.URL = url
            print('self.URl = ' + self.URL)
            func.setset(self.URL, self.dataPathVar, self.picpathVar)
            #urlpath = resource_path("jrongurl.txt");
            #self.w_file(urlpath, self.URL)

    def changeMsgbody(self):
        print('changeMsgBody')
        global  bankinfo
        bankStr = str(bankinfo)
        bankStr = tkinter.simpledialog.askstring(title='获取最新请求消息体', prompt='请输入您要替换的消息体：                                   ',initialvalue=bankStr)
        print(bankStr)

        if bankStr != None:
            bankinfo = ast.literal_eval(bankStr)
            print('bankinfo = ' + str(bankinfo))
            #bankinfopath = resource_path("bankinfo.txt");
            bankinfopath = "bankinfo.txt"
            func.w_file(bankinfopath, str(bankinfo))

    def getopid(self, *args):
        bankinfo['opId'] = self.opId.get()
        print(bankinfo['opId'])

    def typeSelection(self, *args):
        self.pictypevaluebak = self.pictypevalue.get()
        print(self.pictypevaluebak)

    def selectPicPath(self, *args): # 选择图片路径
        picpathVar = filedialog.askdirectory()
        print(picpathVar)
        picpathVar = picpathVar.replace("/", "\\\\")
        print(picpathVar)
        self.picpathVar.set(picpathVar)
        func.setset(self.URL, self.dataPathVar, self.picpathVar)

    def selectDataPath(self, *args): # 选择数据源路径
        dataPathVar = filedialog.askopenfilename()
        print(dataPathVar)
        dataPathVar = dataPathVar.replace("/", "\\\\")
        print(dataPathVar)
        self.dataPathVar.set(dataPathVar)
        func.setset(self.URL, self.dataPathVar, self.picpathVar)

    def thread_getdatalist(self):
        datalist = list()

        datalines = func.getBankInfo(self.dataPathVar)
        print(datalines)

        linelen = len(datalines)
        lineblock = linelen / glob.threadnum

        print('linelen = %d' % linelen)
        print('lineblock = %d' % lineblock)

        if (glob.threadnum > 1):
            for i in range(glob.threadnum):
                linenumname = "thread_%d_linenum" % i

                startline = glob.get_value(linenumname)
                endline = startline + lineblock - 1

                if (endline > linelen):
                    endline = linelen

                linenumname = "thread_%d_lineend" % i
                glob.set(linenumname, endline)

                linenumname = "thread_%d_linenum" % (i + 1)
                glob.set(linenumname, endline + 1)

                print("startline = %d" % startline)
                print("endline = %d" % endline)

                data = datalines[int(startline):int(endline + 1)]
                datalist.append(data)



        return datalist


    def sendBankInfo(self):
        print('sendBankInfo')
        start = time.time()
        datalist = []

        glob.stopFlag = 0

        f_file = file("./out.txt", "a+")
        datalines = func.getBankInfo(self.dataPathVar)
        print(datalines)

        linelen = len(datalines)
        lineblock = linelen / glob.threadnum
        #threads = list()

        print('glob.threadnum = %d' % glob.threadnum)
        print('linelen = %d' % linelen)
        print('lineblock = %d' % lineblock)
        picpath = self.picpathVar.get()

        if (glob.threadnum > 1):
            threadLock = threading.Lock()

            for i in range(glob.threadnum):
                #print('==================================')
                if (glob.FFlag == 1):
                    linenumname = "thread_%d_linenum" % i

                    startline = glob.get_value(linenumname)
                    endline = startline + lineblock-1

                    #print("startline = %d" % startline)
                    #print("endline = %d" % endline)

                    if (endline > linelen):
                        endline = linelen

                    linenumname = "thread_%d_lineend" % i
                    glob.set(linenumname, endline)

                    linenumname = "thread_%d_linenum" % (i + 1)
                    glob.set(linenumname, endline+1)

                    #print('==================================')
                else:
                    startline = glob.get_value("thread_%d_linenum", i)
                    endline = glob.get_value("thread_%d_lineend", i)

                print("startline = %d" % startline)
                print("endline = %d" % endline)

                data = datalines[int(startline):int(endline+1)]
                datalist.append(data)

            glob.FFlag = 0


            for i in range(glob.threadnum):
                threadName = ("thread_%d" % i)

                thread = mythread(threadName, threadLock, startline, bankinfo, self.returns, picpath, self.pictypevaluebak, self.URL, f_file, datalist[i])
                thread.start()
                #threads.append(thread)
            '''
            glob.FFlag = 0

            for thread in threads:
                thread.join()
            '''


            glob.FFlag = 1

        else:
            print('linenum = %s' % (glob.linenum))
            datalines = datalines[glob.linenum:]

            if glob.linenum == 0:
                self.returns.delete('1.0', 'end')

            func.sendInfo(bankinfo, self.returns, picpath, self.pictypevaluebak, self.URL, f_file, datalines)

        del(f_file)
        end = time.time()
        print('耗时：%s' % (end - start))

class Application(Application_ui):
    def __init__(self, master=None):
        global bankinfo
        bankinfo = func.getbankStr()
        self.URL, self.dataPathVar, self.picpathVar = func.getset()
        glob._init()
        glob.set("thread_0_linenum", 0)
        Application_ui.__init__(self, master)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass
