linenum = 0
stopFlag = 0
linecount = 0
threadnum = 1
index = 0
FFlag = 1
picpathVar = ""
encode = 'UTF-8'

def _init():
    global _global_dict
    _global_dict = {}

def set(key, value):
    _global_dict[key] = value
    print("set %s = %d\n" % (key, value))

def get_value(key,defValue=None):
    try:
        print("get %s = %d\n" % (key, _global_dict[key]))
        return _global_dict[key]
    except KeyError:
        print('KeyError')
        return defValue

