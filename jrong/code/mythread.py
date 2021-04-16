import json
import threading
from tkinter import *
import requests
from tkinter.ttk import *
import func
import glob
from tkinter import scrolledtext

class mythread(threading.Thread):
    def __init__(self, threadName, threadLock, startline, bankinfo, returns, picpathVar, pictypevaluebak, URL, f_file, datalines):
        threading.Thread.__init__(self)
        self.threadName = threadName
        self.threadLock = threadLock
        self.startline  = startline
        self.bankinfo = bankinfo
        self.returns = returns
        self.picpathVar = picpathVar
        self.pictypevaluebak = pictypevaluebak
        self.URL = URL
        self.f_file = f_file
        self.datalines = datalines
        '''
        print(type(self.threadName ))
        print(type(self.startline))
        print(type(self.bankinfo))
        print(type(self.dataPathVar))
        print(type(self.returns))
        print(type(self.picpathVar))
        print(type(self.pictypevaluebak))
        print(type(self.URL))
        print(type(self.f_file))
        print(type(self.datalines))
        '''
    def line_init(self):
        lineblock = glob.filelen / glob.threadnum

        if glob.filelen % glob.threadnum != 0:
            lineblock =  lineblock + 1

        print('glob.filelen = %d' % glob.filelen)
        print('lineblock = %d' % lineblock)

        i = int(str(self.threadName).split('_')[1])
        print(self.threadName, i)

        startline = i * lineblock
        endline = (i+1) * lineblock - 1

        if (endline > glob.filelen):
            endline = glob.filelen

        print("startline = %d" % startline)
        print("endline = %d" % endline)

        linenumname = "thread_%d_linestart" % i
        glob.set(linenumname, startline)

        linenumname = "thread_%d_lineend" % i
        glob.set(linenumname, endline)

        linenumname = "thread_%d_linecount" % i
        glob.set(linenumname, 0)



    def run(self):

        print(self.datalines)
        print("########################################")
        print(glob.get_value("%s_linestart" % self.threadName))
        print(glob.get_value("%s_lineend" % self.threadName))
        print("########################################")

        session = requests.Session()

        for index, line in enumerate(self.datalines):
            if glob.stopFlag == 1:
                return

            glob.set("%s_linecount" % self.threadName, index)
            linecount = glob.get_value("%s_linecount" % self.threadName)
            print("%s = %s" % (("%s_linecount" % self.threadName), linecount))

            reqjsonstr = ''
            info = ''

            print(line)

            self.bankinfo['IDNumber'] = line.split(',')[0]
            self.bankinfo['userName'] = line.split(',')[1]
            imgName = line.split(',')[2]
            self.bankinfo['opSerialNum'] = line.split(',')[3]

            self.bankinfo['img64'] = ""
            self.bankinfo['img64'] = func.getimg64(self.picpathVar, self.pictypevaluebak, imgName, self.bankinfo, self.returns)
            bankstr = str(self.bankinfo)

            self.threadLock.acquire()
            print(self.threadName,"======",index,"======","字符串长度位%s" % len(str(self.bankinfo)))
            self.threadLock.release()

            if self.bankinfo['img64'] == "":
                outinfo = "%s,请确认图片是否存在或图片格式是否符合要求!!!\n" % (line)
                self.f_file.w_file(outinfo)
                continue
            # req = session.post(self.URL, json=bankinfo, timeout=20)

            #print(self.bankinfo)
            req = session.post(self.URL, json=self.bankinfo, timeout=20)
            #req = requests.post(self.URL, json=self.bankinfo, timeout=20)
            print("http 请求用时%s" % req.elapsed.total_seconds())

            reqjsodict = req.json()
            print(reqjsodict)

            reqjsonstr = json.dumps(reqjsodict, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

            self.threadLock.acquire()
            #info = "进程 %s 第%d条 内容:%s\n" % (self.threadName, (glob.get_value("%s_linestart" % self.threadName) + index + 1), line)

            info = "进程 %s 第%d条 内容:%s\n" % (self.threadName, (self.startline + index + 1), line)
            print(info)

            self.returns.insert(END, info)
            self.returns.insert(END, reqjsonstr + '\n\n', index)
            self.returns.see("end")
            self.threadLock.release()

            if reqjsodict['resultCode'] != '0000':
                self.returns.tag_config(index, foreground='red')
            else:
                if reqjsodict['checkResult'] == '03':
                    self.returns.tag_config(index, foreground='green')
                elif reqjsodict['checkResult'] == '12':
                    self.returns.tag_config(index, foreground='yellow')
            self.returns.update()

            try:
                glob.linecount = int(self.returns.index('end-1c').split('.')[0])
                print("linecount = %d" % glob.linecount)
            except:
                glob.linecount = 0

            if (glob.linecount > 50):
                delcount = '%d.100' % (glob.linecount - 3000)
                self.returns.delete('1.0', delcount)

            try:
                if reqjsodict['resultCode'] != '0000':
                    outinfo = "%s,%s,%s" % (line, reqjsodict["resultCode"], reqjsodict["Reason"])
                else:
                    if str(reqjsodict).find("verify") == -1:
                        outinfo = "%s,%s,%s" % (line, reqjsodict["resultCode"], reqjsodict["checkResult"])
                    else:
                        similarity = reqjsodict["verify"]["similarity"]
                        outinfo = "%s,%s,%s,%s" % (
                        line, reqjsodict["resultCode"], reqjsodict["checkResult"], similarity)
            except KeyError:
                outinfo = "%s,%s" % (line, reqjsodict["resultCode"])

            outinfo = "%d,%s" % ((self.startline + index + 1), outinfo)

            self.f_file.w_file(outinfo + "\n")

        self.threadLock.acquire()
        self.line_init()
        self.threadLock.release()
