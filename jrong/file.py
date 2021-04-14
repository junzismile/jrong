# Filename: file.py
class file(object):
    def __new__(cls, filename, type="r"):
        ob = super(file, cls).__new__(cls)
        return ob

    def __init__(self, filename, type):
        self.filename = filename
        self.type = type
        self.file = open(self.filename, self.type)

    def w_file(self, line):
        self.file.write(line)
        self.file.flush()

    def r_file(self):
        return self.file.readlines()

    def  __del__(self):
        print('file %s close' % self.filename)
        self.file.close()