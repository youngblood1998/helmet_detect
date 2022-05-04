# -*- coding: cp936 -*-
import ctypes
import string
import time


def test():
    objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
    objdll.USBRELAY_Open.restype = ctypes.c_uint64

    hdl = objdll.USBRELAY_Open(1)
    print("open handle = " + str(hdl))

    for i in range(1, 5):
        res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), i, 1)  # 打开
        print("connect =  " + str(res))
        time.sleep(1)  # sleep 1s
        res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), i, 0)  # 打开
        print("disconnect =  " + str(res))

    res = objdll.USBRELAY_Close(ctypes.c_uint64(hdl))
    print("close handle = " + str(res))


    hdl = objdll.USBRELAY_Open(2)
    print("open handle = " + str(hdl))

    for i in range(1, 5):
        res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), i, 1)  # 打开
        print("connect =  " + str(res))
        time.sleep(1)  # sleep 1s
        res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), i, 0)  # 打开
        print("disconnect =  " + str(res))

    res = objdll.USBRELAY_Close(ctypes.c_uint64(hdl))
    print("close handle = " + str(res))

def test1():
    objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
    objdll.USBRELAY_Open.restype = ctypes.c_uint64

    hdl = objdll.USBRELAY_Open(1)
    print("open handle = " + str(hdl))

    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 4, 1)  # 打开
    print("connect =  " + str(res))
    time.sleep(1)  # sleep 1s
    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 4, 0)  # 打开
    print("disconnect =  " + str(res))

    # i = 1
    # while True:
    #     hdl = objdll.USBRELAY_Open(i)
    #     i += 1

def test2():
    objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
    objdll.USBRELAY_Open.restype = ctypes.c_uint64

    relay_dic = {}

    i = 1
    while True:
        hdl = objdll.USBRELAY_Open(i)
        print("open handle = " + str(hdl))
        i += 1
        if len(str(hdl)) != 20:
            j = 1
            while True:
                res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), j, 1)  # 打开
                print("connect =  " + str(res))
                if res == 0:
                    j += 1
                else:
                    break
            relay_dic[str(hdl)] = j
        else:
            break
    print(relay_dic)

    for key, value in relay_dic.items():
        for i in range(1, value):
            res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(int(key)), i, 0)  # 打开
            print("disconnect =  " + str(res))
        res = objdll.USBRELAY_Close(ctypes.c_uint64(int(key)))
        print("close handle = " + str(res))