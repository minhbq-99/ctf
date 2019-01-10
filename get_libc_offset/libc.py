import os

DB_DIR = os.path.dirname(os.path.abspath(__file__)) + "/db/"

'''offset: int 
symbol: string: name of symbol with given offset
ret_symbol: string: name of symbol that you want to get offset
returned value: offset of ret_symbol'''

def get_libc_offset(offset,symbol,ret_symbol):
    files = os.listdir(DB_DIR)
    for symbol_file in files:
        out = open(DB_DIR + symbol_file,"r").read().replace("\n"," ").strip().split(" ")
        tmp = dict([(out[i],out[i+1]) for i in range(0,len(out),2)])
        if((symbol in tmp.keys()) and (int(tmp[symbol][-3:],16) == offset)):
            if(ret_symbol in tmp.keys()):
                return int(tmp[ret_symbol],16)

'''
input_dict {symbol:offset}
ret_symbol: string: name of symbol that you want to get offset
returned value: offset of ret_symbol'''

def get_libc_offset_dict(input_dict,ret_symbol):
    files = os.listdir(DB_DIR)
    for symbol_file in files:
        out = open(DB_DIR + symbol_file,"r").read().replace("\n"," ").strip().split(" ")
        tmp = dict([(out[i],out[i+1]) for i in range(0,len(out),2)])
        flag = True
        for key in input_dict.keys():
            if(not ((key in tmp.keys()) and (int(tmp[key][-3:],16) == input_dict[key]))):
                flag = False
                break
        if (flag):
            if(ret_symbol in tmp.keys()):
                return int(tmp[ret_symbol],16)
