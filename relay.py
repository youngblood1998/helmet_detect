# -*- coding: cp936 -*-
import ctypes
import string
import time


def test():
    objdll = ctypes.windll.LoadLibrary('./usbrelay.dll')
    objdll.USBRELAY_Open.restype = ctypes.c_uint64
    hdl = objdll.USBRELAY_Open(1)
    print("open handle = " + str(hdl))
    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 1, 1) #打开
    print("connect =  " + str(res))
    time.sleep(1)  #sleep 1s
    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 1, 0) #打开
    print("disconnect =  " + str(res))
    res = objdll.USBRELAY_Close(ctypes.c_uint64(hdl))
    print("close handle = " + str(res))
    # input('\n******************ALL OK; Press ENTER to EXIT**********')
    hdl = objdll.USBRELAY_Open(1)
    print("open handle = " + str(hdl))
    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 2, 1)  # 打开
    print("connect =  " + str(res))
    time.sleep(1)  # sleep 1s
    res = objdll.USBRELAY_SetRelay(ctypes.c_uint64(hdl), 2, 0)  # 打开
    print("disconnect =  " + str(res))
    res = objdll.USBRELAY_Close(ctypes.c_uint64(hdl))
    print("close handle = " + str(res))