import json
import threading
from tkinter import *
import requests
from tkinter.ttk import *
import func
import glob

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

    def run(self):

        print(self.datalines)
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

            print("字符串长度位%s" % len(str(self.bankinfo)))

            if self.bankinfo['img64'] == '':
                outinfo = "%s,请确认图片是否存在或图片格式是否符合要求!!!\n" % (line)
                self.f_file.w_file(outinfo)
                continue
            # req = session.post(self.URL, json=bankinfo, timeout=20)

            req = requests.post(self.URL, json=self.bankinfo, timeout=20)
            print("http 请求用时%s" % req.elapsed.total_seconds())

            reqjsodict = req.json()
            print(reqjsodict)

            reqjsonstr = json.dumps(reqjsodict, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

            info = "进程 %s 第%d条 内容:%s\n" % (self.threadName, (glob.get_value("%s_linenum" % self.threadName) + index + 1), line)
            print(info)

            '''
            self.threadLock.acquire()
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

            if (glob.linecount > 3000):
                delcount = '%d.100' % (glob.linecount - 3000)
                self.returns.delete('1.0', delcount)
            '''
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

            self.f_file.w_file(outinfo + "\n")
        glob.set("%s_linenum" % self.threadName, self.startline)
