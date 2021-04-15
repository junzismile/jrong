linenum = 0
stopFlag = 0
linecount = 0
threadnum = 2
index = 0
FFlag = 1
picpathVar = ""

def _init():
    global _global_dict
    _global_dict = {}

def set(key, value):
    _global_dict[key] = value

def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue

