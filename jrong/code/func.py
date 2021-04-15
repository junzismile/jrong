import ast
import json
import os
import time

import chardet

from file import *
import requests
import base64
from tkinter import *
import glob
import jrong

def w_file(self, filename, line, type="w"):
    f = open(filename, type)
    f.write(line)
    f.close()

def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
        print(base_path)
    else:
        base_path = os.path.abspath(".")
        print(base_path)
    return os.path.join(base_path, relative_path)

def geturl(self):#获取url
    urlpath = resource_path("jrongurl.txt");
    f = open(urlpath, "r")
    URL = f.readline()
    print(URL)
    f.close()
    return URL

def getbankStr():#获取请求消息
    #bankinfopath = resource_path("bankinfo.txt")
    bankinfopath = "bankinfo.txt"
    f = open(bankinfopath, "r")
    bankStr = f.readline()
    f.close()
    #print(bankStr)

    if bankStr != '':
        #global bankinfo
        bankinfo = ast.literal_eval(bankStr)
        print(bankinfo['APPID'])
        return bankinfo

def setset(URL, dataPathVar, picpathVar):
    #setpath = resource_path("set.txt")
    setpath = "set.txt"
    setjson = {'url': '', 'datapath': '', 'picpath': ''}
    setjson['url'] = URL
    setjson['datapath'] = dataPathVar.get()
    setjson['picpath'] = picpathVar.get()

    print(setjson['datapath'])
    print(setjson['picpath'])
    print(setjson['url'])

    f = open(setpath, "w")
    f.writelines(str(setjson))
    f.close()

def getset():
    #self.setpath = resource_path("set.txt")
    setpath = "set.txt"
    print(setpath)
    f = open(setpath, "r")
    setStr = f.read()
    print(setStr)
    f.close()

    if setStr != '':
        setjson = ast.literal_eval(setStr)
        print(setjson)
        URL = setjson['url']
        dataPathVar = setjson['datapath']
        picpathVar = setjson['picpath']

        print(URL)
        print(dataPathVar)
        print(picpathVar)

        return URL, dataPathVar, picpathVar

def getBankInfo(dataPathVar):
    datafilepath = dataPathVar.get()
    print(datafilepath)

    f = open(datafilepath, 'rb')
    glob.encode = chardet.detect(f.read())['encoding']
    print("glob.encode = " + glob.encode)
    f.close()

    with open(datafilepath, mode='r', encoding='UTF-8') as datafile:
        datalines = datafile.read().splitlines()
        print(datalines)
    return datalines

def getimg64(picpathVar, pictypevaluebak, imgName, bankinfo, returns):
    #picpath = self.picpathVar.get() + '\\\\' + bankinfo['IDNumber']
    picpath = ""
    bankinfo['img64'] = ""
    picstr = ""
    picpath = picpathVar + '\\\\' + imgName

    if (picpath != '' and str(bankinfo['opId']) == '9000'):
        if pictypevaluebak:
            try:
                picfile = open(picpath, 'r')
            except FileNotFoundError:
                #self.returns.delete('1.0', 'end')
                returns.insert(INSERT, '图片路径错误，请确认图片是否存在!!!\n\n')
                returns.see("end")
            try:
                picstr = picfile.read()
            except UnicodeDecodeError:
                #self.returns.delete('1.0', 'end')
                returns.insert(INSERT, '传入的不是base64编码后的图片，请确认!!!\n\n')
                returns.see("end")
                return ""
            except UnboundLocalError:
                returns.insert(INSERT, '传入的不是base64编码后的图片，请确认!!!\n\n')
                returns.see("end")
                return ""

            picfile.close()
            bankinfo['img64'] = picstr
            return picstr
        else:
            try:
                picfile = open(picpath, 'rb')
                picstr = picfile.read()
                picfile.close()
                bankinfo['img64'] = base64.b64encode(picstr).decode()
                return bankinfo['img64']
                #print(bankinfo['img64'])
            except FileNotFoundError:
                #self.returns.delete('1.0', 'end')
                returns.insert(INSERT, '图片路径错误，请确认图片是否存在!!!\n\n')
                returns.see("end")
                return ""

def sendInfo(bankinfo, returns, picpathVar, pictypevaluebak, URL, f_file, datalines):#发送请求
    #session = requests.Session()
    for index, line in enumerate(datalines):
        if glob.stopFlag == 1:
            return

        glob.linecount = index
        #print('glob.linecount = %s' % (glob.linecount))
        #print('stopFlag = %s' % (stopFlag))

        reqjsonstr = ''
        info = ''
        bankinfo['IDNumber'] = line.split(',')[0]
        bankinfo['userName'] = line.split(',')[1]
        imgName = line.split(',')[2]
        bankinfo['opSerialNum'] = line.split(',')[3]

        bankinfo['img64'] = ""
        bankinfo['img64'] = getimg64(picpathVar, pictypevaluebak, imgName, bankinfo, returns)
        bankstr = str(bankinfo)

        print("字符串长度位%s" % len(str(bankinfo)))

        if bankinfo['img64'] == '':
            outinfo = "%s,请确认图片是否存在或图片格式是否符合要求!!!\n" % (line)
            f_file.w_file(outinfo)
            continue
        #req = session.post(self.URL, json=bankinfo, timeout=20)

        req = requests.post(URL, json=bankinfo, timeout=20)
        print("http 请求用时%s" % req.elapsed.total_seconds())

        reqjsodict = req.json()
        print(reqjsodict)

        reqjsonstr = json.dumps(reqjsodict, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

        info = "第%s条 内容:%s\n" % (glob.linenum+index+1, line)
        returns.insert(END, info)
        returns.insert(END, reqjsonstr+'\n\n', index)
        returns.see("end")

        if reqjsodict['resultCode'] != '0000':
           returns.tag_config(index, foreground='red')
        else:
            if reqjsodict['checkResult'] == '03':
                returns.tag_config(index, foreground='green')
            elif reqjsodict['checkResult'] == '12':
                returns.tag_config(index, foreground='yellow')
        returns.update()

        try:
            glob.linecount = int(returns.index('end-1c').split('.')[0])
            print("linecount = %d" % glob.linecount)
        except:
            glob.linecount = 0

        if (glob.linecount > 3000):
            delcount = '%d.100' % (glob.linecount - 3000)
            returns.delete('1.0', delcount)

        try:
            if reqjsodict['resultCode'] != '0000':
                outinfo = "%s,%s,%s" % (line, reqjsodict["resultCode"], reqjsodict["Reason"])
            else:
                if str(reqjsodict).find("verify") == -1:
                    outinfo = "%s,%s,%s" % (line, reqjsodict["resultCode"], reqjsodict["checkResult"])
                else:
                    similarity = reqjsodict["verify"]["similarity"]
                    outinfo = "%s,%s,%s,%s" % (line, reqjsodict["resultCode"], reqjsodict["checkResult"], similarity)
        except KeyError:
            outinfo = "%s,%s" % (line, reqjsodict["resultCode"])

        f_file.w_file(outinfo +"\n")
    glob.linenum = 0

