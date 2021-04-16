# Filename: file.py
import time
from operator import itemgetter

class file(object):
    def __new__(cls, filename, type="r", encoding="UTF-8"):
        ob = super(file, cls).__new__(cls)
        return ob

    def __init__(self, filename, type, encoding):
        self.filename = filename
        self.type = type
        self.encoding = encoding
        self.file = open(self.filename, mode=self.type, encoding=self.encoding)

    def w_file(self, line):
        self.file.write(line)
        self.file.flush()

    def r_file(self):
        return self.file.readlines()

    def sort(self):
        table = []
        #header = self.filename.readline()  # 读取并弹出第一行
        for line in self.file:
            col = line.split(',')  # 每行分隔为列表，好处理列格式
            col[1] = int(col[1])
            table.append(col)  # 嵌套列表table[[8,8][*,*],...]

        table_sorted = sorted(table, key=itemgetter(1))  # 先后按列索引3,4排序
        print(table_sorted)

        for row in table_sorted:  # 遍历读取排序后的嵌套列表
            row = [str(x) for x in row]  # 转换为字符串格式，好写入文本
            print("\t".join(row) + '\n')

    def  __del__(self):
        print('file %s close' % self.filename)

        self.sort()
        self.file.close()
        return time.time()