linenum = 0
stopFlag = 0
linecount = 0
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

